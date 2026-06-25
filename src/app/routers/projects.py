from fastapi import APIRouter, Depends
from src.app.schemas import ProjectCreate, ProjectRead
from src.app.validator import validate_project_id
from src.app.state.memory import projects_in_memory, project_id_number

router = APIRouter(prefix="/projects", tags=["Projects"])


# -- "/projects" --
@router.post("", status_code=201)
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


@router.get("")
def list_projects() -> list[ProjectRead]:
    # turn dict into list and only output the objects without the key from the projects dict
    return list(projects_in_memory.values())


@router.get("/{project_id}")
def show_project(project_id: str = Depends(validate_project_id)) -> ProjectRead:
    return projects_in_memory[project_id]


@router.patch("/{project_id}")
def rename_project(
    new_title: ProjectCreate, project_id: str = Depends(validate_project_id)
) -> ProjectRead:
    renamed_project = ProjectRead(
        **new_title.model_dump(),
        id=project_id,
    )

    projects_in_memory[renamed_project.id] = renamed_project

    return renamed_project


@router.delete("/{project_id}", status_code=204)
def delete_task(project_id: str = Depends(validate_project_id)):
    del projects_in_memory[project_id]

    return
