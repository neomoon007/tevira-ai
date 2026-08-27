import uuid

from fastapi import APIRouter

from src.tevira_ai.dependencies import CurrentUserId, DBSession
from src.tevira_ai.schemas import ProjectCreate, ProjectRead
from src.tevira_ai.services.projects import (
    create_project,
    delete_project,
    get_project,
    list_projects,
    rename_project,
)

router = APIRouter(prefix="/projects", tags=["Projects"])


# -- "/projects" --
@router.post("", status_code=201)
async def create_project_endpoint(
    project: ProjectCreate, owner_id: CurrentUserId, db: DBSession
) -> ProjectRead:
    return await create_project(owner_id, db, project)


@router.get("")
async def list_projects_endpoint(
    owner_id: CurrentUserId, db: DBSession
) -> list[ProjectRead]:
    return await list_projects(owner_id, db)


@router.get("/{project_id}")
async def get_project_endpoint(
    project_id: uuid.UUID, owner_id: CurrentUserId, db: DBSession
) -> ProjectRead:
    return await get_project(owner_id, db, project_id)


@router.patch("/{project_id}")
async def rename_project_endpoint(
    new_title: ProjectCreate,
    project_id: uuid.UUID,
    owner_id: CurrentUserId,
    db: DBSession,
) -> ProjectRead:
    return await rename_project(owner_id, db, new_title, project_id)


@router.delete("/{project_id}", status_code=204)
async def delete_project_endpoint(
    project_id: uuid.UUID, owner_id: CurrentUserId, db: DBSession
) -> None:
    await delete_project(owner_id, db, project_id)
