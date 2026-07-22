from src.app.schemas import TaskCreate, TaskRead, NonEmptyString, TaskUpdate
from src.app.db.models import Task
from src.app.db.database import SessionLocal
from src.app.repository.tasks import TaskRepository
from src.app.state.memory import tasks_in_memory
from src.app.services.projects import get_project
from fastapi import HTTPException


def get_project_tasks(project_id) -> list[TaskRead]:
    return [
        task
        for task in tasks_in_memory
        if task.project_id == project_id and task.status == "open"
    ]


def get_task_by_id(task_id: str, database: list | None = None) -> TaskRead:
    tasks_list = database if database is not None else tasks_in_memory

    matching_task = next((task for task in tasks_list if task.id == task_id), None)
    if not matching_task:
        raise HTTPException(
            status_code=404,
            detail=f"Error 404: Task '{task_id}' does not exist.",
        )
    return matching_task


def get_important_task(project_id: str) -> TaskRead | str:
    tasks_db = get_project_tasks(project_id)
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
        owner_id = "local_user"
        repository = TaskRepository(db)

        id_num_from_db = repository.get_highest_id(owner_id)

        task_id = f"task_{id_num_from_db + 1}"

        task_in = Task(
            **task.model_dump(),
            id=task_id,
            status="open",
            owner_id=owner_id,  # TODO: Change from hardcoded to actual owner_id once authentication exists
        )

        task_out = repository.create(
            task_in
        )  # WIP: So far only accepts "project_1 as project_id"
    finally:
        db.close()

    return TaskRead.model_validate(task_out)


def show_tasks(
    project_id: str | None = None, task_id: str | None = None
) -> list[TaskRead]:  # type: ignore
    if project_id is None and task_id is None:
        return tasks_in_memory

    if project_id is not None and task_id is None:
        get_project(project_id)
        return get_project_tasks(project_id)

    if project_id is None and task_id is not None:
        return [get_task_by_id(task_id)]

    if project_id is not None and task_id is not None:
        get_project(project_id)
        project_tasks = get_project_tasks(project_id)
        return [get_task_by_id(task_id, project_tasks)]


def update_task(task_id: NonEmptyString, updated_task: TaskUpdate) -> TaskRead:
    matching_task = get_task_by_id(task_id)
    merged_task = {
        **matching_task.model_dump(),
        **updated_task.model_dump(exclude_none=True),
    }

    task_index = tasks_in_memory.index(matching_task)
    tasks_in_memory[task_index] = TaskRead(**merged_task)

    return TaskRead(**merged_task)


def delete_task(task_id: NonEmptyString) -> None:
    matching_task = get_task_by_id(task_id)
    task_index = tasks_in_memory.index(matching_task)
    del tasks_in_memory[task_index]
    # TODO: change the parameter from str type to a validation (similar to Depends(validate_project_id(project_id) or NonEmptyString at least)
