from sqlalchemy.orm import declarative_base
from app.db.session import engine

Base = declarative_base()


def init_db():
    from app.models import User, AdminUser  # noqa: F401

    Base.metadata.create_all(bind=engine)
