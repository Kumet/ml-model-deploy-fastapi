from pydantic import Field
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    app_env: str = Field(default="local")
    port: int = Field(default=8000)
    model_path: str = Field(default="models/model.joblib")
    model_name: str = Field(default="sklearn-iris")
    model_version: str = Field(default="0.1.0")


settings = Settings()
