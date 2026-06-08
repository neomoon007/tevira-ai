from datetime import datetime, timezone
from fastapi.testclient import TestClient
from fastapi import HTTPException
import pytest
from src.app.schemas import ProgressNoteRead, ProjectRead
from src.app.main import (
    app,
    tasks,
    projects,
    progress_notes,
    validate_progress_note,
    validate_project_id,
)

client = TestClient(app)  # create instance


def test_health():
    response = client.get("/health")

    # tests expected behavior from server
    assert response.status_code == 200
    assert response.json() == {
        "status": "ok",
        "service": "tevira-ai",
    }


def test_create_task():
    tasks.clear()

    response = client.post(
        "/tasks",
        json={
            "title": "Hello, World! This is my first task",
            "priority": "high",
            "due_date": None,
            "project_id": None,
        },
    )

    assert response.status_code == 201

    data = response.json()

    assert data["id"] == "task_1"
    assert data["status"] == "open"
    assert data["title"] == "Hello, World! This is my first task"
    assert data["priority"] == "high"
    assert data["due_date"] is None
    assert data["project_id"] is None


@pytest.fixture
def temp_projects():
    projects["project_1"] = ProjectRead(name="foo", id="project_1")
    projects["project_2"] = ProjectRead(name="bar", id="project_2")
    projects["project_3"] = ProjectRead(name="hello", id="project_3")
    projects["project_4"] = ProjectRead(name="world", id="project_4")

    yield projects
    projects.clear()


@pytest.fixture
def temp_notes():
    progress_notes.extend(
        [
            ProgressNoteRead(
                project_id="project_1",
                current_state="Week 08 got to finish soon",
                last_session="Week 08 halfway through",
                open_loops=["not finished", "WIP", "TBA"],
                next_actions="Finish week 08",
                important_context="One step at a time",
                blockers=["No blockers"],
                updated_at=datetime.now(timezone.utc),
            ),
            ProgressNoteRead(
                project_id="project_2",
                current_state="foo",
                last_session="foo",
                open_loops=["not finished", "WIP", "TBA"],
                next_actions="foo",
                important_context="One step at a time",
                blockers=["No blockers"],
                updated_at=datetime.now(timezone.utc),
            ),
            ProgressNoteRead(
                project_id="project_3",
                current_state="bar",
                last_session="bar",
                open_loops=["not finished", "WIP", "TBA"],
                next_actions="bar",
                important_context="One step at a time",
                blockers=["No blockers"],
                updated_at=datetime.now(timezone.utc),
            ),
            ProgressNoteRead(
                project_id="project_4",
                current_state="hello",
                last_session="hello",
                open_loops=["not finished", "WIP", "TBA"],
                next_actions="hello",
                important_context="One step at a time",
                blockers=["No blockers"],
                updated_at=datetime.now(timezone.utc),
            ),
        ]
    )

    yield progress_notes


def test_validate_project_id_accepts_existing_id(temp_projects: dict):
    response = validate_project_id("project_1")

    assert response == "project_1"
    assert "project_1" in temp_projects


def test_validate_project_id_raises_400_for_empty_string(temp_projects: dict):
    with pytest.raises(HTTPException) as exception_info:
        validate_project_id("")

    assert exception_info.value.status_code == 400


def test_validate_project_id_raises_404_for_non_existing_project(temp_projects: dict):
    with pytest.raises(HTTPException) as exception_info:
        validate_project_id("project_42")

    assert exception_info.value.status_code == 404


def test_validate_progress_note_accepts_existing_note(
    temp_notes: list[ProgressNoteRead],
):
    response = validate_progress_note("project_1")
    assert response == "project_1"


def test_validate_progress_note_raises_404_for_non_existing_note(
    temp_notes: list[ProgressNoteRead],
):
    with pytest.raises(HTTPException) as exception_info:
        validate_progress_note("project_42")

    assert exception_info.value.status_code == 404


# test get_project_tasks function works:
def get_project_tasks_returns_all_tasks():
    return


# test normal case (should pass)
# test edge case (shouldn't pass)

# test GET "/health" endpoint

# test POST "/tasks" endpoint
# test normal case (should pass)
# test edge case (shouldn't pass)

# test GET "/tasks" endpoint
# test GET "/tasks" with 0 parameters passed
# test normal case (should pass)
# test edge case (shouldn't pass)

# test GET "/tasks" with only 'project_id' passed
# test normal case (should pass)
# test edge case (shouldn't pass)

# test GET "/tasks" with only 'task_id' passed
# test normal case (should pass)
# test edge case (shouldn't pass)

# test GET "/tasks" with both parameters passed
# test normal case (should pass)
# test edge case (shouldn't pass)

# test POST "/projects" endpoint
# test normal case (should pass)
# test edge case (shouldn't pass)

# test GET "/projects" endpoint
# test normal case (should pass)
# test edge case (shouldn't pass)

# test POST "/progress-notes" endpoint
# test normal case (should pass)
# test edge case (shouldn't pass)

# test GET "/progress-notes" endpoint
# test normal case (should pass)
# test edge case (shouldn't pass)

# test GET "/context" endpoint
# test normal case (should pass) - valid project_id and valid progress_note
# test edge case (shouldn't pass) - invalid project_id
# test edge case (shouldn't pass) - missing project_id
# test edge case (shouldn't pass) - missing progress_note
