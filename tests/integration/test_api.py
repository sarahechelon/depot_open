"""Integration test: boots the real ASGI app in a worker thread and exercises it
over actual HTTP, end to end (not via the in-process TestClient)."""

import socket
import threading
from collections.abc import Iterator

import httpx
import pytest
import uvicorn

from app.main import app


def _free_port() -> int:
    with socket.socket() as s:
        s.bind(("127.0.0.1", 0))
        port = int(s.getsockname()[1])
    return port


@pytest.fixture(scope="module")
def base_url() -> Iterator[str]:
    port = _free_port()
    config = uvicorn.Config(app, host="127.0.0.1", port=port, log_level="error")
    server = uvicorn.Server(config)
    thread = threading.Thread(target=server.run, daemon=True)
    thread.start()
    url = f"http://127.0.0.1:{port}"
    _wait_until_serving(url)
    yield url
    server.should_exit = True
    thread.join(timeout=5)


def _wait_until_serving(url: str, attempts: int = 100) -> None:
    """Retry real HTTP requests until uvicorn answers (xdist-safe startup wait)."""
    last_error: Exception | None = None
    for _ in range(attempts):
        try:
            httpx.get(f"{url}/health", timeout=1.0)
            return
        except httpx.HTTPError as exc:
            last_error = exc
    raise RuntimeError(f"server at {url} never became ready") from last_error


def test_health_over_real_http(base_url: str) -> None:
    response = httpx.get(f"{base_url}/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_openapi_schema_served(base_url: str) -> None:
    response = httpx.get(f"{base_url}/openapi.json")
    assert response.status_code == 200
    assert "/health" in response.json()["paths"]
