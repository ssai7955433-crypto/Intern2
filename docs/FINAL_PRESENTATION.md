# Project 2 — AI Customer Support Copilot

## Problem

Support agents need to answer repeat questions quickly without making unsupported commitments. The copilot finds approved guidance, prepares an editable draft, and makes evidence and uncertainty visible.

## User and decision

- **User:** customer-support agent.
- **Decision:** review and edit/approve a cited reply, seek more evidence, or escalate.

## Solution

A Python/FastAPI application uses structured schemas, a fictional approved knowledge base, transparent local retrieval, safety routing, and an optional local Ollama generator. The interface requires an agent decision; no reply is sent or persisted.

## Validation

The fixed synthetic evaluation covers supported tickets, unsupported requests, privacy-sensitive input, and payment disputes. Acceptance requires at least 90% status accuracy, at least 90% citation accuracy on supported examples, 100% safe routing, and human review on every case. Run `python -m evaluation.run_eval` to reproduce.

## Trade-offs and limitations

Deterministic templates make the demo reproducible but less flexible. Lexical matching is easy to explain but weak on paraphrases. Optional LLM output can still be wrong; schema checking and citations cannot prove factual entailment. The synthetic set does not establish real-world performance or productivity.

## Future work

Replace demo policies only with approved, versioned knowledge; evaluate on privacy-reviewed representative cases; add authentication and a privacy-approved audit trail; and run a measured agent pilot before scaling.
