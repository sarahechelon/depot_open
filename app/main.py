import os
from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

import sentry_sdk
from fastapi import FastAPI, Response
from prometheus_client import CONTENT_TYPE_LATEST, REGISTRY, generate_latest

from app.log import configure_logging
from app.middleware import RequestIDMiddleware
from app.routers import health


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncIterator[None]:
    configure_logging()
    dsn = os.getenv("SENTRY_DSN")
    if dsn:
        sentry_sdk.init(dsn=dsn, traces_sample_rate=0.2)
    yield


def create_app() -> FastAPI:
    app = FastAPI(title="Depot", description="Internal inventory and orders service.")
    app.include_router(health.router)
    app.add_middleware(RequestIDMiddleware)

    @app.get("/metrics", tags=["health"], include_in_schema=False)
    def get_metrics() -> Response:
        """Prometheus-format metrics for scrape targets."""
        return Response(content=generate_latest(REGISTRY), media_type=CONTENT_TYPE_LATEST)

    return app


app = create_app()
