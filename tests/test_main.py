from datetime import datetime, timezone, date
from fastapi.testclient import TestClient
from fastapi import HTTPException
import pytest
from pydantic import TypeAdapter
from src.app.schemas import ProgressNoteRead, ProjectRead, TaskRead
from src.app.parser import parse_note
from src.app.main import app
from src.app.state.memory import (
    progress_notes_in_memory,
    projects_in_memory,
    tasks_in_memory,
)
from src.app.validator import (
    get_project_tasks,
    validate_progress_note,
    validate_project_id,
)

client = TestClient(app)  # create instance


# TODO: change from global variable to yield one dictionary that has ProjectRead objects in it
@pytest.fixture
def temp_projects():
    projects_in_memory["project_1"] = ProjectRead(name="SAT", id="project_1")
    projects_in_memory["project_2"] = ProjectRead(name="Tevira-AI", id="project_2")
    projects_in_memory["project_3"] = ProjectRead(name="Tech", id="project_3")
    projects_in_memory["project_4"] = ProjectRead(name="foo", id="project_4")

    yield projects_in_memory
    projects_in_memory.clear()


@pytest.fixture
def temp_notes():
    progress_notes_in_memory.extend(
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
                current_state="SAT",
                last_session="SAT",
                open_loops=["not finished", "WIP", "TBA"],
                next_actions="SAT",
                important_context="One step at a time",
                blockers=["No blockers"],
                updated_at=datetime.now(timezone.utc),
            ),
            ProgressNoteRead(
                project_id="project_3",
                current_state="Tevira-AI",
                last_session="Tevira-AI",
                open_loops=["not finished", "WIP", "TBA"],
                next_actions="Tevira-AI",
                important_context="One step at a time",
                blockers=["No blockers"],
                updated_at=datetime.now(timezone.utc),
            ),
            ProgressNoteRead(
                project_id="project_4",
                current_state="Tech",
                last_session="Tech",
                open_loops=["not finished", "WIP", "TBA"],
                next_actions="Tech",
                important_context="One step at a time",
                blockers=["No blockers"],
                updated_at=datetime.now(timezone.utc),
            ),
        ]
    )

    yield progress_notes_in_memory
    progress_notes_in_memory.clear()


@pytest.fixture
def temp_tasks():
    tasks_in_memory.extend(
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
                title="SAT",
                priority="medium",
                due_date=date.today(),
                project_id="project_1",
                id="task_2",
                status="open",
            ),
            TaskRead(
                title="Tevira-AI",
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

    yield tasks_in_memory
    tasks_in_memory.clear()


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
    tasks_in_memory.clear()

    response = client.post(
        "/tasks",
        json={
            "title": "Tech, foo! This is my first task",
            "priority": "high",
            "due_date": None,
            "project_id": None,
        },
    )

    assert response.status_code == 201

    data = response.json()

    assert data["id"] == "task_1"
    assert data["status"] == "open"
    assert data["title"] == "Tech, foo! This is my first task"
    assert data["priority"] == "high"
    assert data["due_date"] is None
    assert data["project_id"] is None
    tasks_in_memory.clear()


def test_show_tasks_returns_all_tasks_when_no_query_parameter_is_passed(temp_tasks):
    expected_num_of_tasks = 4
    response = client.get("/tasks")
    assert response.status_code == 200

    adapter = TypeAdapter(list[TaskRead])
    tasks = adapter.validate_python(response.json())

    assert isinstance(tasks, list)
    assert len(tasks) == expected_num_of_tasks, f"{tasks}"


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


def test_show_tasks_with_task_id_raises_only_one_task(temp_tasks, temp_projects):
    response = client.get("/tasks", params={"task_id": "task_9999"})
    assert response.status_code == 404


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


def test_show_tasks_raises_404_when_task_not_in_project_scope(
    temp_tasks, temp_projects
):
    response = client.get(
        "/tasks", params={"project_id": "project_1", "task_id": "task_4"}
    )
    assert response.status_code == 404


def test_create_project_accepts_valid_project_object(temp_projects):
    projects_in_memory.clear()

    response = client.post(
        "/projects",
        json={"name": "Magnum Opus"},
    )

    assert response.status_code == 201

    data = response.json()
    assert data["name"] == "Magnum Opus"
    assert data["id"] == "project_1"
    projects_in_memory.clear()


def test_create_progress_note_accepts_valid_note_object():
    progress_notes_in_memory.clear()

    response = client.post(
        "/progress-notes",
        json={
            "project_id": "project_1",
            "current_state": "Just created main.py",
            "last_session": "Created github repo",
            "open_loops": ["Create roadmap", "Follow roadmap"],
            "next_actions": "Create fastapi instance",
            "important_context": "Read documentation",
            "blockers": ["Nothing"],
            "confidence": "high",
        },
    )

    response.status_code == 201

    data = response.json()
    assert data["project_id"] == "project_1"
    assert data["current_state"] == "Just created main.py"
    assert data["last_session"] == "Created github repo"
    assert data["open_loops"] == ["Create roadmap", "Follow roadmap"]
    assert data["next_actions"] == "Create fastapi instance"
    assert data["important_context"] == "Read documentation"
    assert data["blockers"] == ["Nothing"]
    assert data["confidence"] == "high"
    progress_notes_in_memory.clear()


def test_show_notes_returns_progress_notes_for_given_project(temp_notes, temp_projects):
    lookup_project = "project_1"
    expected_num_of_notes = 1
    response = client.get(f"/progress-notes/{lookup_project}")

    assert response.status_code == 200

    adapter = TypeAdapter(list[ProgressNoteRead])
    notes = adapter.validate_python(response.json())

    assert isinstance(notes, list)
    assert len(notes) == expected_num_of_notes, f"{notes}"


# test GET "/context" endpoint
def test_restore_context_accepts_valid_project_with_existing_note(
    temp_notes, temp_projects, temp_tasks
):
    lookup_project = "project_1"
    response = client.get(f"/context/{lookup_project}")

    assert response.status_code == 200

    data = response.json()

    assert data["project"] == {"id": "project_1", "name": "SAT"}
    assert data["current_state"] == "Week 08 got to finish soon"
    assert data["open_loops"] == ["not finished", "WIP", "TBA"]
    assert data["open_tasks"] == [
        {
            "title": "Hello World!",
            "priority": "high",
            "due_date": str(date.today()),
            "project_id": "project_1",
            "id": "task_1",
            "status": "open",
        },
        {
            "title": "SAT",
            "priority": "medium",
            "due_date": str(date.today()),
            "project_id": "project_1",
            "id": "task_2",
            "status": "open",
        },
    ]
    assert data["next_actions"] == "Finish week 08"
    assert data["important_context"] == "One step at a time"


def test_restore_context_raises_404_for_non_existent_project(
    temp_notes, temp_projects, temp_tasks
):
    lookup_project = "project_42"
    response = client.get(f"/context/{lookup_project}")

    assert response.status_code == 404


def test_restore_context_raises_404_for_missing_progress_note(
    temp_projects, temp_tasks
):
    lookup_project = "project_1"
    response = client.get(f"/context/{lookup_project}")

    assert response.status_code == 404


def test_parse_note_accepts_valid_input(temp_projects):
    messy_note = (
        "Need to finish the README for SAT before Friday. Next, add setup commands"
    )
    response = parse_note(messy_note, temp_projects)

    assert response == {
        "title": "Need to finish the README for SAT",
        "project_hint": "SAT",
        "due_date_hint": "Friday.",
        "next_action_hint": "add setup commands",
    }
