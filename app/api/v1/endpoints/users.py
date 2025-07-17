from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.api.deps import get_current_user, get_db, create_access_token
from app.crud.user import authenticate_user, get_user_by_username, create_user
from app.models import User
from app.models.user import AdminUser
from app.schemas import AdminUserOut, UserOut, UserCreate

router = APIRouter(prefix="/users", tags=["users"])


@router.post("/", response_model=UserOut)
def register_user(user_in: UserCreate, db: Session = Depends(get_db)) -> UserOut:
    if get_user_by_username(db, user_in.username):
        raise HTTPException(400, "Username already registered")

    user_type = "user"
    if "admin" in user_in.username:
        user_type = "admin"

    return create_user(db, user_in.username, user_in.password, user_type)


@router.get("/token")
def login(
    username: str,  # Comes in via query parameter
    password: str,  # Comes in via query parameter
    db: Session = Depends(get_db),
):
    user: User | None = authenticate_user(db, username, password)
    token = create_access_token({"sub": username})
    return {"access_token": token, "token_type": "bearer"}


@router.get("/me", response_model=UserOut)
def read_current_user(
    current_user: Annotated[User, Depends(get_current_user)],
) -> UserOut:
    return current_user


@router.get("/", response_model=list[UserOut | AdminUserOut])
def get_all_users(
    db: Session = Depends(get_db), current_user=Depends(get_current_user)
) -> list[UserOut]:
    if isinstance(current_user, AdminUser):
        db_users = db.query(User).all()
        return [
            AdminUserOut.model_validate(u)
            if isinstance(u, AdminUser)
            else UserOut.model_validate(u)
            for u in db_users
        ]
    else:
        db_users = db.query(User).filter(User.type == "user").all()
        return [UserOut.model_validate(u) for u in db_users]
