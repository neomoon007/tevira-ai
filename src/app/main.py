from fastapi import FastAPI
from .schemas import TaskCreate, TaskRead, ProjectCreate, ProjectRead # import classes

app = FastAPI(title="Tevira-AI")

tasks: list[TaskRead] = []
projects = {}

@app.get("/health")
def check_health():
    return {"status": "ok", "service": "tevira-ai"}

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

@app.post("/projects", status_code=201)
def create_project(project: ProjectCreate) -> ProjectRead:
    project_id = f"project_{len(projects) + 1}"

    new_project = ProjectRead(
        **project.model_dump(),
        id=project_id,
    )

    # projects.append(new_project)
    projects[new_project.id] = new_project

    return new_project

@app.get("/projects")
def show_projects() -> list[ProjectRead]:
    # turn dict into list and only output the objects without the key from the projects dict
    return list(projects.values()) 