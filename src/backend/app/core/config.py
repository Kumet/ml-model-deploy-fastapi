from pydantic import Field
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    app_env: str = Field(default="local")
    port: int = Field(default=8000)
    model_path: str = Field(default="models/model.joblib")
    model_name: str = Field(default="sklearn-iris")
    model_version: str = Field(default="0.1.0")
    log_level: str = Field(default="INFO")

    api_username: str = Field(default="admin")
    api_password: str = Field(default="changeme")

    jwt_secret: str = Field(default="super-secret-key")
    jwt_algorithm: str = Field(default="HS256")
    jwt_expire_minutes: int = Field(default=30)


settings = Settings()
