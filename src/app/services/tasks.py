from src.app.schemas import TaskCreate, TaskRead, NonEmptyString, TaskUpdate
from src.app.db.models import Task
from src.app.db.database import SessionLocal
from src.app.repository.tasks import TaskRepository
from sqlalchemy.exc import NoResultFound, IntegrityError
from fastapi import HTTPException

OWNER_ID = "local_user"


def get_tasks_by_project(project_id: str) -> list[TaskRead]:
    db = SessionLocal()

    try:
        repository = TaskRepository(db)

        tasks_from_db = repository.get_by_project(OWNER_ID, project_id)
    finally:
        db.close()

    return [TaskRead.model_validate(task) for task in tasks_from_db]


def get_task_by_id(task_id: str) -> TaskRead:
    db = SessionLocal()

    try:
        repository = TaskRepository(db)

        task_from_db = repository.get_by_id(OWNER_ID, task_id)

        if not task_from_db:
            raise HTTPException(
                status_code=404, detail=f"Task: {task_id} does not exist."
            )
    finally:
        db.close()

    return TaskRead.model_validate(task_from_db)


def get_important_task(project_id: str) -> TaskRead | str:
    tasks_db = get_tasks_by_project(project_id)
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


def create_task(task: TaskCreate) -> TaskRead:
    db = SessionLocal()

    try:
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
    finally:
        db.close()

    return TaskRead.model_validate(task_out)


def get_all_tasks() -> list[TaskRead]:
    db = SessionLocal()

    try:
        repository = TaskRepository(db)

        tasks_from_db = repository.get_all(OWNER_ID)
    finally:
        db.close()

    return [TaskRead.model_validate(task) for task in tasks_from_db]


def show_tasks(
    project_id: str | None = None, task_id: str | None = None
) -> list[TaskRead]:  # type: ignore
    if project_id is None and task_id is None:
        return get_all_tasks()

    if project_id is not None and task_id is None:
        return get_tasks_by_project(project_id)

    if (
        project_id is None
        and task_id is not None
        or project_id is not None
        and task_id is not None
    ):
        return [get_task_by_id(task_id)]


def update_task(task_id: NonEmptyString, updated_task: TaskUpdate) -> TaskRead:
    db = SessionLocal()
    update_data = updated_task.model_dump(exclude_unset=True)

    try:
        repository = TaskRepository(db)

        task_from_db = repository.update(OWNER_ID, task_id, update_data)
    except NoResultFound:
        raise HTTPException(status_code=404, detail=f"Task: {task_id} does not exist.")
    finally:
        db.close()

    return TaskRead.model_validate(task_from_db)


def delete_task(task_id: NonEmptyString) -> None:
    db = SessionLocal()

    try:
        repository = TaskRepository(db)

        repository.delete(OWNER_ID, task_id)
    finally:
        db.close()
