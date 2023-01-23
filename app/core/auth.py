from typing import Optional
from datetime import datetime, timedelta

from fastapi import Depends, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm.session import Session
from jose import jwt, JWTError
from starlette import status
from starlette.requests import Request

from app.core.config import settings
from app.core.security import verify_password
from app.db import deps
from app.models.users import User


def authenticate(
    *,
    phone_number: str,
    password: str,
    db: Session = Depends(deps.get_db),
) -> Optional[User]:
    user = db.query(User).filter(User.phone_number == phone_number).first()
    if not user:
        return None
    if not verify_password(password, user.hashed_password):
        return None
    return user


def create_access_token(*, sub: int) -> str:
    return _create_token(
        token_type="access_token",
        lifetime=timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES),
        sub=sub,
    )


def _create_token(
    token_type: str,
    lifetime: timedelta,
    sub: int,
) -> str:
    payload = {}
    expire = datetime.utcnow() + lifetime
    payload["type"] = token_type
    payload["exp"] = expire
    payload["iat"] = datetime.utcnow()
    payload["sub"] = str(sub)

    return jwt.encode(payload, settings.JWT_SECRET, algorithm=settings.ALGORITHM)


class JWTBearer(HTTPBearer):
    def __init__(self):
        super(JWTBearer, self).__init__()

    async def __call__(self, request: Request):
        credentials: HTTPAuthorizationCredentials = await super(JWTBearer, self).__call__(request)
        credentials_exception = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token or expired token",
        )
        if credentials:
            if credentials.scheme != "Bearer":
                raise credentials_exception
            try:
                payload = jwt.decode(
                    credentials.credentials, settings.JWT_SECRET, algorithms=[settings.ALGORITHM]
                )
                user_id: str = payload.get("sub")
                if user_id is None:
                    raise credentials_exception
                return user_id
            except JWTError:
                raise credentials_exception
        else:
            raise credentials_exception


def get_current_user_from_token(
        db: Session = Depends(deps.get_db),
        user_id: str = Depends(JWTBearer())
):
    user = db.query(User).filter(User.id == user_id).first()
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token or expired token.")
    if not user.notary:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="The user is not a notary.")
    return user
