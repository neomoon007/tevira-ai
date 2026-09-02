import uuid

import pytest
from httpx import AsyncClient
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.tevira_ai.db.models import Project
from src.tevira_ai.dependencies import get_current_owner_id
from src.tevira_ai.exceptions import ResourceNotFoundError
from src.tevira_ai.services.projects import get_project


async def test_can_insert_project(db_session: AsyncSession):
    owner_id = get_current_owner_id()
    title = "foo"

    project = Project(owner_id=owner_id, title=title)

    db_session.add(project)
    await db_session.commit()

    saved = await db_session.scalar(
        select(Project).where(
            Project.owner_id == owner_id,
            Project.title == title,
        )
    )

    assert saved is not None


async def test_validate_project_id_accepts_existing_project(
    db_session: AsyncSession, test_project: list[Project]
):
    project_id = test_project[0].id
    response = await get_project(
        owner_id=get_current_owner_id(),
        db=db_session,
        project_id=project_id,
    )

    assert response.id == project_id


async def test_validate_project_id_raises_404_for_non_existing_project(
    db_session: AsyncSession, test_project: list[Project]
):
    non_existent_id = uuid.uuid7()

    with pytest.raises(ResourceNotFoundError) as exception_info:
        await get_project(
            owner_id=get_current_owner_id(),
            db=db_session,
            project_id=non_existent_id,
        )

    assert exception_info.value.status_code == 404


async def test_create_project_accepts_valid_project_object(client: AsyncClient):
    response = await client.post("/projects", json={"title": "Magnum Opus"})
    assert response.status_code == 201

    data = response.json()
    assert data["title"] == "Magnum Opus"


async def test_show_project_returns_200_for_existing_project(
    client: AsyncClient, test_project: list[Project]
):
    project_id = str(test_project[0].id)
    response = await client.get(f"/projects/{project_id}")

    assert response.status_code == 200


async def test_show_project_returns_404_for_non_existing_project(
    client: AsyncClient, test_project: list[Project]
):
    non_existent_id = uuid.uuid7()
    response = await client.get(f"/projects/{non_existent_id}")

    assert response.status_code == 404


async def test_rename_project_returns_200_for_valid_request(
    client: AsyncClient, test_project: list[Project]
):
    project_id = str(test_project[0].id)
    response = await client.patch(
        f"/projects/{project_id}", json={"title": "This project title was renamed"}
    )

    assert response.status_code == 200

    data = response.json()
    assert data["title"] == "This project title was renamed"
    assert data["id"] == project_id


async def test_delete_project_returns_204(
    client: AsyncClient, test_project: list[Project]
):
    project_id = str(test_project[0].id)
    response = await client.delete(f"/projects/{project_id}")

    assert response.status_code == 204


async def test_delete_project_returns_404_for_non_existing_project(
    client: AsyncClient, test_project: list[Project]
):
    project_id = str(uuid.uuid7())
    response = await client.delete(f"/projects/{project_id}")

    assert response.status_code == 404
