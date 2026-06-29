from datetime import date, datetime
from typing import Literal, Annotated
from pydantic import BaseModel, Field, model_validator

NonEmptyString = Annotated[str, Field(min_length=1)]


# --- TASKS ---
class TaskCreate(BaseModel):
    title: NonEmptyString
    priority: Literal["low", "medium", "high"] = "medium"
    due_date: date | None = None
    project_id: str | None = None


class TaskRead(TaskCreate):
    id: str
    status: Literal["open", "done"] = "open"


class TaskUpdate(BaseModel):
    id: NonEmptyString
    title: NonEmptyString | None = None
    priority: Literal["low", "medium", "high"] | None = None
    due_date: date | None = None
    project_id: str | None = None
    status: Literal["open", "done"] | None = None

    @model_validator(mode="before")
    @classmethod
    def ensure_min_field_count(cls, data: dict) -> dict:
        if not isinstance(data, dict):
            raise ValueError(
                "At least one updatable field is required to update a task"
            )

        has_updatable_data = {
            item: value
            for item, value in data.items()
            if item != "id" and value is not None
        }

        if not has_updatable_data:
            raise ValueError(
                "At least one updatable field is required to update a task"
            )

        return data


# --- PROJECTS ---
class ProjectCreate(BaseModel):
    name: NonEmptyString


class ProjectRead(ProjectCreate):
    id: str


# --- PROGRESS NOTES ---
class ProgressNoteCreate(BaseModel):
    project_id: str
    current_state: NonEmptyString
    last_session: NonEmptyString
    open_loops: list[str] = []
    next_actions: str | None = None
    important_context: str | None = None
    blockers: list[str] = []
    confidence: Literal["low", "medium", "high"] = "medium"


class ProgressNoteRead(ProgressNoteCreate):
    id: str
    updated_at: datetime


# --- CONTEXT ---
class ContextRead(BaseModel):
    project: ProjectRead | None = None
    current_state: str | None = None
    open_tasks: list[TaskRead] | None = None
    open_loops: list[str] | None = None
    next_actions: str | None = None
    important_context: str | None = None
