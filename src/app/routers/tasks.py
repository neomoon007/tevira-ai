from src.app.state.memory import tasks_in_memory
from src.app.validator import validate_project_id, get_project_tasks
from fastapi import HTTPException, APIRouter
from src.app.schemas import (
    TaskCreate,
    TaskRead,
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
def show_tasks(project_id: str = None, task_id: str = None) -> list[TaskRead]:
    if project_id is None and task_id is None:
        return tasks_in_memory

    if project_id is not None and task_id is None:
        validate_project_id(project_id)
        return get_project_tasks(project_id)

    if project_id is None and task_id is not None:
        matching_task = [task for task in tasks_in_memory if task.id == task_id]
        if not matching_task:
            raise HTTPException(
                status_code=404,
                detail=f"Error 404: Task {task_id} does not exist.",
            )
        return matching_task

    if project_id is not None and task_id is not None:
        validate_project_id(project_id)
        project_tasks = get_project_tasks(project_id)
        matching_task = [task for task in project_tasks if task.id == task_id]

        if not matching_task:
            raise HTTPException(
                status_code=404,
                detail=f"Error 404: Task '{task_id}' does not exist inside of '{project_id}'",
            )
        return matching_task
