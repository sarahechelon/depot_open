.PHONY: test lint run export-openapi

test:
	uv run pytest

lint:
	uv run ruff check .
	uv run ruff format --check .

run:
	uv run uvicorn app.main:app --reload

export-openapi:
	uv run python scripts/export_openapi.py
