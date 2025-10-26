from __future__ import annotations

from pathlib import Path
from typing import Any

import joblib

from .config import settings

_MODEL: Any | None = None
_META: dict[str, str] = {}


def load_model(force: bool = False):
    global _MODEL, _META
    if _MODEL is not None and not force:
        return _MODEL

    path = Path(settings.model_path)
    if not path.exists():
        raise FileNotFoundError(f"モデルファイルが見つかりません: {path}")

    _MODEL = joblib.load(path)
    _META = {
        "name": settings.model_name,
        "version": settings.model_version,
        "path": str(path.resolve()),
    }
    return _MODEL


def get_model():
    return load_model()


def get_meta():
    if not _META:
        load_model()
    return _META
