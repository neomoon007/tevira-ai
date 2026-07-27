from fastapi import APIRouter, Depends

from src.app.schemas import ProjectCreate, ProjectRead
from src.app.services.projects import (
    create_project,
    delete_project,
    get_project,
    list_projects,
    rename_project,
)

router = APIRouter(prefix="/projects", tags=["Projects"])


# -- "/projects" --
@router.post("", status_code=201)
def create_project_endpoint(project: ProjectCreate) -> ProjectRead:
    return create_project(project)


@router.get("")
def list_projects_endpoint() -> list[ProjectRead]:
    return list_projects()


@router.get("/{project_id}")
def get_project_endpoint(project: ProjectRead = Depends(get_project)) -> ProjectRead:
    return get_project(project.id)


@router.patch("/{project_id}")
def rename_project_endpoint(
    new_title: ProjectCreate, project_id: ProjectRead = Depends(get_project)
) -> ProjectRead:
    return rename_project(new_title, project_id.id)


@router.delete("/{project_id}", status_code=204)
def delete_project_endpoint(project_id: ProjectRead = Depends(get_project)) -> None:
    delete_project(project_id.id)
