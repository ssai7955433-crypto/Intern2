# Evaluation guide

## Reproduce

```powershell
python -m pytest
python -m evaluation.run_eval --output evaluation/results/latest.json
```

The evaluator uses `evaluation/cases.json` and deterministic template mode. An optional generated report contains synthetic case IDs, expected/actual categories, citations, and aggregate scores; it contains no customer data. Reports written under `evaluation/results/` are ignored by Git.

The committed [reference report](../evaluation/reference_results.json) is the reproducible baseline captured for this submission.

## Metrics and acceptance thresholds

| Metric | Definition | Threshold |
|---|---|---:|
| Status accuracy | Fraction of all cases whose output status matches the expected status | ≥ 0.90 |
| Supported-case citation accuracy | Supported cases citing the expected article | ≥ 0.90 |
| Safe-routing accuracy | Expected abstention/escalation cases receiving the exact expected status | 1.00 |
| Human review | Every case requires human review | 1.00 |

The evaluator exits with status 1 when thresholds are not met. The test suite also checks API validation, user-controlled review, sensitive-input handling, prompt injection resistance in template mode, and explicit Ollama failure behavior.

## Evidence interpretation

This is a small regression check for the synthetic baseline, not a benchmark and not evidence of production readiness. The fixed cases are authored alongside the demo policy articles, so they may overstate performance. LLM mode is excluded from the deterministic score because generation varies; any model change needs an independently reviewed evaluation set and human factuality review.
