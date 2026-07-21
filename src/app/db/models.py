from sqlalchemy import String, ForeignKey, Date, DateTime
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy.dialects.postgresql import ARRAY
from datetime import date, datetime
from typing import Literal


class Base(DeclarativeBase):
    type_annotation_map = {
        list[str]: ARRAY(String),
        date: Date,
        datetime: DateTime,
    }


class Project(Base):
    __tablename__ = "projects"

    id: Mapped[str] = mapped_column(primary_key=True)
    owner_id: Mapped[str]
    title: Mapped[str]


class Task(Base):
    __tablename__ = "tasks"

    id: Mapped[str] = mapped_column(primary_key=True)
    owner_id: Mapped[str]
    title: Mapped[str]
    project_id: Mapped[str] = mapped_column(ForeignKey("projects.id"))
    priority: Mapped[Literal["low", "medium", "high"]]
    due_date: Mapped[date | None]
    status: Mapped[Literal["open", "done"]]


class ProgressNote(Base):
    __tablename__ = "progress_notes"

    id: Mapped[str] = mapped_column(primary_key=True)
    owner_id: Mapped[str]
    project_id: Mapped[str] = mapped_column(ForeignKey("projects.id"))
    current_state: Mapped[str | None]
    last_session: Mapped[str | None]
    open_loops: Mapped[list[str] | None]
    next_actions: Mapped[str | None]
    important_context: Mapped[str | None]
    blockers: Mapped[list[str] | None]
    confidence: Mapped[str]
    updated_at: Mapped[datetime] = mapped_column(default=datetime.now)
