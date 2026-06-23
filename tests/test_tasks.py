from src.app.schemas import TaskRead, TaskUpdate
from src.app.validator import get_project_tasks
from src.app.state.memory import tasks_in_memory
from pydantic import TypeAdapter, ValidationError
from datetime import date
import pytest

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

def test_create_task_accepts_valid_task_object(client):
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


def test_show_tasks_returns_all_tasks_when_no_query_parameter_is_passed(client, temp_tasks):
    expected_num_of_tasks = 4
    response = client.get("/tasks")
    assert response.status_code == 200

    adapter = TypeAdapter(list[TaskRead])
    tasks = adapter.validate_python(response.json())

    assert isinstance(tasks, list)
    assert len(tasks) == expected_num_of_tasks, f"{tasks}"


def test_show_tasks_with_project_id_returns_all_project_tasks(
    temp_tasks, temp_projects, client
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


def test_show_tasks_with_non_existent_project_id_raises_404(temp_tasks, temp_projects, client):
    response = client.get("/tasks", params={"project_id": "project_52"})
    assert response.status_code == 404


def test_show_tasks_with_task_id_returns_only_one_task(temp_tasks, temp_projects, client):
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


def test_show_tasks_with_task_id_raises_only_one_task(temp_tasks, temp_projects, client):
    response = client.get("/tasks", params={"task_id": "task_9999"})
    assert response.status_code == 404


def test_show_tasks_with_project_and_task_id_returns_scoped_task(
    temp_tasks, temp_projects, client
):
    response = client.get(
        "/tasks", params={"project_id": "project_1", "task_id": "task_1"}
    )

    assert response.status_code == 200
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
    temp_tasks, temp_projects, client
):
    response = client.get(
        "/tasks", params={"project_id": "project_1", "task_id": "task_4"}
    )
    assert response.status_code == 404

# Whats new:
def test_update_task_accepts_valid_taskread_object(temp_tasks, client):
    given_task_id = "task_1"

    response = client.patch(
        f"/tasks/{given_task_id}",
        json={
            "id": given_task_id,
            "priority": "low",
            "project_id": None,
        }
    )

    assert response.status_code == 200

    adapter = TypeAdapter(TaskRead)
    tasks = adapter.validate_python(response.json())

    assert tasks.title == "Hello World!"
    assert tasks.priority == "low"
    assert tasks.due_date == date.today()
    assert tasks.project_id == "project_1"
    assert tasks.id == "task_1"
    assert tasks.status == "open"
    tasks_in_memory.clear()

def test_update_task_raises_404_for_non_existent_task_id(temp_tasks, client):
    given_task_id = "task_99"

    response = client.patch(
        f"/tasks/{given_task_id}",
        json={
            "id": given_task_id,
            "priority": "low",
            "project_id": None,
        }
    )

    assert response.status_code == 404
    tasks_in_memory.clear()

def test_update_tasks_raises_422_for_missing_updatable_fields(temp_tasks, client):
    given_task_id = "task_1"

    response = client.patch(
        f"/tasks/{given_task_id}",
        json={
            "id": given_task_id,
        }
    )

    assert response.status_code == 422
    tasks_in_memory.clear()

def test_taskupdate_accepts_valid_input():
    input = {"id": "task_1", "title": "my little task", "status": None}

    object = TaskUpdate(**input)

    assert object.id == "task_1"
    assert object.title == "my little task"
    assert object.status is None

def test_taskupdate_raises_error_for_missing_id():
    input = {"title": "my little task", "status": None}

    with pytest.raises(ValidationError):
        TaskUpdate(**input)