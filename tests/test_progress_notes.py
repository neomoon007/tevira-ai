from uuid import UUID

from httpx import AsyncClient

from src.tevira_ai.db.models import ProgressNote, Project


async def test_create_progress_note_accepts_valid_note_obj(
    client: AsyncClient, test_project: list[Project], as_owner_a: UUID
):
    project_id = str(test_project[0].id)
    response = await client.post(
        "/progress-notes",
        json={
            "project_id": project_id,
            "current_state": "Just created main.py",
            "last_session": "Created github repo",
            "open_loops": ["Create roadmap", "Follow roadmap"],
            "next_actions": "Create fastapi instance",
            "important_context": "Read documentation",
            "blockers": ["Nothing"],
            "confidence": "high",
        },
    )

    assert response.status_code == 201

    data = response.json()
    assert data["project_id"] == project_id
    assert data["current_state"] == "Just created main.py"
    assert data["last_session"] == "Created github repo"
    assert data["open_loops"] == ["Create roadmap", "Follow roadmap"]
    assert data["next_actions"] == "Create fastapi instance"
    assert data["important_context"] == "Read documentation"
    assert data["blockers"] == ["Nothing"]
    assert data["confidence"] == "high"


async def test_get_progress_note_returns_existing_note(
    client: AsyncClient,
    test_project: list[Project],
    test_note: list[ProgressNote],
    as_owner_a: UUID,
):
    note_id = str(test_note[0].id)
    project_id = str(test_project[0].id)

    response = await client.get(f"/progress-notes/{note_id}")
    assert response.status_code == 200

    data = response.json()
    assert data["id"] == note_id
    assert data["project_id"] == project_id
    assert data["current_state"] == "test state"
    assert data["last_session"] == "last session log"
    assert data["open_loops"] == ["first open loop", "second open loop"]
    assert data["next_actions"] == "build more, build faster"
    assert data["important_context"] == "this is important"
    assert data["blockers"] == ["bugs"]
    assert data["confidence"] == "medium"


async def test_patch_note_router_returns_accepts_valid_input(
    client: AsyncClient,
    test_project: list[Project],
    test_note: list[ProgressNote],
    as_owner_a: UUID,
):
    note_id = str(test_note[0].id)

    response = await client.patch(
        f"/progress-notes/{note_id}", json={"current_state": "new current state"}
    )
    assert response.status_code == 200

    data = response.json()
    assert data["current_state"] == "new current state"


async def test_delete_note_returns_204_for_existing_note_id(
    client: AsyncClient,
    test_project: list[Project],
    test_note: list[ProgressNote],
    as_owner_a: UUID,
):
    note_id = str(test_note[0].id)

    response = await client.delete(f"/progress-notes/{note_id}")
    assert response.status_code == 204


async def test_raises_404_for_creating_note_with_inaccessible_project(
    client: AsyncClient, test_project: list[Project], as_owner_b: UUID
):
    project_id = str(test_project[0].id)
    response = await client.post(
        "/progress-notes",
        json={
            "project_id": project_id,
            "current_state": "Just created main.py",
            "last_session": "Created github repo",
            "open_loops": ["Create roadmap", "Follow roadmap"],
            "next_actions": "Create fastapi instance",
            "important_context": "Read documentation",
            "blockers": ["Nothing"],
            "confidence": "high",
        },
    )

    assert response.status_code == 404
