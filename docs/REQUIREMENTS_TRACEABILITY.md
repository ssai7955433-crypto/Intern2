# Requirements-to-evidence map

| Requirement | Implementation / evidence |
|---|---|
| Stakeholder, decision, scope, measures | `docs/REQUIREMENTS.md` |
| Prompt/system design | `support_copilot/prompts.py`; `docs/ARCHITECTURE.md` |
| Grounded approved source | `data/knowledge_base.json`; `support_copilot/engine.py`; citation tests |
| Structured output validation | Pydantic models in `support_copilot/schemas.py`; API tests |
| Human review | Browser UI and `/review`; stateless review test |
| Evaluation set and measurable checks | `evaluation/cases.json`, `evaluation/run_eval.py`, `tests/test_evaluation.py` |
| Safety and hallucination controls | Escalation, abstention, prompt boundaries, and limits in `docs/SAFETY_AND_PRIVACY.md` |
| Exceptions and uncertainty | Validation errors, no-evidence response, optional provider error surfaced as HTTP 503 |
| Repeatability and demo | `README.md`, `docs/DEMO_SCRIPT.md`, `docs/EVALUATION.md` |
| Limitations and improvement roadmap | `docs/SAFETY_AND_PRIVACY.md`, `docs/FINAL_PRESENTATION.md` |
