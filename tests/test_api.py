from fastapi.testclient import TestClient

from support_copilot.api import app

client = TestClient(app)


def test_health_and_demo_page() -> None:
    assert client.get("/health").json() == {"status": "ok"}
    page = client.get("/")
    assert page.status_code == 200
    assert "Support Copilot" in page.text
    assert 'fetch("/draft"' in page.text


def test_draft_api_validates_input_and_returns_structured_response() -> None:
    response = client.post("/draft", json={"message": "How do I return an unused item?"})

    assert response.status_code == 200
    body = response.json()
    assert body["status"] == "supported"
    assert body["review_required"] is True
    assert body["citations"][0]["article_id"] == "returns"


def test_unknown_request_fields_are_rejected() -> None:
    response = client.post("/draft", json={"message": "Need help", "customer_email": "demo@example.test"})

    assert response.status_code == 422


def test_review_action_is_stateless_and_explicit() -> None:
    response = client.post(
        "/review",
        json={"decision": "approved", "reviewed_reply": "Reviewed fictional reply."},
    )

    assert response.status_code == 200
    assert response.json()["decision"] == "approved"
    assert response.json()["saved"] is False
    assert "not stored" in response.json()["message"]


def test_ollama_failure_is_reported_as_service_unavailable(monkeypatch) -> None:
    import support_copilot.api as api_module
    from support_copilot.engine import SupportCopilot

    monkeypatch.setattr(
        api_module,
        "copilot",
        SupportCopilot(llm_mode="ollama", ollama_url="http://127.0.0.1:1"),
    )
    response = client.post("/draft", json={"message": "Where can I track my shipment?"})

    assert response.status_code == 503
    assert "Ollama draft generation failed" in response.json()["detail"]
