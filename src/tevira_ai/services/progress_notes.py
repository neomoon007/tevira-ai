import uuid

from sqlalchemy.orm import Session

from src.tevira_ai.db.models import ProgressNote
from src.tevira_ai.exceptions import ResourceNotFoundError
from src.tevira_ai.repository.progress_notes import ProgressNoteRepository
from src.tevira_ai.schemas import (
    ProgressNoteCreate,
    ProgressNoteRead,
    ProgressNoteUpdate,
)
from src.tevira_ai.services.projects import get_project

OWNER_ID = "local_user"


def create_progress_note(db: Session, note: ProgressNoteCreate) -> ProgressNoteRead:
    get_project(db, note.project_id)

    repository = ProgressNoteRepository(db)

    note_in = ProgressNote(
        **note.model_dump(),
        owner_id=OWNER_ID,
    )

    note_out = repository.create(note_in)

    return ProgressNoteRead.model_validate(note_out)


def get_progress_note_by_id(db: Session, note_id: uuid.UUID) -> ProgressNoteRead:
    repository = ProgressNoteRepository(db)

    note_from_db = repository.get_by_id(OWNER_ID, note_id)

    if not note_from_db:
        raise ResourceNotFoundError(
            resource_type="ProgressNote", resource_id=str(note_id)
        )

    return ProgressNoteRead.model_validate(note_from_db)


def get_notes_by_project(db: Session, project_id: uuid.UUID) -> list[ProgressNoteRead]:
    repository = ProgressNoteRepository(db)
    notes_from_db = repository.get_by_project(OWNER_ID, project_id)

    return [ProgressNoteRead.model_validate(note) for note in notes_from_db]


def update_progress_note(
    db: Session, note_id: uuid.UUID, updated_note: ProgressNoteUpdate
) -> ProgressNoteRead:
    update_data = updated_note.model_dump(exclude_unset=True)

    repository = ProgressNoteRepository(db)
    note_from_db = repository.update(OWNER_ID, note_id, update_data)

    if not note_from_db:
        raise ResourceNotFoundError(
            resource_type="ProgressNote", resource_id=str(note_id)
        )

    return ProgressNoteRead.model_validate(note_from_db)


def delete_progress_note(
    db: Session, note_id: uuid.UUID
) -> None:  # TODO: change the parameter from str type to a validation (similar to Depends(validate_project_id(project_id) or NonEmptyString at least)
    get_progress_note_by_id(db, note_id)

    repository = ProgressNoteRepository(db)
    repository.delete(OWNER_ID, note_id)
