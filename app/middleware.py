"""Request tracing: propagate or generate a request ID for every request.

The ID is echoed back in X-Request-ID and bound to structlog's context so
every log line for that request can be correlated.
"""

import uuid
from collections.abc import Awaitable, Callable

import structlog.contextvars
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import Response

REQUEST_ID_HEADER = "X-Request-ID"


class RequestIDMiddleware(BaseHTTPMiddleware):
    async def dispatch(
        self, request: Request, call_next: Callable[[Request], Awaitable[Response]]
    ) -> Response:
        request_id = request.headers.get(REQUEST_ID_HEADER) or str(uuid.uuid4())
        structlog.contextvars.bind_contextvars(request_id=request_id)
        try:
            response = await call_next(request)
            response.headers[REQUEST_ID_HEADER] = request_id
            return response
        finally:
            structlog.contextvars.unbind_contextvars("request_id")


def new_request_id() -> str:
    return str(uuid.uuid4())
