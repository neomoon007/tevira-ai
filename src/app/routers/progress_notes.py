from fastapi import APIRouter, HTTPException
from src.app.schemas import ProgressNoteCreate, ProgressNoteRead, ProgressNoteUpdate
from src.app.state.memory import progress_notes_in_memory, progress_notes_id_number
from src.app.validator import validate_project_id, get_note_by_id
from datetime import datetime, timezone

router = APIRouter(prefix="/progress-notes", tags=["Progress Notes"])


# -- "/progress-notes" --
@router.post("", status_code=201)
def create_progress_note(note: ProgressNoteCreate) -> ProgressNoteRead:
    global progress_notes_id_number
    progress_notes_id_number += 1

    note_id = f"note_{progress_notes_id_number}"

    new_note = ProgressNoteRead(
        **note.model_dump(),
        id=note_id,
        updated_at=datetime.now(timezone.utc),
    )

    progress_notes_in_memory.append(new_note)

    return new_note


@router.get("")
def show_notes(project_id: str = None) -> list[ProgressNoteRead]:
    try:
        validate_project_id(project_id)
        return [
            note for note in progress_notes_in_memory if note.project_id == project_id
        ]
    except HTTPException:
        return progress_notes_in_memory


@router.get("/{note_id}")
def get_note(note_id: str) -> ProgressNoteRead:
    return get_note_by_id(note_id)


@router.patch("/{note_id}")
def update_note(note_id: str, updated_note: ProgressNoteUpdate) -> ProgressNoteRead:
    matching_note = get_note_by_id(note_id)

    merge_ready_note = updated_note.model_dump(exclude_none=True)
    merge_ready_note["updated_at"] = datetime.now(timezone.utc)

    merged_note = {
        **matching_note.model_dump(),
        **merge_ready_note,
    }

    note_index = progress_notes_in_memory.index(matching_note)
    progress_notes_in_memory[note_index] = ProgressNoteRead(**merged_note)

    return ProgressNoteRead(**merged_note)

@router.delete("/{note_id}", status_code=204)
def delete_task(note_id: str):
    # TODO: change the parameter from str type to a validation (similar to Depends(validate_project_id(project_id) or NonEmptyString at least)
    matching_note = get_note_by_id(note_id)
    note_index = progress_notes_in_memory.index(matching_note)
    del progress_notes_in_memory[note_index]

    return