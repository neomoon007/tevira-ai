import uuid

from sqlalchemy import delete, select, update
from sqlalchemy.exc import IntegrityError, NoResultFound
from sqlalchemy.orm import Session

from src.tevira_ai.db.models import Task


class TaskRepository:
    def __init__(self, session: Session):
        self.session = session

    def create(self, task: Task) -> Task:
        self.session.add(task)
        self.session.commit()
        self.session.refresh(task)

        return task

    def get_all(self, owner_id: str) -> list[Task]:
        tasks_list = list(
            self.session.scalars(select(Task).where(Task.owner_id == owner_id)).all()
        )

        return tasks_list

    def get_by_project(self, owner_id: str, project_id: uuid.UUID) -> list[Task]:
        tasks_list = list(
            self.session.scalars(
                select(Task).where(
                    Task.owner_id == owner_id, Task.project_id == project_id
                )
            ).all()
        )

        return tasks_list

    def get_by_id(self, owner_id: str, task_id: uuid.UUID) -> Task | None:
        task_result = self.session.scalars(
            select(Task).where(Task.owner_id == owner_id, Task.id == task_id)
        ).first()

        return task_result

    def update(self, owner_id: str, task_id: uuid.UUID, task_obj: dict) -> Task:
        try:
            updated_task = self.session.execute(
                update(Task)
                .where(Task.owner_id == owner_id, Task.id == task_id)
                .values(**task_obj)
                .returning(Task)
            ).scalar_one()

            self.session.commit()
            return updated_task
        except NoResultFound:
            self.session.rollback()
            raise

    def delete(self, owner_id: str, task_id: uuid.UUID):
        try:
            self.session.execute(
                delete(Task).where(Task.owner_id == owner_id, Task.id == task_id)
            )
            self.session.commit()
        except IntegrityError:
            self.session.rollback()

            raise


# TODO: missing except statement for NoResultFound exception, also there is no error handling on the service layer yet!!!
