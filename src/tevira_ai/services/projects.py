import uuid

from fastapi import HTTPException
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from src.tevira_ai.repository.projects import Project, ProjectRepository
from src.tevira_ai.schemas import ProjectCreate, ProjectRead

OWNER_ID = "local_user"  # TODO: Change from hardcoded to actual owner_id once authentication exists


def get_project(db: Session, project_id: uuid.UUID) -> ProjectRead:
    repository = ProjectRepository(db)

    project_from_db = repository.get_by_id(OWNER_ID, project_id)

    if not project_from_db:
        raise HTTPException(
            status_code=404,
            detail=f"Error 404: Project {project_id} does not exist.",
        )

    return ProjectRead.model_validate(project_from_db)


def create_project(db: Session, project: ProjectCreate) -> ProjectRead:
    repository = ProjectRepository(db)

    project_in = Project(
        **project.model_dump(),
        owner_id=OWNER_ID,
    )

    project_out = repository.create(project_in)

    return ProjectRead.model_validate(project_out)


def list_projects(db: Session) -> list[ProjectRead]:
    repository = ProjectRepository(db)

    projects_from_db = repository.get_all(OWNER_ID)

    return [ProjectRead.model_validate(project) for project in projects_from_db]


def rename_project(
    db: Session, new_title: ProjectCreate, project_id: uuid.UUID
) -> ProjectRead:
    get_project(db, project_id)

    renamed_project = ProjectRead(
        **new_title.model_dump(),
        id=project_id,
    )

    repository = ProjectRepository(db)

    project_result = repository.rename(OWNER_ID, renamed_project)

    return ProjectRead.model_validate(project_result)


def delete_project(db: Session, project_id: uuid.UUID) -> None:
    try:
        repository = ProjectRepository(db)

        repository.delete(OWNER_ID, project_id)
    except IntegrityError:
        raise HTTPException(
            status_code=409,
            detail=f"Project: {project_id} is currently linked to other resources such as notes or tasks.",
        )
