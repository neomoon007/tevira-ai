import uuid
from datetime import date, datetime
from typing import Literal

from sqlalchemy import Date, DateTime, ForeignKey, String
from sqlalchemy.dialects.postgresql import ARRAY
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    type_annotation_map = {
        list[str]: ARRAY(String),
        date: Date,
        datetime: DateTime,
    }


class Project(Base):
    __tablename__ = "projects"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid7)
    owner_id: Mapped[str]
    title: Mapped[str]


class Task(Base):
    __tablename__ = "tasks"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid7)
    owner_id: Mapped[str]
    title: Mapped[str]
    project_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("projects.id"))
    priority: Mapped[Literal["low", "medium", "high"]]
    due_date: Mapped[date | None]
    status: Mapped[Literal["open", "done"]]


class ProgressNote(Base):
    __tablename__ = "progress_notes"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid7)
    owner_id: Mapped[str]
    project_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("projects.id"))
    current_state: Mapped[str | None]
    last_session: Mapped[str | None]
    open_loops: Mapped[list[str] | None]
    next_actions: Mapped[str | None]
    important_context: Mapped[str | None]
    blockers: Mapped[list[str] | None]
    confidence: Mapped[str]
    updated_at: Mapped[datetime] = mapped_column(default=datetime.now)
