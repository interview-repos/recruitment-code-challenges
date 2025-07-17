from typing import Annotated
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
import jwt
from datetime import datetime, timedelta

from app.core.config import settings
from app.db.session import SessionLocal
from app.crud.user import get_user_by_username


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/users/token")


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def create_access_token(data: dict) -> str:
    to_encode = data.copy()
    expire = datetime.now() + timedelta(minutes=settings.access_token_expiry)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, settings.secret_key, algorithm=settings.algorithm)


def get_current_user(
    token: Annotated[str, Depends(oauth2_scheme)], db: Session = Depends(get_db)
):
    credential_exception = HTTPException(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Forbidden"
    )
    try:
        payload = jwt.decode(
            token, settings.secret_key, algorithms=[settings.algorithm]
        )
        username = payload.get("sub")
        if username is None:
            raise credential_exception
    except jwt.PyJWTError:
        raise credential_exception
    user = get_user_by_username(db, username)
    if user is None:
        return credential_exception
    return user
