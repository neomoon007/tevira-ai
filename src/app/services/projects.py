from src.app.state.memory import projects_in_memory
from src.app.schemas import ProjectCreate, ProjectRead
from src.app.db.database import SessionLocal
from src.app.repository.projects import ProjectRepository, Project
from fastapi import HTTPException


def get_project_by_id(project_id: str) -> ProjectRead:
    return projects_in_memory[project_id]


def get_project(project_id: str) -> ProjectRead:
    if project_id == "":
        raise HTTPException(
            status_code=400, detail="Error 400: Empty string where input is required"
        )

    try:
        project = projects_in_memory[project_id]
        return project
    except KeyError as project_missing:
        raise HTTPException(
            status_code=404,
            detail=f"Error 404: Project {project_missing} does not exist.",
        )


def create_project(project: ProjectCreate) -> ProjectRead:
    db = SessionLocal()

    try:
        owner_id = "local_user"
        repository = ProjectRepository(db)

        id_num_from_db = repository.get_highest_id(owner_id)

        project_id = f"project_{id_num_from_db + 1}"

        project_in = Project(
            **project.model_dump(),
            id=project_id,
            owner_id=owner_id,  # TODO: Change from hardcoded to actual owner_id once authentication exists
        )

        project_out = repository.create(
            project_in
        )  # WIP: So far only accepts "project_1 as project_id"
    finally:
        db.close()

    return ProjectRead.model_validate(project_out)
    # global project_id_number
    # project_id_number += 1

    # project_id = f"project_{project_id_number}"

    # new_project = ProjectRead(
    #     **project.model_dump(),
    #     id=project_id,
    # )

    # projects_in_memory[new_project.id] = new_project

    # return new_project


def list_projects() -> list[ProjectRead]:
    return list(projects_in_memory.values())


def rename_project(new_title: ProjectCreate, project_id: str) -> ProjectRead:
    renamed_project = ProjectRead(
        **new_title.model_dump(),
        id=project_id,
    )

    projects_in_memory[renamed_project.id] = renamed_project

    return renamed_project


def delete_project(project_id: str) -> None:
    del projects_in_memory[project_id]
