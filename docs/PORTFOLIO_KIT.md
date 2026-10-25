# Portfolio kit

Use these descriptions as a starting point. Keep the distinction between synthetic regression results and measured production outcomes clear.

## Resume entry

**AI Customer Support Copilot — Python, FastAPI, Pydantic**

- Built a review-first support-reply prototype that retrieves fictional approved guidance, cites its source, abstains on unsupported questions, and routes sensitive/dispute cases to a human.
- Added structured API validation, a constrained optional local-Ollama prompt, a browser-based agent review flow, and a reproducible synthetic evaluation suite.
- Evaluated 10 fixed synthetic cases: 100% status accuracy, 100% expected-source citation accuracy on supported cases, and 100% safe-routing accuracy; results are a small regression check, not production performance.

## LinkedIn post draft

I built an **AI Customer Support Copilot** as an internship project: a support-reply drafting workflow that uses approved knowledge, shows its source, abstains when evidence is missing, and keeps a human agent in control.

The prototype includes typed API contracts, safety routing for selected sensitive/dispute cases, an editable review UI, and an optional local LLM mode. On a fixed set of 10 fictional regression cases, it achieved 100% status accuracy, 100% citation accuracy for supported cases, and 100% safe-routing accuracy.

Those numbers describe only a small synthetic test set—not customer outcomes or measured time savings. My main takeaway: a useful copilot needs visible evidence, clear uncertainty, and an explicit review step, not just fluent text.

Next I would validate against a larger privacy-reviewed dataset with human quality review before considering any real support workflow.

## Interview story (problem → action → evidence → result)

- **Problem:** Agents can spend time searching for standard guidance, while unsupported promises create service and trust risks.
- **Action:** I separated request validation, safety routing, retrieval, draft generation, and agent review. I chose deterministic templates as the reproducible baseline and left local LLM generation optional.
- **Evidence:** The fixed 10-case synthetic suite passed its status, citation, and safe-routing thresholds. API tests cover invalid fields, prompt-injection-like ticket text, sensitive input, and model-service failure.
- **Result:** A mentor can run the demo locally, inspect the article used, edit the draft, and record a stateless review choice. I make no claim of real-world accuracy or productivity without a representative pilot.

## Questions to be ready for

- **Why not auto-send?** The prototype cannot verify every ticket-specific claim or semantic entailment, so a trained person must own the customer-facing decision.
- **What is the biggest trade-off?** Lexical retrieval and templates are explainable and repeatable but weak on paraphrase coverage and natural personalization.
- **How would you scale it?** Add authenticated integration, approved/versioned knowledge, privacy controls, measured retrieval and hallucination evaluation, monitoring, and a human-reviewed pilot before increasing traffic.
