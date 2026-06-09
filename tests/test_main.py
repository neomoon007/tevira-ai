from datetime import datetime, timezone, date
from fastapi.testclient import TestClient
from fastapi import HTTPException
import pytest
from pydantic import TypeAdapter
from src.app.schemas import ProgressNoteRead, ProjectRead, TaskRead
from src.app.main import (
    app,
    tasks,
    projects,
    progress_notes,
    validate_progress_note,
    validate_project_id,
    get_project_tasks,
)

client = TestClient(app)  # create instance


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
    progress_notes.clear()


@pytest.fixture
def temp_tasks():
    tasks.extend(
        [
            TaskRead(
                title="Hello World!",
                priority="high",
                due_date=date.today(),
                project_id="project_1",
                id="task_1",
                status="open",
            ),
            TaskRead(
                title="foo",
                priority="medium",
                due_date=date.today(),
                project_id="project_1",
                id="task_2",
                status="open",
            ),
            TaskRead(
                title="bar",
                priority="low",
                due_date=date.today(),
                project_id="project_2",
                id="task_3",
                status="open",
            ),
            TaskRead(
                title="bro",
                priority="high",
                due_date=date.today(),
                project_id="project_2",
                id="task_4",
                status="done",
            ),
        ]
    )

    yield tasks
    tasks.clear()


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
def test_get_project_tasks_returns_only_open_tasks_project_1(temp_tasks):
    mock_project_id = "project_1"
    expected_num_of_tasks = 2
    response = get_project_tasks(mock_project_id)

    assert isinstance(response, list), "Response is not a list of TaskRead objects"
    assert len(response) == expected_num_of_tasks

    assert all(isinstance(task, TaskRead) for task in response), (
        "Not all items are TaskRead objects"
    )
    assert all(task.project_id == mock_project_id for task in response), (
        f"Not all returned tasks belong to '{mock_project_id}'"
    )


def test_get_project_tasks_returns_only_open_tasks_project_2(temp_tasks):
    mock_project_id = "project_2"
    expected_num_of_tasks = 1
    response = get_project_tasks(mock_project_id)

    assert isinstance(response, list), "Response is not a list of TaskRead objects"
    assert len(response) == expected_num_of_tasks

    assert all(isinstance(task, TaskRead) for task in response), (
        "Not all items are TaskRead objects"
    )
    assert all(task.project_id == mock_project_id for task in response), (
        f"Not all returned tasks belong to '{mock_project_id}'"
    )


def test_get_project_tasks_returns_empty_list_for_missing_project_tasks(temp_tasks):
    mock_project_id = "project_42"
    expected_num_of_tasks = 0
    response = get_project_tasks(mock_project_id)

    assert isinstance(response, list), "Response is not a list of TaskRead objects"
    assert len(response) == expected_num_of_tasks


def test_health_success():
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {
        "status": "ok",
        "service": "tevira-ai",
    }


def test_create_task_accepts_valid_task_object():
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
    tasks.clear()


def test_show_tasks_returns_all_tasks_when_no_query_parameter_is_passed(temp_tasks):
    expected_num_of_tasks = 4
    response = client.get("/tasks")
    assert response.status_code == 200

    adapter = TypeAdapter(list[TaskRead])
    tasks = adapter.validate_python(response.json())

    assert isinstance(tasks, list)
    assert len(tasks) == expected_num_of_tasks, f"{tasks}"
    tasks.clear()


def test_show_tasks_with_project_id_returns_all_project_tasks(
    temp_tasks, temp_projects
):
    expected_num_of_tasks = 2
    query_parameters = {
        "project_id": "project_1",
    }
    response = client.get("/tasks", params=query_parameters)
    assert response.status_code == 200

    adapter = TypeAdapter(list[TaskRead])
    tasks = adapter.validate_python(response.json())

    assert isinstance(tasks, list)
    assert len(tasks) == expected_num_of_tasks, f"{tasks}"
    tasks.clear()


def test_show_tasks_with_non_existent_project_id_raises_404(temp_tasks, temp_projects):
    response = client.get("/tasks", params={"project_id": "project_52"})
    assert response.status_code == 404


def test_show_tasks_with_task_id_returns_only_one_task(temp_tasks, temp_projects):
    response = client.get("/tasks", params={"task_id": "task_1"})
    expected_num_of_tasks = 1

    assert response.status_code == 200

    adapter = TypeAdapter(list[TaskRead])
    tasks = adapter.validate_python(response.json())

    assert isinstance(tasks, list)
    assert len(tasks) == expected_num_of_tasks, f"{tasks}"

    assert tasks[0].title == "Hello World!"
    assert tasks[0].priority == "high"
    assert tasks[0].due_date == date.today()
    assert tasks[0].project_id == "project_1"
    assert tasks[0].id == "task_1"
    assert tasks[0].status == "open"
    tasks.clear()


def test_show_tasks_with_task_id_raises_only_one_task(temp_tasks, temp_projects):
    response = client.get("/tasks", params={"task_id": "task_9999"})
    assert response.status_code == 404
    tasks.clear()


def test_show_tasks_with_project_and_task_id_returns_scoped_task(
    temp_tasks, temp_projects
):
    response = client.get(
        "/tasks", params={"project_id": "project_1", "task_id": "task_1"}
    )

    response.status_code == 200
    adapter = TypeAdapter(list[TaskRead])
    tasks = adapter.validate_python(response.json())
    expected_num_of_tasks = 1

    assert isinstance(tasks, list)
    assert len(tasks) == expected_num_of_tasks, f"{tasks}"

    assert tasks[0].title == "Hello World!"
    assert tasks[0].priority == "high"
    assert tasks[0].due_date == date.today()
    assert tasks[0].project_id == "project_1"
    assert tasks[0].id == "task_1"
    assert tasks[0].status == "open"
    tasks.clear()


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
