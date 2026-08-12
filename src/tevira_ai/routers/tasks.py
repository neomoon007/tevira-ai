from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from src.tevira_ai.db.database import get_db
from src.tevira_ai.schemas import (
    TaskCreate,
    TaskRead,
    TaskUpdate,
)
from src.tevira_ai.services.tasks import (
    create_task,
    delete_task,
    get_task_by_id,
    show_tasks,
    update_task,
)

router = APIRouter(prefix="/tasks", tags=["Tasks"])


# -- "/tasks" --
@router.post("", status_code=201)
def create_task_endpoint(task: TaskCreate, db: Session = Depends(get_db)) -> TaskRead:
    return create_task(db, task)


@router.get("")
def show_tasks_endpoint(
    db: Session = Depends(get_db),
    project_id: str | None = None,
    task_id: str | None = None,
) -> list[TaskRead]:
    return show_tasks(db, project_id, task_id)


@router.patch("/{task_id}")
def update_task_endpoint(
    task_id: str, updated_task: TaskUpdate, db: Session = Depends(get_db)
) -> TaskRead:
    return update_task(db, task_id, updated_task)


@router.delete("/{task_id}", status_code=204)
def delete_task_endpoint(task_id: str, db: Session = Depends(get_db)) -> None:
    if not get_task_by_id(db, task_id):
        raise HTTPException(status_code=404, detail=f"Task '{task_id}' does not exist.")
    delete_task(db, task_id)
