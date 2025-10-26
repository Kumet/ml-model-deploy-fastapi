.PHONY: install prepare-model lint format test qa serve docker-up docker-down pre-commit hooks mlflow-ui

install:
	uv sync --frozen

prepare-model:
	uv run python models/prepare_model.py

lint:
	uv run ruff check .

format:
	uv run black .

test:
	uv run pytest

qa:
	uv run ruff check .
	uv run black --check .
	uv run pytest

serve:
	uv run uvicorn backend.app.main:app --host 0.0.0.0 --port 8000

docker-up:
	docker compose up --build

docker-down:
	docker compose down

pre-commit:
	uv run pre-commit run --all-files

hooks:
	uv run pre-commit install

mlflow-ui:
	uv run mlflow ui --backend-store-uri $${MLFLOW_TRACKING_URI:-file:mlruns} --host 0.0.0.0 --port 5000
