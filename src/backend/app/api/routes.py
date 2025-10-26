import hashlib
import json
import uuid
from time import perf_counter

import structlog
from fastapi import APIRouter, Depends, HTTPException, status

from ..core.auth import authenticate_user, create_access_token, get_current_user
from ..core.model_loader import get_meta
from ..services.predict import predict_proba
from .schemas import (
    ModelInfo,
    PredictRequest,
    PredictResponse,
    TokenRequest,
    TokenResponse,
)

router = APIRouter()
logger = structlog.get_logger(__name__)


@router.get("/health")
def health():
    return {"status": "ok"}


@router.get("/model/info", response_model=ModelInfo)
def model_info():
    logger.info("model_info_requested")
    return get_meta()


@router.post("/auth/token", response_model=TokenResponse)
def issue_token(payload: TokenRequest):
    if not authenticate_user(payload.username, payload.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid username or password",
        )
    token = create_access_token(payload.username)
    logger.info("token_issued", username=payload.username)
    return TokenResponse(access_token=token)


@router.post("/predict", response_model=PredictResponse)
def predict(payload: PredictRequest, _: str = Depends(get_current_user)):
    request_id = uuid.uuid4().hex
    input_id = hashlib.sha256(json.dumps(payload.features, sort_keys=True).encode()).hexdigest()
    start = perf_counter()
    try:
        label, proba = predict_proba(payload.features)
        duration_ms = (perf_counter() - start) * 1000
        logger.info(
            "prediction_made",
            request_id=request_id,
            input_id=input_id,
            label=label,
            proba=proba,
            latency_ms=round(duration_ms, 2),
        )
        return PredictResponse(label=label, proba=proba)
    except ValueError as exc:
        duration_ms = (perf_counter() - start) * 1000
        logger.warning(
            "prediction_validation_error",
            request_id=request_id,
            input_id=input_id,
            latency_ms=round(duration_ms, 2),
            error=str(exc),
        )
        raise HTTPException(status_code=422, detail=str(exc)) from exc
    except Exception as exc:
        duration_ms = (perf_counter() - start) * 1000
        logger.error(
            "prediction_failed",
            request_id=request_id,
            input_id=input_id,
            latency_ms=round(duration_ms, 2),
            error=str(exc),
        )
        raise HTTPException(status_code=400, detail=str(exc)) from exc
