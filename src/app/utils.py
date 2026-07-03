from src.app.state.memory import (
    projects_in_memory,
    tasks_in_memory,
    progress_notes_in_memory,
)
from src.app.schemas import TaskRead, ProgressNoteRead, CaptureRead, CreateProgressNoteProposal, CreateTaskProposal, ProposedAction
from src.app.parser import parse_note
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


def get_task_by_id(task_id: str, database: list | None = None) -> TaskRead:
    tasks_list = database if database is not None else tasks_in_memory

    matching_task = next((task for task in tasks_list if task.id == task_id), None)
    if not matching_task:
        raise HTTPException(
            status_code=404,
            detail=f"Error 404: Task '{task_id}' does not exist.",
        )
    return matching_task


def get_note_by_id(note_id: str, database: list | None = None) -> ProgressNoteRead:
    notes_list = database if database is not None else progress_notes_in_memory

    matching_note = next((note for note in notes_list if note.id == note_id), None)
    if not matching_note:
        raise HTTPException(
            status_code=404,
            detail=f"Error 404: Note '{note_id}' does not exist.",
        )
    return matching_note


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

def capture_from_text(raw_input) -> CaptureRead:
    parsed_input = parse_note(raw_input, projects_in_memory)

    return CaptureRead(
        raw_text=raw_input,
        parsed=parsed_input,
        proposed_actions=[
            ProposedAction(
                type="create_task",
                data=CreateTaskProposal(
                    title=parsed_input.title,
                    due_date_hint=parsed_input.due_date_hint
                    )
            ),
            ProposedAction(
                type="create_progress_note",
                data=CreateProgressNoteProposal(
                    next_action=parsed_input.next_action_hint
                    )
                ),
        ],
    )