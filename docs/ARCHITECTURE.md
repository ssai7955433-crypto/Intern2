# Architecture

## Request flow

1. FastAPI validates a bounded ticket request with Pydantic.
2. The safety gate detects likely exposed credentials/payment data and dispute/fraud escalation terms.
3. A transparent lexical matcher ranks fictional approved knowledge articles.
4. No overlap produces a structured `insufficient_evidence` result with no citations.
5. A supported match produces a template-based reply by default. Optional Ollama mode passes only the ticket and retrieved approved facts to a constrained JSON prompt; the response is schema-validated.
6. The result includes a citation created by the application from the selected article, never a citation invented by the model.
7. The web UI displays status, evidence, and an editable reply. The agent explicitly chooses approve, edit, or escalate.

## Components

- `support_copilot/schemas.py`: input/output contracts and validation.
- `support_copilot/engine.py`: knowledge loading, safety routing, lexical retrieval, deterministic reply, and optional local generation.
- `support_copilot/prompts.py`: system prompt and user-context builder.
- `support_copilot/api.py`: health, browser demo, draft, and stateless review endpoints.
- `data/knowledge_base.json`: fictional approved articles.
- `evaluation/`: fixed cases and deterministic metrics.
- `web/index.html`: accessible single-page agent demonstration.

## Model and retrieval decisions

The default mode is deterministic so a mentor can run the app without an API key or network connection. It is a controlled baseline, not a claim that templates are equivalent to a language model. Setting `SUPPORT_COPILOT_LLM_MODE=ollama` enables an optional local model. In both modes, the evidence is application-selected and review is mandatory.

The lexical matcher favors transparency and zero extra embedding/model dependencies for this small demo. It is vulnerable to paraphrases and should be replaced or augmented only after measured evaluation on approved, representative data.

## Privacy and review evidence

The app does not write ticket text, draft text, or decisions to disk. Evaluation output contains synthetic case IDs and metrics only. A production audit trail would need an approved retention policy, access control, redaction, and an explicit storage design; none is implied here.
