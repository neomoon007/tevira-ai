from fastapi import FastAPI
from src.app.routers import tasks, health, projects, progress_notes, context

app = FastAPI(title="Tevira-AI")

# --- ROUTERS ---
app.include_router(tasks.router)
app.include_router(health.router)
app.include_router(projects.router)
app.include_router(progress_notes.router)
app.include_router(context.router)
