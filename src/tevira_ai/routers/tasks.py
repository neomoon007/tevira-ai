import uuid

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.tevira_ai.db.database import get_db
from src.tevira_ai.schemas import (
    TaskCreate,
    TaskRead,
    TaskUpdate,
)
from src.tevira_ai.services.tasks import (
    create_task,
    delete_task,
    show_tasks,
    update_task,
)

router = APIRouter(prefix="/tasks", tags=["Tasks"])


# -- "/tasks" --
@router.post("", status_code=201)
async def create_task_endpoint(
    task: TaskCreate, db: AsyncSession = Depends(get_db)
) -> TaskRead:
    return await create_task(db, task)


@router.get("")
async def show_tasks_endpoint(
    db: AsyncSession = Depends(get_db),
    project_id: uuid.UUID | None = None,
    task_id: uuid.UUID | None = None,
) -> list[TaskRead]:
    return await show_tasks(db, project_id, task_id)


@router.patch("/{task_id}")
async def update_task_endpoint(
    task_id: uuid.UUID, updated_task: TaskUpdate, db: AsyncSession = Depends(get_db)
) -> TaskRead:
    return await update_task(db, task_id, updated_task)


@router.delete("/{task_id}", status_code=204)
async def delete_task_endpoint(
    task_id: uuid.UUID, db: AsyncSession = Depends(get_db)
) -> None:
    await delete_task(db, task_id)
