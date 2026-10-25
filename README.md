# AI Customer Support Copilot

A review-first support assistant that drafts replies from a fictional approved knowledge base, cites the source it used, abstains when evidence is missing, and routes sensitive or dispute-related tickets for a human. It never sends or stores a reply.

> **Demo only:** use fictional ticket data. The included policies and evaluation cases are invented and are not real company policy.

## Project overview

| | |
|---|---|
| Primary user | Customer-support agent |
| Stakeholder decision | Edit/approve a cited draft, gather more information, or escalate |
| Default stack | Python 3.10+, FastAPI, Pydantic, plain HTML/JavaScript |
| Default generation | Deterministic, reproducible local template |
| Optional LLM | Local Ollama model; no external LLM API |
| Privacy posture | No ticket/review persistence; no automatic sending |

## Quick start (Windows PowerShell)

```powershell
py -3 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
python -m uvicorn support_copilot.api:app --reload
```

Open <http://127.0.0.1:8000/>. Interactive API docs are at <http://127.0.0.1:8000/docs>.

The default template mode needs no API key or model download.

## Optional local Ollama generation

Install and start [Ollama](https://ollama.com/download), then select a model shown by `ollama list`:

```powershell
ollama list
$env:SUPPORT_COPILOT_LLM_MODE = "ollama"
$env:OLLAMA_MODEL = "llama3.2:latest"
python -m uvicorn support_copilot.api:app --reload
```

On this machine, Ollama 0.40.10 has `llama3.2:latest` installed (also listed as `llama3.2:3b`). Optional settings: `OLLAMA_URL` (default `http://127.0.0.1:11434`) and `OLLAMA_MODEL` (default `llama3.2:latest`). Provider errors are returned as HTTP 503. The LLM prompt requests a constrained JSON reply; malformed output is rejected. A human must still check every generated claim against the cited evidence.

## Example API request

```powershell
Invoke-RestMethod -Method Post `
  -Uri http://127.0.0.1:8000/draft `
  -ContentType "application/json" `
  -Body '{"subject":"Tracking question","message":"Where can I track my delayed shipment?"}'
```

The response includes `status`, `reply`, `citations`, `match_score` (a lexical heuristic, not a probability), `review_required`, `quality_flags`, and `next_step`. `/review` accepts `approved`, `needs_edit`, or `escalated` and explicitly does not persist the submitted reply.

## Tests and evaluation

```powershell
python -m pytest
python -m evaluation.run_eval
```

To save a synthetic-data-only JSON report:

```powershell
python -m evaluation.run_eval --output evaluation/results/latest.json
```

The baseline acceptance thresholds and what the small synthetic evaluation does (and does not) demonstrate are documented in [Evaluation](docs/EVALUATION.md).
The committed [reference evaluation report](evaluation/reference_results.json) records the current fixed-set run.

## Deliverables and project guide

- [Requirements and success criteria](docs/REQUIREMENTS.md)
- [Requirements traceability](docs/REQUIREMENTS_TRACEABILITY.md)
- [Architecture](docs/ARCHITECTURE.md) and [decision log](docs/DECISIONS.md)
- [Safety, privacy, limitations, and roadmap](docs/SAFETY_AND_PRIVACY.md)
- [Evaluation guide](docs/EVALUATION.md) and `evaluation/cases.json`
- [Mentor demo script](docs/DEMO_SCRIPT.md)
- [Final presentation outline](docs/FINAL_PRESENTATION.md)
- [Resume, LinkedIn, and interview portfolio kit](docs/PORTFOLIO_KIT.md)

## Known limitations

The corpus and cases are fictional and small; lexical search may miss paraphrases. Safety detection is pattern-based. Citations show which article was retrieved but do not prove that every sentence is entailed. The optional model can hallucinate. This prototype has no authentication, ticket-system integration, durable audit log, monitoring, or production security controls. See [Safety and privacy](docs/SAFETY_AND_PRIVACY.md) before adapting it for real use.
