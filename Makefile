.PHONY: test lint run

test:
	uv run pytest

lint:
	uv run ruff check .
	uv run ruff format --check .

run:
	uv run uvicorn app.main:app --reload
