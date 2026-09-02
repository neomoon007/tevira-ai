import uuid

from httpx import AsyncClient
from pydantic import TypeAdapter
from sqlalchemy.ext.asyncio import AsyncSession

from src.tevira_ai.db.models import Project, Task
from src.tevira_ai.dependencies import get_current_owner_id
from src.tevira_ai.schemas import TaskRead
from src.tevira_ai.services.tasks import get_important_task, get_tasks_by_project


async def test_get_important_task_returns_highest_priority_task(
    db_session: AsyncSession, test_project: list[Project], test_task: list[Task]
):
    project_id = test_project[0].id
    task_id = test_task[1].id
    response = await get_important_task(
        owner_id=get_current_owner_id(), db=db_session, project_id=project_id
    )

    assert isinstance(response, TaskRead)
    assert response.id == task_id


async def test_get_tasks_by_project_returns_only_open_tasks_project_1(
    db_session: AsyncSession, test_project: list[Project], test_task: list[Task]
):
    project_id = test_project[0].id
    expected_num_of_tasks = 2
    response = await get_tasks_by_project(
        owner_id=get_current_owner_id(), db=db_session, project_id=project_id
    )

    assert isinstance(response, list), "Response is not a list"
    assert len(response) == expected_num_of_tasks

    assert all(isinstance(task, TaskRead) for task in response), (
        "Not all returned items are TaskRead objects"
    )
    assert all(task.project_id == project_id for task in response), (
        f"Not all returned tasks belong to '{project_id}'"
    )


async def test_get_tasks_by_project_returns_empty_list_for_missing_project_tasks(
    db_session: AsyncSession, test_project: list[Project]
):
    project_id = test_project[0].id
    expected_num_of_tasks = 0
    response = await get_tasks_by_project(
        owner_id=get_current_owner_id(), db=db_session, project_id=project_id
    )

    assert isinstance(response, list), "Response is not a list"
    assert len(response) == expected_num_of_tasks


async def test_create_task_accepts_valid_task_object(
    client: AsyncClient, test_project: list[Project]
):
    project_id = str(test_project[0].id)
    response = await client.post(
        "/tasks",
        json={"title": "My new task!", "priority": "high", "project_id": project_id},
    )

    assert response.status_code == 201

    data = response.json()
    assert data["status"] == "open"
    assert data["title"] == "My new task!"
    assert data["priority"] == "high"
    assert data["project_id"] == project_id


async def test_show_tasks_returns_all_tasks_when_no_query_parameter_is_passed(
    client: AsyncClient, test_project: list[Project], test_task: list[Task]
):
    expected_num_of_tasks = 3
    response = await client.get("/tasks")
    assert response.status_code == 200

    adapter = TypeAdapter(list[TaskRead])
    tasks = adapter.validate_python(response.json())
    assert isinstance(tasks, list)
    assert len(tasks) == expected_num_of_tasks, f"{tasks}"


async def test_show_tasks_with_project_id_returns_all_project_tasks(
    client: AsyncClient, test_project: list[Project], test_task: list[Task]
):
    project_id = str(test_project[0].id)
    expected_num_of_tasks = 2
    query_parameters = {"project_id": project_id}
    response = await client.get("/tasks", params=query_parameters)

    assert response.status_code == 200

    adapter = TypeAdapter(list[TaskRead])
    tasks = adapter.validate_python(response.json())
    assert isinstance(tasks, list)
    assert len(tasks) == expected_num_of_tasks, f"{tasks}"


async def test_show_tasks_with_non_existent_project_raises_404(
    client: AsyncClient, test_project: list[Project], test_task: list[Task]
):
    non_existent_project_id = str(uuid.uuid7())
    query_parameters = {"project_id": non_existent_project_id}
    response = await client.get("/tasks", params=query_parameters)

    assert response.status_code == 404, f"{response.json()}"


async def test_show_tasks_with_task_id_returns_only_one_task(
    client: AsyncClient, test_project: list[Project], test_task: list[Task]
):
    task_id = test_task[0].id
    project_id = test_project[0].id
    query_parameters = {"task_id": str(task_id)}
    response = await client.get("/tasks", params=query_parameters)
    expected_num_of_tasks = 1

    assert response.status_code == 200

    adapter = TypeAdapter(list[TaskRead])
    tasks = adapter.validate_python(response.json())

    assert isinstance(tasks, list)
    assert len(tasks) == expected_num_of_tasks, f"{tasks}"

    assert tasks[0].id == task_id
    assert tasks[0].title == "test task 1"
    assert tasks[0].project_id == project_id
    assert tasks[0].priority == "medium"
    assert tasks[0].status == "open"


async def test_show_tasks_with_missing_task_raises_404(
    client: AsyncClient, test_project: list[Project], test_task: list[Task]
):
    non_existent_task_id = str(uuid.uuid7())
    query_parameters = {"task_id": non_existent_task_id}
    response = await client.get("/tasks", params=query_parameters)

    assert response.status_code == 404


async def test_show_tasks_with_project_and_task_id_returns_one_task(
    client: AsyncClient, test_project: list[Project], test_task: list[Task]
):
    project_id = test_project[0].id
    task_id = test_task[0].id
    query_parameters = {"project_id": str(project_id), "task_id": str(task_id)}
    response = await client.get("/tasks", params=query_parameters)

    assert response.status_code == 200

    adapter = TypeAdapter(list[TaskRead])
    tasks = adapter.validate_python(response.json())
    expected_num_of_tasks = 1

    assert isinstance(tasks, list)
    assert len(tasks) == expected_num_of_tasks, f"{tasks}"

    assert tasks[0].id == task_id
    assert tasks[0].title == "test task 1"
    assert tasks[0].project_id == project_id
    assert tasks[0].priority == "medium"
    assert tasks[0].status == "open"


async def test_update_task_accepts_valid_task_object(
    client: AsyncClient, test_project: list[Project], test_task: list[Task]
):
    task_id = test_task[0].id
    project_id = test_project[0].id
    response = await client.patch(
        f"/tasks/{task_id}",
        json={"priority": "low"},
    )

    assert response.status_code == 200

    adapter = TypeAdapter(TaskRead)
    task = adapter.validate_python(response.json())

    assert task.id == task_id
    assert task.title == "test task 1"
    assert task.project_id == project_id
    assert task.priority == "low"
    assert task.status == "open"


async def test_update_task_raises_404_for_non_existent_task(
    client: AsyncClient, test_project: list[Project], test_task: list[Task]
):
    task_id = uuid.uuid7()
    response = await client.patch(f"/tasks/{task_id}", json={"priority": "low"})

    assert response.status_code == 404


async def test_delete_task_returns_204(
    client: AsyncClient, test_project: list[Project], test_task: list[Task]
):
    task_id = test_task[0].id
    response = await client.delete(f"/tasks/{task_id}")

    assert response.status_code == 204


async def test_delete_task_raises_404_for_non_existent_task(
    client: AsyncClient, test_project: list[Project], test_task: list[Task]
):
    task_id = uuid.uuid7()
    response = await client.delete(f"/tasks/{task_id}")

    assert response.status_code == 404
