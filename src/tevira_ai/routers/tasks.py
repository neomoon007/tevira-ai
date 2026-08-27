import uuid

from fastapi import APIRouter

from src.tevira_ai.dependencies import CurrentUserId, DBSession
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
    task: TaskCreate, owner_id: CurrentUserId, db: DBSession
) -> TaskRead:
    return await create_task(owner_id, db, task)


@router.get("")
async def show_tasks_endpoint(
    owner_id: CurrentUserId,
    db: DBSession,
    project_id: uuid.UUID | None = None,
    task_id: uuid.UUID | None = None,
) -> list[TaskRead]:
    return await show_tasks(owner_id, db, project_id, task_id)


@router.patch("/{task_id}")
async def update_task_endpoint(
    task_id: uuid.UUID, updated_task: TaskUpdate, owner_id: CurrentUserId, db: DBSession
) -> TaskRead:
    return await update_task(owner_id, db, task_id, updated_task)


@router.delete("/{task_id}", status_code=204)
async def delete_task_endpoint(
    task_id: uuid.UUID, owner_id: CurrentUserId, db: DBSession
) -> None:
    await delete_task(owner_id, db, task_id)
