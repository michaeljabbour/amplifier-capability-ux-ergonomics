"""Exposed fictional adjudication controls; no target-method outcome claims."""
import copy
import hashlib
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
import yaml
from score_review import score

ROOT = Path(__file__).resolve().parents[1]
RUBRIC = yaml.safe_load((ROOT / "tests/evaluation-rubric.yaml").read_text())
CASE = yaml.safe_load((ROOT / "tests/benchmark-cases.yaml").read_text())["cases"][0]
REVIEW = "Fictional review: evidence is missing; cause unknown; discriminate with a study."


def receipt():
    return {"format": "ux-adjudication/v1", "review_sha256": hashlib.sha256(REVIEW.encode()).hexdigest(),
            "case_id": CASE["id"], "adjudicator": "fictional-control-only",
            "hard_failures": {name: False for name in RUBRIC["hard_failures"]},
            "ratings": {name: {"score": 2, "evidence_quote": "Fictional review"} for name in RUBRIC["dimensions"]},
            "case_assertions": [{"index": index, "satisfied": True, "evidence_quote": "Fictional review"} for index in range(len(CASE["expected"]))]}


class ScoreGateTests(unittest.TestCase):
    def test_non_text_api_input_is_structured_invalid_receipt(self):
        for value in (None, b"bytes", 7, False, [], "\ud800"):
            with self.subTest(value=value):
                self.assertEqual(score(value, receipt(), RUBRIC, CASE)["status"], "invalid-receipt")

    def test_cli_preserves_raw_utf8_crlf_hash_and_rejects_duplicate_keys(self):
        raw = (REVIEW + "\r\nSecond fictional line.\r\n").encode("utf-8")
        record = receipt()
        record["review_sha256"] = hashlib.sha256(raw).hexdigest()
        with tempfile.TemporaryDirectory() as directory:
            review_path = Path(directory) / "review.txt"
            judgment_path = Path(directory) / "judgments.json"
            review_path.write_bytes(raw)
            command = [sys.executable, str(ROOT / "tests/score_review.py"), str(review_path), str(judgment_path)]
            judgment_path.write_text(json.dumps(record))
            valid = subprocess.run(command, capture_output=True, text=True)
            self.assertEqual(valid.returncode, 0, valid.stdout + valid.stderr)
            self.assertEqual(json.loads(valid.stdout)["status"], "pass-on-supplied-judgments")
            key = next(iter(record["hard_failures"]))
            serialized = json.dumps(record)
            self.assertIn(json.dumps(key) + ": false", serialized)
            ambiguous = serialized.replace(json.dumps(key) + ": false", json.dumps(key) + ": true, " + json.dumps(key) + ": false", 1)
            judgment_path.write_text(ambiguous)
            invalid = subprocess.run(command, capture_output=True, text=True)
            self.assertNotEqual(invalid.returncode, 0)
            result = json.loads(invalid.stdout)
            self.assertEqual(result["status"], "invalid-receipt")
            self.assertTrue(any("Duplicate JSON key" in message for message in result["errors"]))

    def test_complete_fictional_receipt_passes_mechanical_gate_only(self):
        result = score(REVIEW, receipt(), RUBRIC, CASE)
        self.assertEqual(result["status"], "pass-on-supplied-judgments")
        self.assertIn("Mechanical", result["limits"])

    def test_empty_output_and_empty_receipt_cannot_pass(self):
        for review, record in [("", receipt()), (REVIEW, {})]:
            self.assertEqual(score(review, record, RUBRIC, CASE)["status"], "invalid-receipt")

    def test_missing_dimension_and_assertion_cannot_pass(self):
        for field in ("ratings", "case_assertions"):
            record = receipt()
            if field == "ratings":
                record[field].pop(next(iter(record[field])))
            else:
                record[field].pop()
            self.assertEqual(score(REVIEW, record, RUBRIC, CASE)["status"], "invalid-receipt")

    def test_duplicate_assertions_cannot_substitute_for_coverage(self):
        record = receipt()
        record["case_assertions"][-1] = copy.deepcopy(record["case_assertions"][0])
        self.assertEqual(score(REVIEW, record, RUBRIC, CASE)["status"], "invalid-receipt")

    def test_invalid_scores_hashes_quotes_and_hard_failure_types_are_rejected(self):
        for defect in ("boolean-score", "out-of-range", "hash", "quote", "hard-type"):
            record = receipt()
            first = record["ratings"][next(iter(record["ratings"]))]
            if defect == "boolean-score": first["score"] = True
            elif defect == "out-of-range": first["score"] = 3
            elif defect == "hash": record["review_sha256"] = "wrong"
            elif defect == "quote": first["evidence_quote"] = "absent-source-text"
            else: record["hard_failures"][next(iter(record["hard_failures"]))] = "false"
            with self.subTest(defect=defect):
                self.assertEqual(score(REVIEW, record, RUBRIC, CASE)["status"], "invalid-receipt")

    def test_hard_failure_low_score_and_failed_case_assertion_fail(self):
        for defect in ("hard-failure", "low-score", "case-failure"):
            record = receipt()
            if defect == "hard-failure": record["hard_failures"][next(iter(record["hard_failures"]))] = True
            elif defect == "low-score":
                for value in record["ratings"].values(): value["score"] = 0
            else: record["case_assertions"][0]["satisfied"] = False
            with self.subTest(defect=defect):
                self.assertEqual(score(REVIEW, record, RUBRIC, CASE)["status"], "fail-on-supplied-judgments")


if __name__ == "__main__":
    unittest.main(verbosity=2)
