# Bounded UX review comparison

The existing cases and weighted rubric are authoring inputs, not completed
method evaluations. `tests/score_review.py` supplies a mechanical gate for
separately adjudicated records. It requires a nonempty hashed review, all six
rubric dimensions, every selected case assertion, explicit hard-failure
judgments and source quotations. Empty or partial output cannot pass.

Run the exposed software controls in an environment that already has PyYAML:

```sh
python3 -m unittest discover -s tests -p test_score_review.py
python3 tests/score_review.py review.txt judgments.json
```

Judgment format: `ux-adjudication/v1`, `review_sha256`, a case ID from
`tests/benchmark-cases.yaml`, adjudicator identifier, exact `hard_failures`
boolean map, exact `ratings` map (`score` 0/1/2 and `evidence_quote` per
dimension), and `case_assertions` (`index`, `satisfied`, `evidence_quote` for
each expected assertion). The test fixture is fictional and exposed.

The gate binds judgment coverage and arithmetic to supplied bytes. It does not
authenticate the judge, decide whether a quotation entails a judgment, or show
that the method improves usability. Keep semantic adjudication and disagreement
records separate; a mechanically valid but incorrect judgment is still wrong.

For an actual comparison, freeze a real authorized task/state packet, baseline
workflow, assistance, versions, time/cost budget and meaningful improvement
criterion before running either arm. Include an evidence-free redesign trap,
a workflow that should remain unchanged, interrupted recovery and user-stop
cases. Use blinded independent review and untouched confirmation tasks;
these exposed software controls are not blind held-outs.

Let the person attempt first and choose one bounded change with a keep/revert
reason. Use at most two rounds, and stop on completion, no meaningful movement,
regression, missing evidence/resources or user exit. Do not infer growth or an
accessibility-conformance result. No outcome comparison has been run by adding
this gate; no paid provider calls are required for its software controls.
