import os
from pathlib import Path

import pytest
from fastapi.testclient import TestClient

from backend.app.main import app


@pytest.fixture(scope="session", autouse=True)
def _ensure_model():
    os.environ.setdefault("MODEL_PATH", "models/model.joblib")
    path = Path(os.environ["MODEL_PATH"])
    if not path.exists():
        from models.prepare_model import main as prepare_model

        prepare_model()
    yield


@pytest.fixture()
def client():
    return TestClient(app)
