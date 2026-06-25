from fastapi import APIRouter, Depends
from src.app.schemas import ProjectCreate, ProjectRead
from src.app.validator import validate_project_id
from src.app.state.memory import projects_in_memory

router = APIRouter(prefix="/projects", tags=["Projects"])


# -- "/projects" --
@router.post("", status_code=201)
def create_project(project: ProjectCreate) -> ProjectRead:
    project_id = f"project_{len(projects_in_memory) + 1}"  # TODO change from length to be like tasks (separate counter)

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
