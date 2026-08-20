import os
from collections.abc import AsyncGenerator

from dotenv import load_dotenv
from fastapi import Request
from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)

load_dotenv()


def get_db_url() -> str:
    return (
        f"postgresql+psycopg://"
        f"{os.getenv('POSTGRES_USER')}:"
        f"{os.getenv('POSTGRES_PASSWORD')}"
        f"@localhost:5432/"
        f"{os.getenv('POSTGRES_DB')}"
    )


def create_engine(database_url: str) -> AsyncEngine:
    engine = create_async_engine(database_url, echo=False)
    return engine


def create_session(engine: AsyncEngine) -> async_sessionmaker[AsyncSession]:
    AsyncSessionLocal = async_sessionmaker(
        bind=engine,
        autoflush=False,
        expire_on_commit=False,
        class_=AsyncSession,
    )
    return AsyncSessionLocal


async def get_db(request: Request) -> AsyncGenerator[AsyncSession]:
    async with request.app.state.session_factory() as session:
        yield session
