import uuid

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.tevira_ai.db.database import get_db
from src.tevira_ai.schemas import (
    ProgressNoteCreate,
    ProgressNoteRead,
    ProgressNoteUpdate,
)
from src.tevira_ai.services.progress_notes import (
    create_progress_note,
    delete_progress_note,
    get_notes_by_project,
    get_progress_note_by_id,
    update_progress_note,
)

router = APIRouter(prefix="/progress-notes", tags=["Progress Notes"])


# -- "/progress-notes" --
@router.post("", status_code=201)
async def create_progress_note_endpoint(
    note: ProgressNoteCreate, db: AsyncSession = Depends(get_db)
) -> ProgressNoteRead:
    return await create_progress_note(db, note)


@router.get("")
async def get_progress_notes_endpoint(
    project_id: uuid.UUID, db: AsyncSession = Depends(get_db)
) -> list[ProgressNoteRead]:
    return await get_notes_by_project(db, project_id)


@router.get("/{note_id}")
async def get_progress_note_by_id_endpoint(
    note_id: uuid.UUID, db: AsyncSession = Depends(get_db)
) -> ProgressNoteRead:
    return await get_progress_note_by_id(db, note_id)


@router.patch("/{note_id}")
async def update_progress_note_endpoint(
    note_id: uuid.UUID,
    updated_note: ProgressNoteUpdate,
    db: AsyncSession = Depends(get_db),
) -> ProgressNoteRead:
    return await update_progress_note(db, note_id, updated_note)


@router.delete("/{note_id}", status_code=204)
async def delete_progress_note_endpoint(
    note_id: uuid.UUID, db: AsyncSession = Depends(get_db)
) -> None:
    await delete_progress_note(db, note_id)
