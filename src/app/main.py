from fastapi import FastAPI, Depends, HTTPException
from src.app.state import projects_in_memory, progress_notes
from src.app.validator import (  # TODO: create a separate folder for validator.py and state.py
    validate_project_id,
    validate_progress_note,
    get_project_tasks,
)
from src.app.routers import tasks, health, projects
from datetime import datetime, timezone
from operator import attrgetter
from src.app.schemas import (
    ProgressNoteCreate,
    ProgressNoteRead,
    ContextRead,
)

app = FastAPI(title="Tevira-AI")

# --- ROUTERS ---
app.include_router(tasks.router)
app.include_router(health.router)
app.include_router(projects.router)


# # -- "/projects" --
# @app.post("/projects", status_code=201)
# def create_project(project: ProjectCreate) -> ProjectRead:
#     project_id = f"project_{len(projects_in_memory) + 1}"

#     new_project = ProjectRead(
#         **project.model_dump(),
#         id=project_id,
#     )

#     projects_in_memory[new_project.id] = new_project

#     return new_project


# @app.get("/projects")
# def show_projects() -> list[ProjectRead]:
#     # turn dict into list and only output the objects without the key from the projects dict
#     return list(projects_in_memory.values())


# -- "/progress-notes" --
@app.post("/progress-notes", status_code=201)
def create_progress_note(note: ProgressNoteCreate) -> ProgressNoteRead:
    new_note = ProgressNoteRead(
        **note.model_dump(),
        updated_at=datetime.now(timezone.utc),
    )

    progress_notes.append(new_note)

    return new_note


@app.get("/progress-notes")
def direct_to_notes_route() -> str:
    raise HTTPException(
        status_code=405,
        detail="Error 405: Method not allowed. You meant 'progress-notes/project_1'?",
    )


@app.get("/progress-notes/{project_id}")
def show_notes(
    project_id: str = Depends(validate_project_id),
) -> list[ProgressNoteRead]:
    return [note for note in progress_notes if note.project_id == project_id]


@app.get("/context/{project_id}")
def restore_context(project_id: str = Depends(validate_project_id)) -> ContextRead:
    # find project
    project = projects_in_memory[project_id]

    validate_progress_note(project_id)

    # find all notes that belong to that project_id
    matching_notes = [note for note in progress_notes if note.project_id == project_id]

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
