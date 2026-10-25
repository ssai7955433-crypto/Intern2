# Problem definition and requirements

## Stakeholder and decision

- **Primary user:** customer-support agent who reviews and sends replies.
- **Business stakeholder:** support-team lead responsible for response quality and safe handling.
- **Decision enabled:** whether an evidence-backed draft is safe to edit/approve, needs more information, or must be escalated.
- **Intended benefit:** reduce time spent locating approved guidance while making source evidence and uncertainty visible. This prototype makes no measured productivity claim.

## Scope and boundaries

The prototype accepts a ticket subject, customer message, and optional non-sensitive context. It searches a small, fictional, approved knowledge base and returns one of three outcomes: a cited draft, an abstention, or a safety escalation. Every draft requires human review.

It does not connect to customer accounts, send messages, grant refunds, change orders, authenticate agents, store tickets/reviews, ingest arbitrary knowledge documents, or make binding policy decisions. Use fictional demo data only.

## Inputs and outputs

| Area | Definition |
|---|---|
| Input | Subject (optional, up to 200 characters), message (1–4,000 characters), context (optional, up to 2,000 characters) |
| Output | Validated status, editable reply, approved-article citation(s), heuristic knowledge match score, quality flags, and next step |
| Human control | Agent edits the reply and marks approved, needs edit, or escalated; no message is sent |
| Privacy | Requests are processed in memory; review action is acknowledged but not persisted; no analytics or customer data logging |
| LLM | Deterministic template mode by default; optional local Ollama generation, with prompt and JSON validation |

## Success measures

The fixed regression suite passes when:

1. Status classification accuracy is at least 90%.
2. Correct article citation accuracy among supported cases is at least 90%.
3. Safe routing accuracy for abstention/escalation cases is 100%.
4. Human review remains required on every case.

These are prototype regression thresholds on a small synthetic dataset, not estimates of production accuracy, customer satisfaction, or time saved.

## Edge cases and constraints

- Empty or oversize fields and unrecognized request properties are rejected by the API schema.
- No matching approved article results in abstention rather than invented policy.
- Dispute/fraud terms and detected credential/payment data trigger escalation.
- Customer-provided instructions are treated as untrusted content.
- Knowledge snippets may be incomplete or lexically mismatched; a human must verify the match and the customer's details.
- Optional LLM mode depends on a running local Ollama service and a locally installed model. Provider errors are visible as HTTP 503.
