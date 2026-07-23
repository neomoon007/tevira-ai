from src.app.services.tasks import (
    create_task,
    show_tasks,
    update_task,
    delete_task,
    get_task_by_id,
)
from fastapi import APIRouter, Depends
from src.app.schemas import (
    TaskCreate,
    TaskRead,
    TaskUpdate,
    NonEmptyString,
)

router = APIRouter(prefix="/tasks", tags=["Tasks"])


# -- "/tasks" --
@router.post("", status_code=201)
def create_task_endpoint(task: TaskCreate) -> TaskRead:
    return create_task(task)


@router.get("")
def show_tasks_endpoint(
    project_id: str | None = None, task_id: str | None = None
) -> list[TaskRead]:
    return show_tasks(project_id, task_id)


@router.patch("/{task_id}")
def update_task_endpoint(task_id: NonEmptyString, updated_task: TaskUpdate) -> TaskRead:
    return update_task(task_id, updated_task)


@router.delete("/{task_id}", status_code=204)
def delete_task_endpoint(task_id: str = Depends(get_task_by_id)) -> None:
    delete_task(task_id)
