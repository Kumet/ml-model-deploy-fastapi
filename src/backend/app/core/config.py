from pathlib import Path

from pydantic import Field, model_validator
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
    api_username_file: str | None = Field(default=None)
    api_password_file: str | None = Field(default=None)

    jwt_secret: str = Field(default="super-secret-key")
    jwt_algorithm: str = Field(default="HS256")
    jwt_expire_minutes: int = Field(default=30)
    jwt_secret_file: str | None = Field(default=None)

    @staticmethod
    def _resolve_secret(file_path: str | None, fallback: str, env_name: str) -> str:
        if not file_path:
            return fallback
        try:
            return Path(file_path).read_text(encoding="utf-8").strip()
        except FileNotFoundError as exc:
            raise ValueError(f"Secret file not found for {env_name}: {file_path}") from exc

    @model_validator(mode="after")
    def load_secret_files(self):
        self.api_username = self._resolve_secret(
            self.api_username_file, self.api_username, "API_USERNAME"
        )
        self.api_password = self._resolve_secret(
            self.api_password_file, self.api_password, "API_PASSWORD"
        )
        self.jwt_secret = self._resolve_secret(self.jwt_secret_file, self.jwt_secret, "JWT_SECRET")
        return self


settings = Settings()
