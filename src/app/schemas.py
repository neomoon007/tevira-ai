from datetime import date, datetime
from typing import Literal, Optional
from pydantic import BaseModel, Field

# Create object structure for tasks
class TaskCreate(BaseModel):
    title: str = Field(min_length=1)
    priority: Literal["low", "medium", "high"] = "medium"
    due_date: Optional[date] = None
    project_id: Optional[str] = None

# Create object structure for reading tasks
class TaskRead(TaskCreate):
    id: str
    status: Literal["open", "done"] = "open"

# Create object structure for projects
class ProjectCreate(BaseModel):
    name: str = Field(min_length=1)

# Create object structure for reading projects
class ProjectRead(ProjectCreate):
    id: str