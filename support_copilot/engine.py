from __future__ import annotations

import json
import os
import re
import urllib.error
import urllib.request
from pathlib import Path
from typing import Any

from pydantic import BaseModel, ConfigDict, Field, ValidationError

from .prompts import SYSTEM_PROMPT, build_user_prompt
from .schemas import Citation, DraftResponse, TicketRequest

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_KNOWLEDGE_PATH = ROOT / "data" / "knowledge_base.json"
TOKEN_PATTERN = re.compile(r"[a-z0-9]+")
SENSITIVE_PATTERNS = (
    re.compile(r"\b(?:password|passcode)\s*(?:is|:)\s*\S+", re.IGNORECASE),
    re.compile(r"\b(?:one[- ]time|verification|security)\s+code\s*(?:is|:)\s*\d{4,8}\b", re.IGNORECASE),
    re.compile(r"\b(?:\d[ -]*?){13,19}\b"),
    re.compile(r"\b(?:ssn|social security number)\s*(?:is|:)\s*\d{3}[- ]?\d{2}[- ]?\d{4}\b", re.IGNORECASE),
)
ESCALATION_TERMS = {
    "chargeback",
    "fraud",
    "hacked",
    "lawyer",
    "lawsuit",
    "stolen",
    "unauthorized",
}
UNSUPPORTED_PROMISE_PATTERN = re.compile(
    r"\b(?:guarantee|guaranteed|definitely|for sure)\b", re.IGNORECASE
)
STOP_WORDS = {
    "a", "an", "and", "are", "as", "at", "be", "can", "do", "for", "from",
    "how", "i", "in", "is", "it", "me", "my", "of", "on", "or", "the", "to",
    "was", "what", "when", "where", "which", "will", "with", "you", "your",
}


class KnowledgeArticle(BaseModel):
    model_config = ConfigDict(extra="forbid")

    article_id: str
    title: str
    keywords: list[str] = Field(min_length=1)
    approved_facts: list[str] = Field(min_length=1)
    approved_reply: str = Field(min_length=1)


class KnowledgeBase(BaseModel):
    model_config = ConfigDict(extra="forbid")

    articles: list[KnowledgeArticle] = Field(min_length=1)


class GeneratedReply(BaseModel):
    model_config = ConfigDict(extra="forbid")

    reply: str = Field(min_length=1, max_length=5000)


