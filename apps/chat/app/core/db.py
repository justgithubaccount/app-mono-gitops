from sqlmodel import SQLModel, create_engine, Session
from app.core.config import get_settings

DATABASE_URL = get_settings().database_url
engine = create_engine(DATABASE_URL, echo=True)


def init_db() -> None:
    SQLModel.metadata.create_all(engine)


def get_session():
    with Session(engine) as session:
        yield session
