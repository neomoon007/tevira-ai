from fastapi import FastAPI
# from app.schemas import TaskCreate, TaskRead # import classes

app = FastAPI(title="Tevira-AI")

# tasks: list[TaskRead] = []

@app.get("/health")
def check_health():
    return {"status": "ok", "service": "tevira-ai"}