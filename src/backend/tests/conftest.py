import os
from pathlib import Path

import pytest
from fastapi.testclient import TestClient

from backend.app.main import app


@pytest.fixture(scope="session", autouse=True)
def _ensure_model():
    os.environ.setdefault("MODEL_PATH", "models/model.joblib")
    os.environ.setdefault("API_USERNAME", "admin")
    os.environ.setdefault("API_PASSWORD", "changeme")
    os.environ.setdefault("JWT_SECRET", "test-secret")
    os.environ.setdefault("JWT_ALGORITHM", "HS256")
    os.environ.setdefault("JWT_EXPIRE_MINUTES", "30")
    os.environ.setdefault("LOG_LEVEL", "INFO")
    path = Path(os.environ["MODEL_PATH"])
    if not path.exists():
        from models.prepare_model import main as prepare_model

        prepare_model()
    yield


@pytest.fixture()
def client():
    return TestClient(app)


@pytest.fixture()
def auth_headers(client: TestClient):
    response = client.post(
        "/auth/token",
        json={"username": "admin", "password": "changeme"},
    )
    token = response.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}
