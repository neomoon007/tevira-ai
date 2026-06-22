from fastapi import APIRouter, HTTPException, Depends
from src.app.schemas import ProgressNoteCreate, ProgressNoteRead
from src.app.state import progress_notes_in_memory
from src.app.validator import validate_project_id
from datetime import datetime, timezone

router = APIRouter(prefix="/progress-notes", tags=["Progress Notes"])


# -- "/progress-notes" --
@router.post("", status_code=201)
def create_progress_note(note: ProgressNoteCreate) -> ProgressNoteRead:
    new_note = ProgressNoteRead(
        **note.model_dump(),
        updated_at=datetime.now(timezone.utc),
    )

    progress_notes_in_memory.append(new_note)

    return new_note


@router.get("")
def direct_to_notes_route() -> str:
    raise HTTPException(
        status_code=405,
        detail="Error 405: Method not allowed. You meant 'progress-notes/project_1'?",
    )


@router.get("/{project_id}")
def show_notes(
    project_id: str = Depends(validate_project_id),
) -> list[ProgressNoteRead]:
    return [note for note in progress_notes_in_memory if note.project_id == project_id]
