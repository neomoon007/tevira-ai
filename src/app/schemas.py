from datetime import date, datetime
from typing import Literal, Optional
from pydantic import BaseModel, Field

# --- TASKS ---
class TaskCreate(BaseModel):
    title: str = Field(min_length=1)
    priority: Literal["low", "medium", "high"] = "medium"
    due_date: Optional[date] = None
    project_id: Optional[str] = None

class TaskRead(TaskCreate):
    id: str
    status: Literal["open", "done"] = "open"

# --- PROJECTS ---
class ProjectCreate(BaseModel):
    name: str = Field(min_length=1)

class ProjectRead(ProjectCreate):
    id: str

# --- PROGRESS NOTES ---
class ProgressNoteCreate(BaseModel):
    project_id: str
    current_state: str = Field(min_length=1)
    last_session: str = Field(min_length=1)
    open_loops: list[str] = []
    next_actions: Optional[str] = None
    important_context: Optional[str] = None
    blockers: list[str] = []
    confidence: Literal["low", "medium", "high"] = "medium"

class ProgressNoteRead(ProgressNoteCreate):
    updated_at: datetime

# --- CONTEXT ---
class ContextRead(BaseModel):
    project: Optional[ProjectRead] = None
    current_state: Optional[str] = None
    open_tasks: Optional[list[TaskCreate]] = None
    open_loops: Optional[list[str]] = None
    next_actions: Optional[str] = None
    important_context: Optional[str] = None