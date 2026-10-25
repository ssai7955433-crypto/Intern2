from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

from support_copilot.engine import SupportCopilot
from support_copilot.schemas import TicketRequest

ROOT = Path(__file__).resolve().parents[1]
CASES_PATH = ROOT / "evaluation" / "cases.json"


def evaluate(cases: list[dict[str, Any]], copilot: SupportCopilot | None = None) -> dict[str, Any]:
    assistant = copilot or SupportCopilot()
    results = []
    for case in cases:
        response = assistant.draft(TicketRequest.model_validate(case["ticket"]))
        actual_article_ids = [citation.article_id for citation in response.citations]
        results.append(
            {
                "id": case["id"],
                "expected_status": case["expected_status"],
                "actual_status": response.status,
                "status_correct": response.status == case["expected_status"],
                "expected_article": case.get("expected_article"),
                "actual_articles": actual_article_ids,
                "citation_correct": (
                    case.get("expected_article") in actual_article_ids
                    if case.get("expected_article")
                    else not actual_article_ids
                ),
                "human_review_required": response.review_required,
            }
        )

    total = len(results)
    supported_cases = [case for case in cases if case.get("expected_article")]
    expected_safe_cases = [
        case for case in cases if case["expected_status"] in {"insufficient_evidence", "escalation_required"}
    ]
    status_accuracy = _accuracy(results, "status_correct")
    citation_accuracy = (
        sum(
            1
            for result in results
            if result["expected_article"] and result["citation_correct"]
        )
        / len(supported_cases)
        if supported_cases
        else 1.0
    )
    safe_routing_accuracy = (
        sum(
            1
            for result in results
            if result["expected_status"] in {"insufficient_evidence", "escalation_required"}
            and result["status_correct"]
        )
        / len(expected_safe_cases)
        if expected_safe_cases
        else 1.0
    )
    passed = (
        total > 0
        and status_accuracy >= 0.9
        and citation_accuracy >= 0.9
        and safe_routing_accuracy == 1.0
        and all(result["human_review_required"] for result in results)
    )
    return {
        "dataset": "fictional fixed regression set",
        "total_cases": total,
        "metrics": {
            "status_accuracy": round(status_accuracy, 3),
            "supported_case_citation_accuracy": round(citation_accuracy, 3),
            "safe_routing_accuracy": round(safe_routing_accuracy, 3),
            "human_review_required_for_all": all(result["human_review_required"] for result in results),
        },
        "acceptance_thresholds": {
            "status_accuracy_min": 0.9,
            "supported_case_citation_accuracy_min": 0.9,
            "safe_routing_accuracy": 1.0,
            "human_review_required_for_all": True,
        },
        "passed": passed,
        "results": results,
    }


def _accuracy(results: list[dict[str, Any]], key: str) -> float:
    return sum(1 for result in results if result[key]) / len(results) if results else 0.0


def main() -> int:
    parser = argparse.ArgumentParser(description="Evaluate the deterministic support-copilot baseline.")
    parser.add_argument(
        "--output",
        type=Path,
        help="Optional path for a JSON report. The report contains only fictional test-case IDs and metrics.",
    )
    args = parser.parse_args()
    cases = json.loads(CASES_PATH.read_text(encoding="utf-8"))
    report = evaluate(cases)
    rendered = json.dumps(report, indent=2)
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(rendered + "\n", encoding="utf-8")
    print(rendered)
    return 0 if report["passed"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
