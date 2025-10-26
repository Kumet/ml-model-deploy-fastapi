from __future__ import annotations

import numpy as np
import structlog

from ..core.model_loader import get_model

logger = structlog.get_logger(__name__)


def predict_proba(features: list[float]) -> tuple[int, float]:
    array = np.asarray(features, dtype=float)
    if array.ndim != 1:
        raise ValueError("features は一次元配列で指定してください")

    sample = array.reshape(1, -1)
    model = get_model()

    if hasattr(model, "predict_proba"):
        proba = float(max(model.predict_proba(sample)[0]))
    else:
        proba = 1.0

    label = int(model.predict(sample)[0])
    logger.debug("predict_proba", label=label, proba=proba)
    return label, proba
