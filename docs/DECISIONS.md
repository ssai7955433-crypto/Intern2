# Decision log

| Decision | Rationale | Trade-off |
|---|---|---|
| Use FastAPI, Pydantic, and a browser UI | Simple typed API plus a demo interface that a mentor can run locally | No production identity or ticket-system integration |
| Default to deterministic, local templates | Repeatable demo and evaluation without secrets, paid APIs, or model downloads | Less natural phrasing and limited response flexibility |
| Offer optional Ollama mode | Demonstrates a real local LLM prompt while keeping external data transfer off by default | Requires a running local model; generated claims still need human review |
| Return source citations from application retrieval | Prevents model-created source identifiers and enables visible evidence checks | Citation presence does not prove semantic entailment |
| No persistence or automatic send | Minimizes privacy risk and preserves agent control | No durable audit history or direct productivity measurement |
| Keep fictional knowledge and ticket cases | Safe, reproducible demonstration | Results do not generalize to a real support organization |
