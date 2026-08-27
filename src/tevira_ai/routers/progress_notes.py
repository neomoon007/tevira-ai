import uuid

from fastapi import APIRouter

from src.tevira_ai.dependencies import CurrentUserId, DBSession
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
    note: ProgressNoteCreate, owner_id: CurrentUserId, db: DBSession
) -> ProgressNoteRead:
    return await create_progress_note(owner_id, db, note)


@router.get("")
async def get_progress_notes_endpoint(
    project_id: uuid.UUID, owner_id: CurrentUserId, db: DBSession
) -> list[ProgressNoteRead]:
    return await get_notes_by_project(owner_id, db, project_id)


@router.get("/{note_id}")
async def get_progress_note_by_id_endpoint(
    note_id: uuid.UUID, owner_id: CurrentUserId, db: DBSession
) -> ProgressNoteRead:
    return await get_progress_note_by_id(owner_id, db, note_id)


@router.patch("/{note_id}")
async def update_progress_note_endpoint(
    note_id: uuid.UUID,
    updated_note: ProgressNoteUpdate,
    owner_id: CurrentUserId,
    db: DBSession,
) -> ProgressNoteRead:
    return await update_progress_note(owner_id, db, note_id, updated_note)


@router.delete("/{note_id}", status_code=204)
async def delete_progress_note_endpoint(
    note_id: uuid.UUID, owner_id: CurrentUserId, db: DBSession
) -> None:
    await delete_progress_note(owner_id, db, note_id)
