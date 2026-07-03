from src.app.state.memory import (
    tasks_in_memory,
)
from src.app.schemas import TaskRead, ProjectRead
from fastapi import HTTPException


# --- ROUTE VALIDATION ---


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