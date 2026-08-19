import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import sessionmaker

from src.tevira_ai.db.database import get_db
from src.tevira_ai.db.models import ProgressNote, Project, Task
from src.tevira_ai.db.test_database import engine
from src.tevira_ai.main import app


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
    projects = [
        Project(title="Test Project 1", id="project_1", owner_id="local_user"),
        Project(title="Test Project 2", id="project_2", owner_id="local_user"),
    ]

    db_session.add_all(projects)
    db_session.commit()

    return projects


@pytest.fixture
def test_note(db_session):
    notes = [
        ProgressNote(
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
        ),
        ProgressNote(
            id="note_2",
            owner_id="local_user",
            project_id="project_2",
            current_state="test state",
            last_session="last session log",
            open_loops=["first open loop", "second open loop"],
            important_context="this is important",
            blockers=["bugs"],
            confidence="medium",
        ),
    ]

    db_session.add_all(notes)
    db_session.commit()

    return notes


@pytest.fixture
def test_task(db_session):
    tasks = [
        Task(
            id="task_1",
            owner_id="local_user",
            title="test task 1",
            project_id="project_1",
            priority="medium",
            status="open",
        ),
        Task(
            id="task_2",
            owner_id="local_user",
            title="test task 2",
            project_id="project_1",
            priority="high",
            status="open",
        ),
        Task(
            id="task_3",
            owner_id="local_user",
            title="test task 3",
            project_id="project_2",
            priority="low",
            status="open",
        ),
    ]

    db_session.add_all(tasks)
    db_session.commit()

    return tasks
