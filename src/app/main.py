from fastapi import FastAPI
from src.app.db.models import Base, Project, Task, ProgressNote
from src.app.db.database import engine
from src.app.routers import (
    health,
    projects,
    progress_notes,
    context,
    tasks,
    capture,
    actions,
)


def init_db():
    print("Creating tables...")
    Base.metadata.create_all(engine)
    print("Database ready!")
    return


def create_app():
    app = FastAPI(title="Tevira-AI")

    # --- ROUTERS ---
    app.include_router(tasks.router)
    app.include_router(health.router)
    app.include_router(projects.router)
    app.include_router(progress_notes.router)
    app.include_router(context.router)
    app.include_router(capture.router)
    app.include_router(actions.router)
    return app


init_db()
app = create_app()
