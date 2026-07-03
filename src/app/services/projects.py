from src.app.state.memory import project_id_number, projects_in_memory
from src.app.schemas import ProjectCreate, ProjectRead
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
    global project_id_number
    project_id_number += 1

    project_id = f"project_{project_id_number}"

    new_project = ProjectRead(
        **project.model_dump(),
        id=project_id,
    )

    projects_in_memory[new_project.id] = new_project

    return new_project

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