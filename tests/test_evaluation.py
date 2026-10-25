import json
from pathlib import Path

from evaluation.run_eval import evaluate
from support_copilot.engine import SupportCopilot

ROOT = Path(__file__).resolve().parents[1]


def test_fixed_evaluation_set_meets_acceptance_thresholds() -> None:
    cases = json.loads((ROOT / "evaluation" / "cases.json").read_text(encoding="utf-8"))
    report = evaluate(cases, SupportCopilot(knowledge_path=ROOT / "data" / "knowledge_base.json"))

    assert report["passed"] is True
    assert report["total_cases"] == 10
    assert report["metrics"]["status_accuracy"] >= 0.9
    assert report["metrics"]["supported_case_citation_accuracy"] >= 0.9
    assert report["metrics"]["safe_routing_accuracy"] == 1.0
