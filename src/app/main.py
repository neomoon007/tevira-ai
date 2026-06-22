from fastapi import FastAPI, Depends
from src.app.state import projects_in_memory, progress_notes_in_memory
from src.app.validator import (  # TODO: create a separate folder for validator.py and state.py
    validate_project_id,
    validate_progress_note,
    get_project_tasks,
)
from src.app.routers import tasks, health, projects, progress_notes
from operator import attrgetter
from src.app.schemas import (
    ContextRead,
)

app = FastAPI(title="Tevira-AI")

# --- ROUTERS ---
app.include_router(tasks.router)
app.include_router(health.router)
app.include_router(projects.router)
app.include_router(progress_notes.router)


@app.get("/context/{project_id}")
def restore_context(project_id: str = Depends(validate_project_id)) -> ContextRead:
    # find project
    project = projects_in_memory[project_id]

    validate_progress_note(project_id)

    # find all notes that belong to that project_id
    matching_notes = [
        note for note in progress_notes_in_memory if note.project_id == project_id
    ]

    # find all tasks that belong to that project_id && status == "open"
    open_tasks = get_project_tasks(project_id)

    # output recommended next action (latest note next actions OR open tasks
    latest_note = max(matching_notes, key=attrgetter("updated_at"), default=None)

    return {
        "project": project,
        "current_state": latest_note.current_state if latest_note else None,
        "open_tasks": open_tasks,
        "open_loops": latest_note.open_loops if latest_note else None,
        "next_actions": latest_note.next_actions if latest_note else None,
        "important_context": latest_note.important_context if latest_note else None,
    }
