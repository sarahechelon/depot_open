# AGENTS.md

Conventions for the Depot API (see `docs/SPEC.md` for the full product spec).
Follow these in every session and every PR.

## Stack

Python 3.12, FastAPI, Pydantic v2, SQLAlchemy 2.0, Alembic, pytest + httpx,
ruff, uv. SQLite in development, PostgreSQL in production. Docker for local
infra, GitHub Actions for CI. One story per PR, worked in backlog order.

## Layout

- `app/routers/` — one file per resource.
- `app/services/` — all business logic. Services must **never** import
  FastAPI (or anything HTTP-specific); they take and return plain data.
- `app/models/` and `app/schemas/` — mirror each other: one model per
  resource, one schema module per model.

## Rules

- Every schema change ships with an Alembic migration in the same PR.
- Every router has a matching test module.
- Existing tests are never deleted or rewritten to make new code pass.
- `make test`, `make lint`, and `make run` must always work. Run them
  before finishing any change.
