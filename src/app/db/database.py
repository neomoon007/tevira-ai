import os
from collections.abc import Iterator

from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker

load_dotenv()

DATABASE_URL = (
    f"postgresql+psycopg://"
    f"{os.getenv('POSTGRES_USER')}:"
    f"{os.getenv('POSTGRES_PASSWORD')}"
    f"@localhost:5432/"
    f"{os.getenv('POSTGRES_DB')}"
)

if not DATABASE_URL:
    raise ValueError("DATABASE_URL environment variable is missing")


def create_session(database_url: str):
    engine = create_engine(database_url, echo=True)

    SessionLocal = sessionmaker(
        bind=engine,
        autoflush=False,
        expire_on_commit=False,
    )

    return engine, SessionLocal


engine, SessionLocal = create_session(DATABASE_URL)


def get_db() -> Iterator[Session]:
    db = SessionLocal()

    try:
        yield db
    finally:
        db.close()
