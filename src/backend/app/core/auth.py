from __future__ import annotations

from datetime import UTC, datetime, timedelta
from typing import Annotated, Any

import jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from .config import settings

security_scheme = HTTPBearer(auto_error=True)


def authenticate_user(username: str, password: str) -> bool:
    return username == settings.api_username and password == settings.api_password


def create_access_token(subject: str, expires_minutes: int | None = None) -> str:
    expire_in = expires_minutes or settings.jwt_expire_minutes
    expire = datetime.now(tz=UTC) + timedelta(minutes=expire_in)
    payload: dict[str, Any] = {"sub": subject, "exp": expire}
    return jwt.encode(payload, settings.jwt_secret, algorithm=settings.jwt_algorithm)


def decode_token(token: str) -> dict[str, Any]:
    try:
        return jwt.decode(token, settings.jwt_secret, algorithms=[settings.jwt_algorithm])
    except jwt.PyJWTError as exc:  # type: ignore[attr-defined]
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token is invalid or expired",
        ) from exc


TokenCredentials = Annotated[HTTPAuthorizationCredentials, Depends(security_scheme)]


def get_current_user(credentials: TokenCredentials) -> str:
    token_payload = decode_token(credentials.credentials)
    username = token_payload.get("sub")
    if not username:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
        )
    return str(username)
