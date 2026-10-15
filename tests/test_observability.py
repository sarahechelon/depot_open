"""Tests for structured logging, request-ID tracing, and metrics."""

from fastapi.testclient import TestClient

from app.log import scrub_sensitive


def test_request_id_is_generated_and_echoed(client: TestClient) -> None:
    response = client.get("/health")
    assert response.status_code == 200
    assert len(response.headers["X-Request-ID"]) == 36


def test_request_id_is_propagated(client: TestClient) -> None:
    response = client.get("/health", headers={"X-Request-ID": "trace-123"})
    assert response.headers["X-Request-ID"] == "trace-123"


def test_metrics_endpoint(client: TestClient) -> None:
    response = client.get("/metrics")
    assert response.status_code == 200
    assert "python_gc_" in response.text


def test_scrub_masks_sensitive_keys() -> None:
    event = scrub_sensitive(
        None, "info", {"email": "a@b.c", "password": "hunter2", "order_id": "1"}
    )
    assert event["password"] == "[REDACTED]"
    assert event["email"] == "a@b.c"
    assert event["order_id"] == "1"
