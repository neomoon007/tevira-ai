from pydantic import TypeAdapter

from src.tevira_ai.schemas import TaskRead
from src.tevira_ai.services.tasks import get_important_task, get_tasks_by_project


def test_get_important_task_returns_highest_priority_task(
    db_session, test_project, test_task
):
    project_id = "project_1"
    response = get_important_task(db_session, project_id)

    assert isinstance(response, TaskRead)
    assert response.id == "task_2"


def test_get_tasks_by_project_returns_only_open_tasks_project_1(
    db_session, test_project, test_task
):
    project_id = "project_1"
    expected_num_of_tasks = 2
    response = get_tasks_by_project(db_session, project_id)

    assert isinstance(response, list), "Response is not a list"
    assert len(response) == expected_num_of_tasks

    assert all(isinstance(task, TaskRead) for task in response), (
        "Not all returned items are TaskRead objects"
    )
    assert all(task.project_id == project_id for task in response), (
        f"Not all returned tasks belong to '{project_id}'"
    )


def test_get_tasks_by_project_returns_empty_list_for_missing_project_tasks(
    db_session, test_project
):
    project_id = "project_1"
    expected_num_of_tasks = 0
    response = get_tasks_by_project(db_session, project_id)

    assert isinstance(response, list), "Response is not a list"
    assert len(response) == expected_num_of_tasks


def test_create_task_accepts_valid_task_object(client, test_project):
    response = client.post(
        "/tasks",
        json={"title": "My new task!", "priority": "high", "project_id": "project_1"},
    )

    assert response.status_code == 201

    data = response.json()
    assert data["status"] == "open"
    assert data["title"] == "My new task!"
    assert data["priority"] == "high"
    assert data["project_id"] == "project_1"


def test_show_tasks_returns_all_tasks_when_no_query_parameter_is_passed(
    client, test_project, test_task
):
    expected_num_of_tasks = 3
    response = client.get("/tasks")

    assert response.status_code == 200

    adapter = TypeAdapter(list[TaskRead])
    tasks = adapter.validate_python(response.json())

    assert isinstance(tasks, list)
    assert len(tasks) == expected_num_of_tasks, f"{tasks}"


def test_show_tasks_with_project_id_returns_all_project_tasks(
    client, test_project, test_task
):
    expected_num_of_tasks = 2
    query_parameters = {"project_id": "project_1"}
    response = client.get("/tasks", params=query_parameters)

    assert response.status_code == 200

    adapter = TypeAdapter(list[TaskRead])
    tasks = adapter.validate_python(response.json())

    assert isinstance(tasks, list)
    assert len(tasks) == expected_num_of_tasks, f"{tasks}"


def test_show_tasks_with_non_existent_project_raises_404(
    client, test_project, test_task
):
    query_parameters = {"project_id": "project_999"}
    response = client.get("/tasks", params=query_parameters)

    assert response.status_code == 404, f"{response.json()}"


def test_show_tasks_with_task_id_returns_only_one_task(client, test_project, test_task):
    query_parameters = {"task_id": "task_1"}
    response = client.get("/tasks", params=query_parameters)
    expected_num_of_tasks = 1

    assert response.status_code == 200

    adapter = TypeAdapter(list[TaskRead])
    tasks = adapter.validate_python(response.json())

    assert isinstance(tasks, list)
    assert len(tasks) == expected_num_of_tasks, f"{tasks}"

    assert tasks[0].id == "task_1"
    assert tasks[0].title == "test task 1"
    assert tasks[0].project_id == "project_1"
    assert tasks[0].priority == "medium"
    assert tasks[0].status == "open"


def test_show_tasks_with_missing_task_raises_404(client, test_project, test_task):
    query_parameters = {"task_id": "task_999"}
    response = client.get("/tasks", params=query_parameters)

    assert response.status_code == 404


def test_show_tasks_with_project_and_task_id_returns_one_task(
    client, test_project, test_task
):
    query_parameters = {"project_id": "project_1", "task_id": "task_1"}
    response = client.get("/tasks", params=query_parameters)

    assert response.status_code == 200

    adapter = TypeAdapter(list[TaskRead])
    tasks = adapter.validate_python(response.json())
    expected_num_of_tasks = 1

    assert isinstance(tasks, list)
    assert len(tasks) == expected_num_of_tasks, f"{tasks}"

    assert tasks[0].id == "task_1"
    assert tasks[0].title == "test task 1"
    assert tasks[0].project_id == "project_1"
    assert tasks[0].priority == "medium"
    assert tasks[0].status == "open"


def test_update_task_accepts_valid_task_object(client, test_project, test_task):
    task_id = "task_1"
    response = client.patch(
        f"/tasks/{task_id}",
        json={"priority": "low"},
    )

    assert response.status_code == 200

    adapter = TypeAdapter(TaskRead)
    task = adapter.validate_python(response.json())

    assert task.id == "task_1"
    assert task.title == "test task 1"
    assert task.project_id == "project_1"
    assert task.priority == "low"
    assert task.status == "open"


def test_update_task_raises_404_for_non_existent_task(client, test_project, test_task):
    task_id = "task_999"

    response = client.patch(f"/tasks/{task_id}", json={"priority": "low"})

    assert response.status_code == 404


def test_delete_task_returns_204(client, test_project, test_task):
    task_id = "task_1"
    response = client.delete(f"/tasks/{task_id}")

    assert response.status_code == 204


def test_delete_task_raises_404_for_non_existent_task(client, test_project, test_task):
    task_id = "task_999"
    response = client.delete(f"/tasks/{task_id}")

    assert response.status_code == 404
