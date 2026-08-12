from fastapi import FastAPI

from src.tevira_ai.routers import (
    actions,
    capture,
    context,
    health,
    progress_notes,
    projects,
    tasks,
)


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


app = create_app()
