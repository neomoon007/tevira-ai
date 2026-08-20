import uuid

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.tevira_ai.db.database import get_db
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
    project: ProjectCreate, db: AsyncSession = Depends(get_db)
) -> ProjectRead:
    return await create_project(db, project)


@router.get("")
async def list_projects_endpoint(
    db: AsyncSession = Depends(get_db),
) -> list[ProjectRead]:
    return await list_projects(db)


@router.get("/{project_id}")
async def get_project_endpoint(
    project_id: uuid.UUID, db: AsyncSession = Depends(get_db)
) -> ProjectRead:
    return await get_project(db, project_id)


@router.patch("/{project_id}")
async def rename_project_endpoint(
    new_title: ProjectCreate,
    project_id: uuid.UUID,
    db: AsyncSession = Depends(get_db),
) -> ProjectRead:
    return await rename_project(db, new_title, project_id)


@router.delete("/{project_id}", status_code=204)
async def delete_project_endpoint(
    project_id: uuid.UUID, db: AsyncSession = Depends(get_db)
) -> None:
    await delete_project(db, project_id)
