import os

import pytest_asyncio
from alembic.config import Config
from httpx import ASGITransport, AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from alembic import command
from src.tevira_ai.db.database import get_db
from src.tevira_ai.db.models import ProgressNote, Project, Task
from src.tevira_ai.dependencies import get_current_owner_id
from src.tevira_ai.main import app

alembic_config = Config("/app/alembic.ini")

test_engine = create_async_engine(
    f"postgresql+psycopg://{os.getenv('POSTGRES_USER')}:{os.getenv('POSTGRES_PASSWORD')}@{os.getenv('DB_HOST')}:5432/{os.getenv('POSTGRES_TEST_DB')}",
    echo=False,
)


@pytest_asyncio.fixture(scope="session", autouse=True, loop_scope="session")
async def setup_database():

    async with test_engine.begin() as connection:
        await connection.run_sync(sync_connection, upgradable=True)
    yield
    async with test_engine.begin() as connection:
        await connection.run_sync(sync_connection, upgradable=False)


def sync_connection(connection, upgradable: bool):
    alembic_config.attributes["connection"] = connection

    if upgradable:
        command.upgrade(alembic_config, "head")
        return

    command.downgrade(alembic_config, "base")


@pytest_asyncio.fixture
async def db_session():
    connection = await test_engine.connect()
    transaction = await connection.begin()
    TestingSession = async_sessionmaker(
        bind=connection,
        expire_on_commit=False,
        join_transaction_mode="create_savepoint",
    )

    async with TestingSession() as session:
        yield session

    await session.close()
    await transaction.rollback()
    await connection.close()


@pytest_asyncio.fixture
async def client(db_session: AsyncSession):
    async def _override_get_db():
        yield db_session

    app.dependency_overrides[get_db] = _override_get_db
    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as client:
        yield client
    app.dependency_overrides.clear()


# --- Data dependencies ---
@pytest_asyncio.fixture
async def test_project(db_session: AsyncSession) -> list[Project]:
    projects = [
        Project(title="Test Project 1", owner_id=get_current_owner_id()),
        Project(title="Test Project 2", owner_id=get_current_owner_id()),
    ]

    db_session.add_all(projects)
    await db_session.commit()

    return projects


@pytest_asyncio.fixture
async def test_note(
    db_session: AsyncSession, test_project: list[Project]
) -> list[ProgressNote]:
    notes = [
        ProgressNote(
            owner_id=get_current_owner_id(),
            project_id=test_project[0].id,
            current_state="test state",
            last_session="last session log",
            open_loops=["first open loop", "second open loop"],
            next_actions="build more, build faster",
            important_context="this is important",
            blockers=["bugs"],
            confidence="medium",
        ),
        ProgressNote(
            owner_id=get_current_owner_id(),
            project_id=test_project[1].id,
            current_state="test state",
            last_session="last session log",
            open_loops=["first open loop", "second open loop"],
            important_context="this is important",
            blockers=["bugs"],
            confidence="medium",
        ),
    ]

    db_session.add_all(notes)
    await db_session.commit()

    return notes


@pytest_asyncio.fixture
async def test_task(
    db_session: AsyncSession, test_project: list[Project]
) -> list[Task]:
    tasks = [
        Task(
            owner_id=get_current_owner_id(),
            title="test task 1",
            project_id=test_project[0].id,
            priority="medium",
            status="open",
        ),
        Task(
            owner_id=get_current_owner_id(),
            title="test task 2",
            project_id=test_project[0].id,
            priority="high",
            status="open",
        ),
        Task(
            owner_id=get_current_owner_id(),
            title="test task 3",
            project_id=test_project[1].id,
            priority="low",
            status="open",
        ),
    ]

    db_session.add_all(tasks)
    await db_session.commit()

    return tasks
