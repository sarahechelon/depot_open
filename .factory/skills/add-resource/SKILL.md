---
name: add-resource
description: Add a new HTTP resource (product, order, return...) to the Depot API following the repo's router/service/model/schema conventions.
---

# Add a resource to Depot

Follow these steps in order. Every step is required for a complete PR.

1. **Model** — create `app/models/<resource>.py` with a SQLAlchemy 2.0 model.
2. **Migration** — generate `uv run alembic revision --autogenerate -m "add <resource>"`;
   review it and fix SQLite/Postgres compatibility (e.g. no JSONB in SQLite).
3. **Schemas** — create `app/schemas/<resource>.py` mirroring the model:
   `<Resource>Create`, `<Resource>Read` at minimum.
4. **Service** — put business logic in `app/services/<resource>.py`.
   Services must NOT import FastAPI; take/return plain data or Pydantic models.
5. **Router** — create `app/routers/<resource>.py` with `router = APIRouter(...)`,
   then include it in `create_app()` in `app/main.py`.
6. **Tests** — create `tests/test_<resource>.py` with TestClient tests covering
   happy path, validation errors, and conflict cases (e.g. duplicate SKU → 409).
   Never delete or rewrite existing tests to make new code pass.
7. **Verify** — `make lint && make test` must pass, then
   `make run` and `curl -i http://127.0.0.1:8000/<resource>s` for a smoke check.
8. **Docs** — run `make export-openapi` and commit the updated `openapi.json`.
