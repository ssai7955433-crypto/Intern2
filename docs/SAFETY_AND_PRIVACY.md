# Safety, privacy, and limitations

## Controls in this prototype

- Use fictional data only. Do not paste real customer information.
- Ticket input is length-bounded and rejects unexpected fields.
- Prompt text treats customer content as untrusted; it may not override system instructions.
- Sensitive-credential/payment patterns and selected dispute terms are routed for human escalation before drafting.
- Unsupported questions abstain rather than inventing a policy.
- Citations come only from the local approved demo corpus.
- Every response says that human review is required. The UI never sends a customer reply.
- Ollama is optional and local; no external model API is configured.
- Ticket, draft, and review text are not persisted. The review endpoint only acknowledges a decision.
- API errors in optional generation are reported as service-unavailable responses, not disguised as successful drafts.

## Known limitations

- Synthetic knowledge and evaluation data cannot establish real-world safety or accuracy.
- Keyword retrieval and pattern-based safety checks can miss paraphrases, ambiguous intent, and obfuscated sensitive data.
- The optional model can introduce unsupported phrasing even when given approved excerpts. Schema validation and citation membership do not prove factual entailment; the agent must compare every claim with cited evidence.
- No authentication, authorization, rate limiting, monitoring, data-retention controls, or multi-agent workflow is implemented.
- UI review decisions are not stored, so this is not a production audit mechanism.

## Responsible next steps before production

1. Obtain policy and privacy approval; replace demo content with versioned, owner-approved articles.
2. Create a privacy-reviewed, de-identified test set representing real ticket categories and adversarial inputs.
3. Add agent authentication/authorization, secure deployment, rate limiting, secrets management, and security testing.
4. Add a privacy-approved decision log with access control, retention/deletion, and redaction.
5. Evaluate hallucination, citation entailment, escalation recall, latency, and agent edit/approval rates with human reviewers.
6. Pilot with a small agent group; measure handling time and quality against a documented baseline before making productivity claims.
