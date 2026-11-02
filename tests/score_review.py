"""Mechanical gate for supplied UX judgments, not a prose/behavior evaluator."""
import argparse
import hashlib
import json
from pathlib import Path
import yaml

ROOT = Path(__file__).resolve().parents[1]


def score(review, judgments, rubric, case):
    errors = []
    if not isinstance(review, str):
        return {"status": "invalid-receipt", "errors": ["Review must be UTF-8 text"]}
    try:
        review_bytes = review.encode("utf-8")
    except UnicodeError:
        return {"status": "invalid-receipt", "errors": ["Review must be UTF-8 text"]}
    if not review.strip():
        errors.append("A nonempty review artifact is required")
    if not isinstance(judgments, dict):
        return {"status": "invalid-receipt", "errors": errors + ["Judgments must be an object"]}
    if judgments.get("format") != "ux-adjudication/v1":
        errors.append("Expected ux-adjudication/v1")
    if judgments.get("review_sha256") != hashlib.sha256(review_bytes).hexdigest():
        errors.append("Judgment/source hash mismatch")
    if judgments.get("case_id") != case["id"]:
        errors.append("Case ID mismatch")

    def evidence_present(record):
        quote = record.get("evidence_quote") if isinstance(record, dict) else None
        return isinstance(quote, str) and bool(quote.strip()) and quote in review

    hard = judgments.get("hard_failures")
    if not isinstance(hard, dict) or set(hard) != set(rubric["hard_failures"]) or any(type(x) is not bool for x in hard.values()):
        errors.append("Every hard-failure judgment must be explicit and boolean")
        hard = {}
    ratings = judgments.get("ratings")
    weighted = total = 0
    if not isinstance(ratings, dict) or set(ratings) != set(rubric["dimensions"]):
        errors.append("Every rubric dimension must be rated exactly once")
        ratings = {}
    for name, record in ratings.items():
        value = record.get("score") if isinstance(record, dict) else None
        if type(value) is not int or value not in (0, 1, 2) or not evidence_present(record):
            errors.append("Invalid score or missing source quote: " + name)
            continue
        weight = rubric["dimensions"][name]["weight"]
        weighted += weight * value
        total += weight * 2
    checks = judgments.get("case_assertions")
    expected = set(range(len(case["expected"])))
    if not isinstance(checks, list) or len(checks) != len(expected):
        errors.append("Every case assertion must be judged")
        checks = []
    indices = [x.get("index") for x in checks if isinstance(x, dict)]
    if any(type(x) is not int for x in indices) or set(indices) != expected or len(indices) != len(set(indices)):
        errors.append("Case assertion indices must cover the exact case without duplicates")
    for record in checks:
        if not isinstance(record, dict) or type(record.get("satisfied")) is not bool or not evidence_present(record):
            errors.append("Case assertion requires a boolean judgment and a source quote")
    if not isinstance(judgments.get("adjudicator"), str) or not judgments["adjudicator"].strip():
        errors.append("Record the adjudicator identifier; this field does not authenticate them")
    if errors or not total:
        return {"status": "invalid-receipt", "errors": errors or ["No scored dimensions"]}
    fraction = weighted / total
    passed = (sum(hard.values()) <= rubric["passing"]["hard_failures_allowed"]
              and fraction >= rubric["passing"]["minimum_weighted_fraction"]
              and all(x["satisfied"] for x in checks))
    return {"status": "pass-on-supplied-judgments" if passed else "fail-on-supplied-judgments",
            "weighted_fraction": fraction, "hard_failures": sum(hard.values()), "case_assertions": len(checks),
            "limits": "Mechanical coverage, source binding and arithmetic only. Quotes do not prove semantic support, adjudicator independence, usability benefit or accessibility conformance."}


def unique_json_object(pairs):
    result = {}
    for key, value in pairs:
        if key in result:
            raise ValueError("Duplicate JSON key: " + key)
        result[key] = value
    return result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("review", type=Path)
    parser.add_argument("judgments", type=Path)
    args = parser.parse_args()
    rubric = yaml.safe_load((ROOT / "tests/evaluation-rubric.yaml").read_text())
    cases = yaml.safe_load((ROOT / "tests/benchmark-cases.yaml").read_text())["cases"]
    try:
        judgments = json.loads(args.judgments.read_bytes().decode("utf-8"), object_pairs_hook=unique_json_object)
        review = args.review.read_bytes().decode("utf-8")
    except (OSError, UnicodeError, ValueError) as error:
        print(json.dumps({"status": "invalid-receipt", "errors": [str(error)]}, indent=2))
        return 1
    if not isinstance(judgments, dict):
        print(json.dumps({"status": "invalid-receipt", "errors": ["Judgments must be an object"]}))
        return 1
    selected = next((c for c in cases if c["id"] == judgments.get("case_id")), None)
    if selected is None:
        parser.error("Unknown benchmark case_id")
    # Preserve exact UTF-8 bytes when re-encoding, including CRLF and a BOM.
    result = score(review, judgments, rubric, selected)
    print(json.dumps(result, indent=2))
    return 0 if result["status"] == "pass-on-supplied-judgments" else 1


if __name__ == "__main__":
    raise SystemExit(main())
