from pydantic import BaseModel
import pydantic


class UserCreate(BaseModel):
    username: str
    password: str


class UserOut(BaseModel):
    id: int
    username: str

    class Config:
        from_attributes = True


class AdminUserOut(UserOut):
    is_admin: bool


@pydantic.dataclasses.dataclass
class Token:
    access_token: str
    token_type: str
