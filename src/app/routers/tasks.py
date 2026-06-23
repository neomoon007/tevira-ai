from src.app.state.memory import tasks_in_memory
from src.app.validator import validate_project_id, get_project_tasks, get_task_by_id
from fastapi import HTTPException, APIRouter
from src.app.schemas import (
    TaskCreate,
    TaskRead,
    TaskUpdate,
)

router = APIRouter(prefix="/tasks", tags=["Tasks"])


# -- "/tasks" --
@router.post("", status_code=201)
def create_task(task: TaskCreate) -> TaskRead:
    task_id = f"task_{len(tasks_in_memory) + 1}"

    new_task = TaskRead(
        **task.model_dump(),  # Dumps all `task` fields here, no need to type them manually.
        id=task_id,
        status="open",
    )

    tasks_in_memory.append(new_task)

    return new_task


@router.get("")
def show_tasks(project_id: str = None, task_id: str = None) -> list[TaskRead]: # type: ignore
    if project_id is None and task_id is None:
        return tasks_in_memory

    if project_id is not None and task_id is None:
        validate_project_id(project_id)
        return get_project_tasks(project_id)

    if project_id is None and task_id is not None:
        return [get_task_by_id(task_id)]

    if project_id is not None and task_id is not None:
        validate_project_id(project_id)
        project_tasks = get_project_tasks(project_id)
        return [get_task_by_id(task_id, project_tasks)]
    
# @router.patch("/{task_id}")
# def update_task(updated_task: TaskUpdate) -> TaskRead:
    # check if given id matched any of the IDs inside tasks dictionary.
    # if they match, then replace that item with the new values only keeping the old ones if the new value is None.
    # get the taskupdate fields, loop through them and extract the non none keys and value when values arent none,