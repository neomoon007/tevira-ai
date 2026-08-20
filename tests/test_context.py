import uuid

from httpx import AsyncClient

from src.tevira_ai.db.models import ProgressNote, Project, Task


async def test_restore_context_accepts_valid_project_with_existing_note(
    client: AsyncClient, test_project: list[Project], test_note: list[ProgressNote]
):
    lookup_project = str(test_project[0].id)
    response = await client.get(f"/context/{lookup_project}")

    assert response.status_code == 200

    data = response.json()

    assert data["project"] == {
        "id": lookup_project,
        "title": "Test Project 1",
    }
    assert data["current_state"] == "test state"
    assert data["open_loops"] == ["first open loop", "second open loop"]
    assert data["open_tasks"] == []
    assert data["next_actions"] == "build more, build faster"
    assert data["important_context"] == "this is important"


async def test_restore_context_raises_404_for_non_existent_project(
    client: AsyncClient, test_project: list[Project]
):
    lookup_project = str(uuid.uuid7())
    response = await client.get(f"/context/{lookup_project}")

    assert response.status_code == 404


async def test_restore_context_returns_task_when_missing_next_actions(
    client: AsyncClient,
    test_project: list[Project],
    test_note: list[ProgressNote],
    test_task: list[Task],
):
    project_id = str(test_project[1].id)
    task_id = str(test_task[2].id)

    response = await client.get(f"/context/{project_id}")

    assert response.status_code == 200

    data = response.json()

    assert data["next_actions"] == {
        "title": "test task 3",
        "priority": "low",
        "due_date": None,
        "project_id": project_id,
        "id": task_id,
        "status": "open",
    }
