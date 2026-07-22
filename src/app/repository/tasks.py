from sqlalchemy.orm import Session
from sqlalchemy import select, func, desc, cast, Integer
from src.app.db.models import Task


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
