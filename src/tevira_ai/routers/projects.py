import uuid

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

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
def create_project_endpoint(
    project: ProjectCreate, db: Session = Depends(get_db)
) -> ProjectRead:
    return create_project(db, project)


@router.get("")
def list_projects_endpoint(db: Session = Depends(get_db)) -> list[ProjectRead]:
    return list_projects(db)


@router.get("/{project_id}")
def get_project_endpoint(
    project_id: uuid.UUID, db: Session = Depends(get_db)
) -> ProjectRead:
    return get_project(db, project_id)


@router.patch("/{project_id}")
def rename_project_endpoint(
    new_title: ProjectCreate,
    project_id: uuid.UUID,
    db: Session = Depends(get_db),
) -> ProjectRead:
    return rename_project(db, new_title, project_id)


@router.delete("/{project_id}", status_code=204)
def delete_project_endpoint(
    project_id: uuid.UUID, db: Session = Depends(get_db)
) -> None:
    delete_project(db, project_id)
