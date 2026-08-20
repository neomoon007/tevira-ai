from contextlib import asynccontextmanager

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from src.tevira_ai.db.database import create_engine, create_session, get_db_url
from src.tevira_ai.exceptions import DomainException
from src.tevira_ai.routers import (
    actions,
    capture,
    context,
    health,
    progress_notes,
    projects,
    tasks,
)


@asynccontextmanager
async def lifespan(app: FastAPI):
    app.state.database_url = get_db_url()
    app.state.engine = create_engine(app.state.database_url)
    app.state.session_factory = create_session(app.state.engine)

    yield

    await app.state.engine.dispose()


def create_app():
    app = FastAPI(title="Tevira-AI", lifespan=lifespan)

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


@app.exception_handler(DomainException)
def domain_exception_handler(request: Request, exception: DomainException):
    return JSONResponse(
        status_code=exception.status_code,
        content={
            "status": "error",
            "code": exception.error_code,
            "message": exception.message,
        },
    )
