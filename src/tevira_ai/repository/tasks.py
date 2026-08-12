from sqlalchemy import Integer, cast, delete, desc, func, select, update
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

    def get_highest_id(self, owner_id: str) -> int:
        clean_number = func.regexp_replace(Task.id, r"\D", "", "g")
        num_only_from_id = cast(clean_number, Integer)
        query = (
            select(num_only_from_id)
            .where(Task.owner_id == owner_id)
            .order_by(desc(num_only_from_id))
            .limit(1)
        )

        highest_task_id = self.session.scalars(query).first()

        return highest_task_id if highest_task_id is not None else 0

    def get_by_project(self, owner_id: str, project_id: str) -> list[Task]:
        tasks_list = list(
            self.session.scalars(
                select(Task).where(
                    Task.owner_id == owner_id, Task.project_id == project_id
                )
            ).all()
        )

        return tasks_list

    def get_by_id(self, owner_id: str, task_id: str) -> Task | None:
        task_result = self.session.scalars(
            select(Task).where(Task.owner_id == owner_id, Task.id == task_id)
        ).first()

        return task_result

    def update(self, owner_id: str, task_id: str, task_obj: dict) -> Task:
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

    def delete(self, owner_id: str, task_id: str):
        try:
            self.session.execute(
                delete(Task).where(Task.owner_id == owner_id, Task.id == task_id)
            )
            self.session.commit()
        except IntegrityError:
            self.session.rollback()

            raise


# TODO: missing except statement for NoResultFound exception, also there is no error handling on the service layer yet!!!
