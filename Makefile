.PHONY: test lint run export-openapi

test:
	uv run pytest -n auto --cov=app --cov-report=term-missing --cov-fail-under=85

lint:
	uv run ruff check .
	uv run ruff format --check .

run:
	uv run uvicorn app.main:app --reload

export-openapi:
	uv run python scripts/export_openapi.py