class SupportCopilot:
    def __init__(
        self,
        knowledge_path: Path = DEFAULT_KNOWLEDGE_PATH,
        llm_mode: str | None = None,
        ollama_model: str | None = None,
        ollama_url: str | None = None,
    ) -> None:
        try:
            data = json.loads(knowledge_path.read_text(encoding="utf-8"))
            self.articles = KnowledgeBase.model_validate(data).articles
        except (OSError, json.JSONDecodeError, ValidationError) as exc:
            raise ValueError(f"Could not load approved knowledge at {knowledge_path}: {exc}") from exc

        self.llm_mode = llm_mode or os.getenv("SUPPORT_COPILOT_LLM_MODE", "template")
        self.ollama_model = ollama_model or os.getenv("OLLAMA_MODEL", "llama3.2:latest")
        self.ollama_url = (ollama_url or os.getenv("OLLAMA_URL", "http://127.0.0.1:11434")).rstrip("/")
        if self.llm_mode not in {"template", "ollama"}:
            raise ValueError("SUPPORT_COPILOT_LLM_MODE must be 'template' or 'ollama'")

    def draft(self, ticket: TicketRequest) -> DraftResponse:
        normalized_ticket = " ".join((ticket.subject + " " + ticket.message + " " + ticket.context).split())
        if any(pattern.search(normalized_ticket) for pattern in SENSITIVE_PATTERNS):
            return self._escalation(
                "The message may contain sensitive credentials or personal data. "
                "Please remove it and route the ticket through the approved secure process."
            )

        ticket_tokens = self._tokens(normalized_ticket)
        if ticket_tokens & ESCALATION_TERMS:
            return self._escalation(
                "This issue needs review by a support specialist. No action or outcome has been promised."
            )
        if UNSUPPORTED_PROMISE_PATTERN.search(normalized_ticket):
            return DraftResponse(
                status="insufficient_evidence",
                reply=(
                    "The approved guidance does not support a guarantee. "
                    "Please verify the specific request with a support specialist before replying."
                ),
                citations=[],
                match_score=0,
                quality_flags=["unsupported_commitment_request", "human_review_required"],
                next_step="Verify the requested commitment against an approved source.",
            )

        ranked = sorted(
            (
                (self._score(ticket_tokens, article), article)
                for article in self.articles
            ),
            key=lambda result: result[0],
            reverse=True,
        )
        score, article = ranked[0]
        if score == 0:
            return DraftResponse(
                status="insufficient_evidence",
                reply=(
                    "I could not find an approved knowledge article for this request. "
                    "Please review it and follow up with the customer rather than guessing."
                ),
                citations=[],
                match_score=0,
                quality_flags=["no_matching_approved_source"],
                next_step="Find an approved source or route to a support specialist.",
            )

        citation = Citation(
            article_id=article.article_id,
            title=article.title,
            excerpt=" ".join(article.approved_facts),
        )
        if self.llm_mode == "ollama":
            reply = self._generate_with_ollama(ticket, [article])
        else:
            reply = f"Hi,\n\n{article.approved_reply}\n\nBest,\nCustomer Support"

        return DraftResponse(
            status="supported",
            reply=reply,
            citations=[citation],
            match_score=round(min(score, 1.0), 2),
            quality_flags=["human_review_required", "verify_ticket_specific_details"],
            next_step="Verify the cited guidance and ticket details, then edit or approve the draft.",
        )

    @staticmethod
    def _tokens(text: str) -> set[str]:
        return {token for token in TOKEN_PATTERN.findall(text.lower()) if token not in STOP_WORDS}

    @classmethod
    def _score(cls, ticket_tokens: set[str], article: KnowledgeArticle) -> float:
        article_tokens = cls._tokens(
            " ".join([article.title, *article.keywords, *article.approved_facts])
        )
        if not ticket_tokens or not article_tokens:
            return 0.0
        overlap = ticket_tokens & article_tokens
        return len(overlap) / len(ticket_tokens)

    @staticmethod
    def _escalation(reply: str) -> DraftResponse:
        return DraftResponse(
            status="escalation_required",
            reply=reply,
            citations=[],
            match_score=0,
            quality_flags=["safety_escalation", "human_review_required"],
            next_step="Escalate to a trained support specialist; do not send this draft automatically.",
        )

    def _generate_with_ollama(
        self, ticket: TicketRequest, articles: list[KnowledgeArticle]
    ) -> str:
        excerpts = [
            f"{article.title} ({article.article_id}): "
            + " ".join(article.approved_facts)
            for article in articles
        ]
        body: dict[str, Any] = {
            "model": self.ollama_model,
            "system": SYSTEM_PROMPT,
            "prompt": build_user_prompt(ticket, excerpts),
            "format": {
                "type": "object",
                "properties": {"reply": {"type": "string"}},
                "required": ["reply"],
                "additionalProperties": False,
            },
            "stream": False,
        }
        request = urllib.request.Request(
            f"{self.ollama_url}/api/generate",
            data=json.dumps(body).encode("utf-8"),
            headers={"Content-Type": "application/json"},
            method="POST",
        )
        try:
            with urllib.request.urlopen(request, timeout=60) as response:
                payload = json.loads(response.read().decode("utf-8"))
            model_output = json.loads(payload["response"])
            return GeneratedReply.model_validate(model_output).reply
        except (urllib.error.URLError, TimeoutError, KeyError, json.JSONDecodeError, ValidationError) as exc:
            raise RuntimeError(f"Ollama draft generation failed: {exc}") from exc
