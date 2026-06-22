from fastapi import FastAPI, Depends, HTTPException
from src.app.state import tasks_in_memory, projects, progress_notes
from src.app.routers import tasks
from datetime import datetime, timezone
from operator import attrgetter
from src.app.schemas import (
    # TaskCreate,
    TaskRead,
    ProjectCreate,
    ProjectRead,
    ProgressNoteCreate,
    ProgressNoteRead,
    ContextRead,
)

app = FastAPI(title="Tevira-AI")

# --- ROUTERS ---
app.include_router(tasks.router)

# --- MEMORY STORAGE ---
# tasks_in_memory: list[TaskRead] = []
# projects = {}
# progress_notes: list[ProgressNoteRead] = []


# --- ROUTE VALIDATION ---
def validate_project_id(project_id: str):
    if project_id == "":
        raise HTTPException(
            status_code=400, detail="Error 400: Empty string where input is required"
        )
    try:
        projects[project_id]
        return project_id
    except Exception as project_missing:
        raise HTTPException(
            status_code=404,
            detail=f"Error 404: Project {project_missing} does not exist.",
        )


def validate_progress_note(project_id: str):
    if any(note.project_id == project_id for note in progress_notes):
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


# --- ENDPOINTS ---
# -- "/health" --
@app.get("/health")
def check_health():
    return {"status": "ok", "service": "tevira-ai"}


# -- "/tasks" --
# @app.post("/tasks", status_code=201)
# def create_task(task: TaskCreate) -> TaskRead:
#     task_id = f"task_{len(tasks) + 1}"

#     new_task = TaskRead(
#         **task.model_dump(),  # Dumps all `task` fields here, no need to type them manually.
#         id=task_id,
#         status="open",
#     )

#     tasks.append(new_task)

#     return new_task


# @app.get("/tasks")
# def show_tasks(project_id: str = None, task_id: str = None) -> list[TaskRead]:
#     if project_id is None and task_id is None:
#         return tasks

#     if project_id is not None and task_id is None:
#         validate_project_id(project_id)
#         return get_project_tasks(project_id)

#     if project_id is None and task_id is not None:
#         matching_task = [task for task in tasks if task.id == task_id]
#         if not matching_task:
#             raise HTTPException(
#                 status_code=404,
#                 detail=f"Error 404: Task {task_id} does not exist.",
#             )
#         return matching_task

#     if project_id is not None and task_id is not None:
#         validate_project_id(project_id)
#         project_tasks = get_project_tasks(project_id)
#         matching_task = [task for task in project_tasks if task.id == task_id]

#         if not matching_task:
#             raise HTTPException(
#                 status_code=404,
#                 detail=f"Error 404: Task '{task_id}' does not exist inside of '{project_id}'",
#             )
#         return matching_task


# -- "/projects" --
@app.post("/projects", status_code=201)
def create_project(project: ProjectCreate) -> ProjectRead:
    project_id = f"project_{len(projects) + 1}"

    new_project = ProjectRead(
        **project.model_dump(),
        id=project_id,
    )

    projects[new_project.id] = new_project

    return new_project


@app.get("/projects")
def show_projects() -> list[ProjectRead]:
    # turn dict into list and only output the objects without the key from the projects dict
    return list(projects.values())


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
    project = projects[project_id]

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
