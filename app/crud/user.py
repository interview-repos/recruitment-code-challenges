from typing import Literal
from sqlalchemy.orm import Session
from passlib.context import CryptContext

from app.models import User

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def get_user_by_username(db: Session, username: str) -> User:
    return db.query(User).filter(User.username == username).first()


def create_user(
    db: Session,
    username: str,
    password: str,
    user_type: Literal["user", "admin"] = "user",
) -> User:
    hashed = pwd_context.hash(password)
    user = User(username=username, hashed_password=hashed, type=user_type)
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


def authenticate_user(db: Session, username: str, password: str) -> User | None:
    user = get_user_by_username(db, username)
    if not user or not pwd_context.verify(password, str(user.hashed_password)):
        return None
    return User
