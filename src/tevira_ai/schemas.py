import uuid
from datetime import date, datetime
from typing import Annotated, Literal

from pydantic import BaseModel, ConfigDict, Field

NonEmptyString = Annotated[str, Field(min_length=1)]


# --- TASKS ---
class TaskCreate(BaseModel):
    title: NonEmptyString
    priority: Literal["low", "medium", "high"] = "medium"
    due_date: date | None = None
    project_id: uuid.UUID


class TaskRead(TaskCreate):
    id: uuid.UUID | None = None
    status: Literal["open", "done"] = "open"

    model_config = ConfigDict(from_attributes=True)


class TaskUpdate(BaseModel):
    title: NonEmptyString | None = None
    priority: Literal["low", "medium", "high"] | None = None
    due_date: date | None = None
    project_id: uuid.UUID | None = None
    status: Literal["open", "done"] | None = None


# --- PROJECTS ---
class ProjectCreate(BaseModel):
    title: NonEmptyString


class ProjectRead(ProjectCreate):
    id: uuid.UUID | None = None

    model_config = ConfigDict(from_attributes=True)


# --- PROGRESS NOTES ---
class ProgressNoteCreate(BaseModel):
    project_id: uuid.UUID
    current_state: NonEmptyString | None = None
    last_session: NonEmptyString | None = None
    open_loops: list[str] = []
    next_actions: str | None = None
    important_context: str | None = None
    blockers: list[str] = []
    confidence: Literal["low", "medium", "high"] = "medium"


class ProgressNoteRead(ProgressNoteCreate):
    id: uuid.UUID | None = None
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


class ProgressNoteUpdate(BaseModel):
    project_id: uuid.UUID | None = None
    current_state: NonEmptyString | None = None
    last_session: NonEmptyString | None = None
    open_loops: list[str] | None = None
    next_actions: str | None = None
    important_context: str | None = None
    blockers: list[str] | None = None
    confidence: Literal["low", "medium", "high"] | None = None
    updated_at: datetime | None = None


# --- CONTEXT ---
class ContextRead(BaseModel):
    project: ProjectRead | None = None
    current_state: str | None = None
    open_tasks: list[TaskRead] | None = None
    open_loops: list[str] | None = None
    next_actions: TaskRead | str | None = None
    important_context: str | None = None


# --- PARSER ---
class ParseNoteRead(BaseModel):
    title: NonEmptyString
    project_id_hint: uuid.UUID
    due_date_hint: NonEmptyString
    next_action_hint: NonEmptyString


class CreateTaskProposal(BaseModel):
    title: NonEmptyString
    due_date_hint: NonEmptyString
    project_hint: uuid.UUID


class CreateProgressNoteProposal(BaseModel):
    next_action: str | None = None
    project_hint: uuid.UUID


class CreateTaskAction(BaseModel):
    type: Literal["create_task"]
    data: CreateTaskProposal


class CreateProgressNoteAction(BaseModel):
    type: Literal["create_progress_note"]
    data: CreateProgressNoteProposal


ProposedAction = CreateTaskAction | CreateProgressNoteAction


# --- CAPTURE ---
class CaptureRead(BaseModel):
    raw_text: NonEmptyString
    parsed: ParseNoteRead
    proposed_actions: list[ProposedAction]


# --- ACTIONS ---
class ApplyActionResponse(BaseModel):
    status: Literal["applied"]
    action: ProposedAction
    result: TaskRead | ProgressNoteRead
