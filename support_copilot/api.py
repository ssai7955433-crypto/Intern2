from pathlib import Path

from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse

from .engine import SupportCopilot
from .schemas import DraftResponse, ReviewRequest, ReviewResponse, TicketRequest

app = FastAPI(
    title="AI Customer Support Copilot",
    description="Grounded support-reply drafts for human review. Demo data only.",
    version="1.0.0",
)
copilot = SupportCopilot()
WEB_ROOT = Path(__file__).resolve().parents[1] / "web"


@app.get("/", include_in_schema=False)
def home() -> FileResponse:
    return FileResponse(WEB_ROOT / "index.html")


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


@app.post("/draft", response_model=DraftResponse)
def create_draft(ticket: TicketRequest) -> DraftResponse:
    try:
        return copilot.draft(ticket)
    except RuntimeError as exc:
        raise HTTPException(status_code=503, detail=str(exc)) from exc


@app.post("/review", response_model=ReviewResponse)
def record_review(review: ReviewRequest) -> ReviewResponse:
    messages = {
        "approved": "Draft marked approved for the agent's workflow. Ticket data is not stored.",
        "needs_edit": "Draft marked for editing. Ticket data is not stored.",
        "escalated": "Ticket marked for specialist escalation. Ticket data is not stored.",
    }
    return ReviewResponse(decision=review.decision, message=messages[review.decision])
