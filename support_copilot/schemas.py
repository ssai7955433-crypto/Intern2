from __future__ import annotations

from typing import Literal

from pydantic import BaseModel, ConfigDict, Field


class TicketRequest(BaseModel):
    model_config = ConfigDict(extra="forbid", str_strip_whitespace=True)

    subject: str = Field(default="", max_length=200)
    message: str = Field(min_length=1, max_length=4000)
    context: str = Field(default="", max_length=2000)


class Citation(BaseModel):
    article_id: str
    title: str
    excerpt: str


class DraftResponse(BaseModel):
    status: Literal["supported", "insufficient_evidence", "escalation_required"]
    reply: str
    citations: list[Citation]
    match_score: float = Field(ge=0, le=1)
    review_required: Literal[True] = True
    quality_flags: list[str]
    next_step: str


class ReviewRequest(BaseModel):
    model_config = ConfigDict(extra="forbid", str_strip_whitespace=True)

    decision: Literal["approved", "needs_edit", "escalated"]
    reviewed_reply: str = Field(min_length=1, max_length=5000)


class ReviewResponse(BaseModel):
    decision: Literal["approved", "needs_edit", "escalated"]
    message: str
    saved: Literal[False] = False
