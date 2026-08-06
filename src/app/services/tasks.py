from fastapi import HTTPException
from sqlalchemy.exc import NoResultFound
from sqlalchemy.orm import Session

from src.app.db.models import Task
from src.app.repository.tasks import TaskRepository
from src.app.schemas import NonEmptyString, TaskCreate, TaskRead, TaskUpdate
from src.app.services.projects import get_project

OWNER_ID = "local_user"


def get_tasks_by_project(db: Session, project_id: str) -> list[TaskRead]:
    repository = TaskRepository(db)

    tasks_from_db = repository.get_by_project(OWNER_ID, project_id)

    return [TaskRead.model_validate(task) for task in tasks_from_db]


def get_task_by_id(db: Session, task_id: str) -> TaskRead:
    repository = TaskRepository(db)

    task_from_db = repository.get_by_id(OWNER_ID, task_id)

    if not task_from_db:
        raise HTTPException(
            status_code=404, detail=f"Error 404: {task_id} does not exist."
        )

    return TaskRead.model_validate(task_from_db)


def get_important_task(db: Session, project_id: str) -> TaskRead | str:
    tasks_db = get_tasks_by_project(db, project_id)
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


def create_task(db: Session, task: TaskCreate) -> TaskRead:
    get_project(db, task.project_id)

    repository = TaskRepository(db)

    id_num_from_db = repository.get_highest_id(OWNER_ID)

    task_id = f"task_{id_num_from_db + 1}"

    task_in = Task(
        **task.model_dump(),
        id=task_id,
        status="open",
        owner_id=OWNER_ID,
    )

    task_out = repository.create(task_in)

    return TaskRead.model_validate(task_out)


def get_all_tasks(db: Session) -> list[TaskRead]:
    repository = TaskRepository(db)

    tasks_from_db = repository.get_all(OWNER_ID)

    return [TaskRead.model_validate(task) for task in tasks_from_db]


def show_tasks(
    db: Session, project_id: str | None = None, task_id: str | None = None
) -> list[TaskRead]:  # type: ignore
    if project_id is None and task_id is None:
        return get_all_tasks(db)

    if project_id is not None and task_id is None:
        if not get_project(db, project_id):
            raise HTTPException(
                status_code=404, detail=f"Project '{project_id}' does not exist."
            )
        return get_tasks_by_project(db, project_id)

    if (
        project_id is None
        and task_id is not None
        or project_id is not None
        and task_id is not None
    ):
        return [get_task_by_id(db, task_id)]


def update_task(
    db: Session, task_id: NonEmptyString, updated_task: TaskUpdate
) -> TaskRead:
    if updated_task.project_id:
        get_project(db, updated_task.project_id)

    update_data = updated_task.model_dump(exclude_unset=True)

    try:
        repository = TaskRepository(db)

        task_from_db = repository.update(OWNER_ID, task_id, update_data)
    except NoResultFound:
        raise HTTPException(status_code=404, detail=f"Task: {task_id} does not exist.")

    return TaskRead.model_validate(task_from_db)


def delete_task(db: Session, task_id: NonEmptyString) -> None:
    repository = TaskRepository(db)

    repository.delete(OWNER_ID, task_id)
