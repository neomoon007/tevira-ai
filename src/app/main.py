from fastapi import FastAPI
from .schemas import TaskCreate, TaskRead # import classes

app = FastAPI(title="Tevira-AI")

tasks: list[TaskRead] = []

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