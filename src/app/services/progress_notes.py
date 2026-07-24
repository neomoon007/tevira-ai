from src.app.schemas import ProgressNoteCreate, ProgressNoteRead, ProgressNoteUpdate
from src.app.db.database import SessionLocal
from src.app.db.models import ProgressNote
from src.app.repository.progress_notes import ProgressNoteRepository
from sqlalchemy.exc import NoResultFound
from fastapi import HTTPException

OWNER_ID = "local_user"


def create_progress_note(note: ProgressNoteCreate) -> ProgressNoteRead:
    db = SessionLocal()

    try:
        repository = ProgressNoteRepository(db)

        id_num_from_db = repository.get_highest_id(OWNER_ID)

        note_id = f"note_{id_num_from_db + 1}"

        note_in = ProgressNote(
            **note.model_dump(),
            id=note_id,
            owner_id=OWNER_ID,
        )

        note_out = repository.create(note_in)
    finally:
        db.close()

    return ProgressNoteRead.model_validate(note_out)


def get_progress_note_by_id(note_id: str) -> ProgressNoteRead:
    db = SessionLocal()

    try:
        repository = ProgressNoteRepository(db)

        note_from_db = repository.get_by_id(OWNER_ID, note_id)

        if not note_from_db:
            raise HTTPException(
                status_code=404, detail=f"Error 404: {note_id} does not exist."
            )
    finally:
        db.close()

    return ProgressNoteRead.model_validate(note_from_db)


def get_notes_by_project(project_id: str) -> list[ProgressNoteRead]:
    db = SessionLocal()

    try:
        repository = ProgressNoteRepository(db)

        if project_id:
            notes_from_db = repository.get_by_project(OWNER_ID, project_id)
        else:
            notes_from_db = repository.get_all(OWNER_ID)
    finally:
        db.close()

    return [ProgressNoteRead.model_validate(note) for note in notes_from_db]


def update_progress_note(
    note_id: str, updated_note: ProgressNoteUpdate
) -> ProgressNoteRead:
    db = SessionLocal()
    update_data = updated_note.model_dump(exclude_unset=True)

    try:
        repository = ProgressNoteRepository(db)

        note_from_db = repository.update(OWNER_ID, note_id, update_data)
    except NoResultFound:
        raise HTTPException(
            status_code=404, detail=f"Error 404: {note_id} does not exist."
        )
    finally:
        db.close()

    return ProgressNoteRead.model_validate(note_from_db)


def delete_progress_note(
    note_id: str,
) -> None:  # TODO: change the parameter from str type to a validation (similar to Depends(validate_project_id(project_id) or NonEmptyString at least)
    db = SessionLocal()

    try:
        repository = ProgressNoteRepository(db)

        repository.delete(OWNER_ID, note_id)
    finally:
        db.close()
