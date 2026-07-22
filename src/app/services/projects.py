from src.app.state.memory import projects_in_memory
from src.app.schemas import ProjectCreate, ProjectRead
from src.app.db.database import SessionLocal
from src.app.repository.projects import ProjectRepository, Project
from fastapi import HTTPException

OWNER_ID = "local_user"  # TODO: Change from hardcoded to actual owner_id once authentication exists


def get_project(project_id: str) -> ProjectRead:
    db = SessionLocal()

    if project_id == "":
        raise HTTPException(
            status_code=400, detail="Error 400: Empty string where input is required"
        )

    try:
        repository = ProjectRepository(db)

        project_from_db = repository.get_by_id(OWNER_ID, project_id)

        if not project_from_db:
            raise HTTPException(
                status_code=404,
                detail=f"Error 404: Project {project_id} does not exist.",
            )

    finally:
        db.close()

    return ProjectRead.model_validate(project_from_db)


def create_project(project: ProjectCreate) -> ProjectRead:
    db = SessionLocal()

    try:
        repository = ProjectRepository(db)

        id_num_from_db = repository.get_highest_id(OWNER_ID)

        project_id = f"project_{id_num_from_db + 1}"

        project_in = Project(
            **project.model_dump(),
            id=project_id,
            owner_id=OWNER_ID,
        )

        project_out = repository.create(project_in)
    finally:
        db.close()

    return ProjectRead.model_validate(project_out)


def list_projects() -> list[ProjectRead]:
    db = SessionLocal()

    try:
        repository = ProjectRepository(db)

        projects_from_db = repository.get_all(OWNER_ID)
    finally:
        db.close()

    return [ProjectRead.model_validate(project) for project in projects_from_db]


def rename_project(new_title: ProjectCreate, project_id: str) -> ProjectRead:
    renamed_project = ProjectRead(
        **new_title.model_dump(),
        id=project_id,
    )

    db = SessionLocal()

    try:
        repository = ProjectRepository(db)

        project_result = repository.rename(OWNER_ID, renamed_project)
    finally:
        db.close()

    return ProjectRead.model_validate(project_result)


def delete_project(project_id: str) -> None:
    del projects_in_memory[project_id]
