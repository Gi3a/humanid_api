from fastapi import Depends, HTTPException
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from datetime import datetime, timedelta

from jwt import InvalidTokenError, decode, encode

from configs.settings import settings


def create_access_token(user_id: int) -> str:
    payload: dict[str, int | datetime] = {
        "sub": user_id,
        "exp": datetime.utcnow() + timedelta(days=7),
    }

    return encode(
        payload=payload,
        key=settings.JWT_SECRET_KEY,
        algorithm=settings.JWT_ALGORITHM,
    )


def decode_access_token(token: str) -> tuple[int, str]:
    try:
        payload: dict[str, int] = decode(
            jwt=token,
            key=settings.JWT_SECRET_KEY,
            algorithms=[
                settings.JWT_ALGORITHM,
            ],
        )
    except InvalidTokenError:
        return (0, "Token is invalid")

    return (payload["sub"], "")


def identify_user(credentials: HTTPAuthorizationCredentials = Depends(HTTPBearer())) -> int:
    user_id, error_message = decode_access_token(credentials.credentials)
    if error_message:
        raise HTTPException(status_code=401, detail=error_message)
    return user_id
