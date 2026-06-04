from fastapi import FastAPI, Depends, HTTPException
from datetime import datetime, timezone
from .schemas import (
    TaskCreate, TaskRead,
    ProjectCreate, ProjectRead,
    ProgressNoteCreate, ProgressNoteRead
)

app = FastAPI(title="Tevira-AI")

# --- MEMORY STORAGE ---
tasks: list[TaskRead] = []
projects = {}
progress_notes: list[ProgressNoteRead] = []

# --- ROUTE VALIDATION ---
# TODO: change function to compare parameter 'project_id' against the projects dict, not progress_notes list
def validate_project_id(project_id: str):
    try:
        projects[project_id]
        return project_id
    except:
        raise HTTPException(status_code=404)


# --- ENDPOINTS ---

# -- "/health" --
@app.get("/health")
def check_health():
    return {"status": "ok", "service": "tevira-ai"}

# -- "/tasks" --
@app.post("/tasks", status_code=201)
def create_task(task: TaskCreate) -> TaskRead:
    task_id = f"task_{len(tasks) + 1}"

    new_task = TaskRead(
        **task.model_dump(), # Dumps all `task` fields here, no need to type them manually.
        id=task_id,
        status="open",
    )

    tasks.append(new_task)

    return new_task

@app.get("/tasks")
def show_tasks() -> list[TaskRead]:
    return tasks

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
def show_notes(project_id: str = Depends(validate_project_id)) -> list[ProgressNoteRead]:
    return [note for note in progress_notes if note.project_id == project_id]