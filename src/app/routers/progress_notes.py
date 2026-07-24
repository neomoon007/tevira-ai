from fastapi import APIRouter
from src.app.schemas import ProgressNoteCreate, ProgressNoteRead, ProgressNoteUpdate
from src.app.services.progress_notes import (
    create_progress_note,
    get_notes_by_project,
    get_progress_note_by_id,
    update_progress_note,
    delete_progress_note,
)

router = APIRouter(prefix="/progress-notes", tags=["Progress Notes"])


# -- "/progress-notes" --
@router.post("", status_code=201)
def create_progress_note_endpoint(note: ProgressNoteCreate) -> ProgressNoteRead:
    return create_progress_note(note)


@router.get("")
def get_progress_notes_endpoint(
    project_id: str = "",
) -> list[ProgressNoteRead]:
    return get_notes_by_project(project_id)


@router.get("/{note_id}")
def get_progress_note_by_id_endpoint(note_id: str) -> ProgressNoteRead:
    return get_progress_note_by_id(note_id)


@router.patch("/{note_id}")
def update_progress_note_endpoint(
    note_id: str, updated_note: ProgressNoteUpdate
) -> ProgressNoteRead:
    return update_progress_note(note_id, updated_note)


@router.delete("/{note_id}", status_code=204)
def delete_progress_note_endpoint(note_id: str) -> None:
    delete_progress_note(note_id)
