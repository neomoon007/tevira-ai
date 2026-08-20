import uuid

from sqlalchemy.ext.asyncio import AsyncSession

from src.tevira_ai.db.models import Task
from src.tevira_ai.exceptions import ResourceNotFoundError
from src.tevira_ai.repository.tasks import TaskRepository
from src.tevira_ai.schemas import TaskCreate, TaskRead, TaskUpdate
from src.tevira_ai.services.projects import get_project

OWNER_ID = "local_user"


async def get_tasks_by_project(
    db: AsyncSession, project_id: uuid.UUID
) -> list[TaskRead]:
    repository = TaskRepository(db)

    tasks_from_db = await repository.get_by_project(OWNER_ID, project_id)

    return [TaskRead.model_validate(task) for task in tasks_from_db]


async def get_task_by_id(db: AsyncSession, task_id: uuid.UUID) -> TaskRead:
    repository = TaskRepository(db)

    task_from_db = await repository.get_by_id(OWNER_ID, task_id)

    if not task_from_db:
        raise ResourceNotFoundError(
            resource_type="Task",
            resource_id=str(task_id),
        )

    return TaskRead.model_validate(task_from_db)


async def get_important_task(db: AsyncSession, project_id: uuid.UUID) -> TaskRead | str:
    tasks_db = await get_tasks_by_project(db, project_id)
    priority_list = ["high", "medium", "low"]
    recommended_task: TaskRead | None = None

    for p in priority_list:
        recommended_task = next(
            (task for task in tasks_db if task.priority == p and task.status == "open"),
            None,
        )

        if recommended_task is not None:
            return recommended_task

    return "No open next action found."


async def create_task(db: AsyncSession, task: TaskCreate) -> TaskRead:
    await get_project(db, task.project_id)

    repository = TaskRepository(db)

    task_in = Task(
        **task.model_dump(),
        status="open",
        owner_id=OWNER_ID,
    )

    task_out = await repository.create(task_in)

    return TaskRead.model_validate(task_out)


async def get_all_tasks(db: AsyncSession) -> list[TaskRead]:
    repository = TaskRepository(db)

    tasks_from_db = await repository.get_all(OWNER_ID)

    return [TaskRead.model_validate(task) for task in tasks_from_db]


async def show_tasks(
    db: AsyncSession,
    project_id: uuid.UUID | None = None,
    task_id: uuid.UUID | None = None,
) -> list[TaskRead]:
    if project_id is None and task_id is None:
        return await get_all_tasks(db)

    if project_id is not None and task_id is None:
        await get_project(db, project_id)
        return await get_tasks_by_project(db, project_id)

    if (
        project_id is None
        and task_id is not None
        or project_id is not None
        and task_id is not None
    ):
        return [await get_task_by_id(db, task_id)]

    return []


async def update_task(
    db: AsyncSession, task_id: uuid.UUID, updated_task: TaskUpdate
) -> TaskRead:
    if updated_task.project_id:
        await get_project(db, updated_task.project_id)

    update_data = updated_task.model_dump(exclude_unset=True)
    repository = TaskRepository(db)
    task_from_db = await repository.update(OWNER_ID, task_id, update_data)

    if not task_from_db:
        raise ResourceNotFoundError(
            resource_type="Task",
            resource_id=str(task_id),
        )

    return TaskRead.model_validate(task_from_db)


async def delete_task(db: AsyncSession, task_id: uuid.UUID) -> None:
    await get_task_by_id(db, task_id)

    repository = TaskRepository(db)
    await repository.delete(OWNER_ID, task_id)
