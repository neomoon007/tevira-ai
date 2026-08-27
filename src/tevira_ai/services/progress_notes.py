from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession

from src.tevira_ai.db.models import ProgressNote
from src.tevira_ai.exceptions import ResourceNotFoundError
from src.tevira_ai.repository.progress_notes import ProgressNoteRepository
from src.tevira_ai.schemas import (
    ProgressNoteCreate,
    ProgressNoteRead,
    ProgressNoteUpdate,
)
from src.tevira_ai.services.projects import get_project


async def create_progress_note(
    owner_id: UUID, db: AsyncSession, note: ProgressNoteCreate
) -> ProgressNoteRead:
    await get_project(owner_id, db, note.project_id)

    repository = ProgressNoteRepository(db)

    note_in = ProgressNote(
        **note.model_dump(),
        owner_id=owner_id,
    )

    note_out = await repository.create(note_in)

    return ProgressNoteRead.model_validate(note_out)


async def get_progress_note_by_id(
    owner_id: UUID, db: AsyncSession, note_id: UUID
) -> ProgressNoteRead:
    repository = ProgressNoteRepository(db)

    note_from_db = await repository.get_by_id(owner_id, note_id)

    if not note_from_db:
        raise ResourceNotFoundError(
            resource_type="ProgressNote", resource_id=str(note_id)
        )

    return ProgressNoteRead.model_validate(note_from_db)


async def get_notes_by_project(
    owner_id: UUID, db: AsyncSession, project_id: UUID
) -> list[ProgressNoteRead]:
    repository = ProgressNoteRepository(db)
    notes_from_db = await repository.get_by_project(owner_id, project_id)

    return [ProgressNoteRead.model_validate(note) for note in notes_from_db]


async def update_progress_note(
    owner_id: UUID,
    db: AsyncSession,
    note_id: UUID,
    updated_note: ProgressNoteUpdate,
) -> ProgressNoteRead:
    update_data = updated_note.model_dump(exclude_unset=True)

    repository = ProgressNoteRepository(db)
    note_from_db = await repository.update(owner_id, note_id, update_data)

    if not note_from_db:
        raise ResourceNotFoundError(
            resource_type="ProgressNote", resource_id=str(note_id)
        )

    return ProgressNoteRead.model_validate(note_from_db)


async def delete_progress_note(owner_id: UUID, db: AsyncSession, note_id: UUID) -> None:
    await get_progress_note_by_id(owner_id, db, note_id)

    repository = ProgressNoteRepository(db)
    await repository.delete(owner_id, note_id)
