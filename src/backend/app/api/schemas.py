from pydantic import BaseModel, Field


class PredictRequest(BaseModel):
    features: list[float] = Field(..., description="数値特徴量のリスト")


class PredictResponse(BaseModel):
    label: int
    proba: float


class ModelInfo(BaseModel):
    name: str
    version: str
    path: str


class TokenRequest(BaseModel):
    username: str
    password: str


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
