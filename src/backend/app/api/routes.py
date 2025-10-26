from fastapi import APIRouter, HTTPException

from ..core.model_loader import get_meta
from ..services.predict import predict_proba
from .schemas import ModelInfo, PredictRequest, PredictResponse

router = APIRouter()


@router.get("/health")
def health():
    return {"status": "ok"}


@router.get("/model/info", response_model=ModelInfo)
def model_info():
    return get_meta()


@router.post("/predict", response_model=PredictResponse)
def predict(payload: PredictRequest):
    try:
        label, proba = predict_proba(payload.features)
        return PredictResponse(label=label, proba=proba)
    except ValueError as exc:
        raise HTTPException(status_code=422, detail=str(exc)) from exc
    except Exception as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
