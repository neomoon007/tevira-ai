import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import sessionmaker

from src.app.db.database import get_db
from src.app.db.models import ProgressNote, Project, Task
from src.app.db.test_database import engine
from src.app.main import app


@pytest.fixture
def db_session():
    connection = engine.connect()
    transaction = connection.begin()

    TestSession = sessionmaker(
        bind=connection,
        join_transaction_mode="create_savepoint",
        expire_on_commit=False,
    )

    session = TestSession()

    yield session

    session.close()
    transaction.rollback()
    connection.close()


@pytest.fixture
def client(db_session):
    app.dependency_overrides[get_db] = lambda: db_session

    with TestClient(app) as test_client:
        yield test_client

    app.dependency_overrides.clear()


# --- Data dependencies ---
@pytest.fixture
def test_project(db_session):
    project = Project(title="Test Project", id="project_1", owner_id="local_user")

    db_session.add(project)
    db_session.commit()

    return project


@pytest.fixture
def test_note(db_session):
    note = ProgressNote(
        id="note_1",
        owner_id="local_user",
        project_id="project_1",
        current_state="test state",
        last_session="last session log",
        open_loops=["first open loop", "second open loop"],
        next_actions="build more, build faster",
        important_context="this is important",
        blockers=["bugs"],
        confidence="medium",
    )

    db_session.add(note)
    db_session.commit()

    return note
