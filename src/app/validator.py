from src.app.state.memory import (
    projects_in_memory,
    tasks_in_memory,
    progress_notes_in_memory,
)
from src.app.schemas import TaskRead
from fastapi import HTTPException


# --- ROUTE VALIDATION ---
def validate_project_id(project_id: str):
    if project_id == "":
        raise HTTPException(
            status_code=400, detail="Error 400: Empty string where input is required"
        )
    try:
        projects_in_memory[project_id]
        return project_id
    except Exception as project_missing:
        raise HTTPException(
            status_code=404,
            detail=f"Error 404: Project {project_missing} does not exist.",
        )


def validate_progress_note(project_id: str):
    if any(note.project_id == project_id for note in progress_notes_in_memory):
        return project_id
    else:
        raise HTTPException(
            status_code=404,
            detail="Error 404: No progress note found for this project.",
        )


def get_project_tasks(project_id) -> list[TaskRead]:
    return [
        task
        for task in tasks_in_memory
        if task.project_id == project_id and task.status == "open"
    ]
