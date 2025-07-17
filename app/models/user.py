from sqlalchemy import Column, Integer, String, Boolean
from app.db.base import Base


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    type = Column(String)

    __mapper_args__ = {"polymorphic_identity": "user", "polymorphic_on": type}


class AdminUser(User):
    is_admin = Column(Boolean, default=True)

    __mapper_args__ = {"polymorphic_identity": "admin"}
