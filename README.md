# Depot

Internal inventory and orders service for a small retailer. Staff manage products,
suppliers and stock; customer orders reserve stock; downstream systems are notified
by webhook. See `docs/SPEC.md` for the product spec and `AGENTS.md` for the
conventions all contributors (human and AI) follow.

## Setup

Requires [uv](https://docs.astral.sh/uv/) and Python 3.12+.

```sh
uv sync                 # create .venv and install pinned deps (uv.lock)
uv run pre-commit install   # optional: ruff, mypy, guard checks on every commit
```

## Development

| Command | What it does |
| --- | --- |
| `make run` | Start the dev server on http://127.0.0.1:8000 with auto-reload |
| `make test` | Run the test suite (parallel, with coverage gate and timing) |
| `make lint` | ruff check + format check |

Interactive API docs (auto-generated OpenAPI/Swagger) are served at
`/docs` and `/openapi.json` while the server runs.

## Interactive QA

From a fresh clone to a live endpoint:

```sh
uv sync
make run            # starts uvicorn on http://127.0.0.1:8000
curl -i http://127.0.0.1:8000/health   # expect 200 {"status":"ok"}
```

There is no auth gate and no external service required locally: the dev database
is SQLite (`DEPOT_DATABASE_URL` defaults to `sqlite:///./depot.db`). Copy
`.env.example` to `.env` to change settings.

## Environment variables

All documented in `.env.example`: `DEPOT_DATABASE_URL` (connection string),
`SENTRY_DSN` (optional error reporting), `DEPOT_FLAG_*` (optional feature flags).

## Architecture

See `docs/architecture.md` for the component diagram and service dependencies.

## Operations

Incident response lives in `docs/runbooks/incident-response.md`. Deploy impact is
monitored via the `/metrics` Prometheus endpoint and the health check at
`/health`; releases are published by the [release-please](.github/workflows/release-please.yml) workflow.

## Contributing

Branch off `master`, one backlog story per PR. CI must pass: lint, strict typing,
tests with coverage gate, and the repo guard scripts (file size, TODO policy).
Follow the issue labels in `docs/labels.md` and the PR template.
