from uuid import UUID

from sqlalchemy import delete, select, update
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from src.tevira_ai.db.models import Task
from src.tevira_ai.exceptions import ResourceInUseError


class TaskRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create(self, task: Task) -> Task:
        self.session.add(task)
        await self.session.commit()
        await self.session.refresh(task)

        return task

    async def get_all(self, owner_id: UUID) -> list[Task]:
        tasks_list = await self.session.scalars(
            select(Task).where(Task.owner_id == owner_id)
        )

        return list(tasks_list.all())

    async def get_by_project(self, owner_id: UUID, project_id: UUID) -> list[Task]:
        tasks_list = await self.session.scalars(
            select(Task).where(Task.owner_id == owner_id, Task.project_id == project_id)
        )

        return list(tasks_list.all())

    async def get_by_id(self, owner_id: UUID, task_id: UUID) -> Task | None:
        task_result = await self.session.scalar(
            select(Task).where(Task.owner_id == owner_id, Task.id == task_id)
        )

        return task_result

    async def update(
        self, owner_id: UUID, task_id: UUID, task_obj: dict
    ) -> Task | None:
        updated_task = await self.session.scalar(
            update(Task)
            .where(Task.owner_id == owner_id, Task.id == task_id)
            .values(**task_obj)
            .returning(Task)
        )

        await self.session.commit()
        return updated_task

    async def delete(self, owner_id: UUID, task_id: UUID):
        try:
            await self.session.execute(
                delete(Task).where(Task.owner_id == owner_id, Task.id == task_id)
            )
            await self.session.commit()
        except IntegrityError:
            await self.session.rollback()

            raise ResourceInUseError(
                resource_type="Task",
                resource_id=str(task_id),
            )


# TODO: missing except statement for NoResultFound exception, also there is no error handling on the service layer yet!!!
