from src.app.schemas import ProgressNoteCreate, ProgressNoteRead, ProgressNoteUpdate
from src.app.state.memory import progress_notes_id_number, progress_notes_in_memory
from src.app.services.projects import get_project
from fastapi import HTTPException
from datetime import datetime, timezone

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

def get_progress_note_by_id(note_id: str, database: list | None = None) -> ProgressNoteRead:
    notes_list = database if database is not None else progress_notes_in_memory

    matching_note = next((note for note in notes_list if note.id == note_id), None)
    if not matching_note:
        raise HTTPException(
            status_code=404,
            detail=f"Error 404: Note '{note_id}' does not exist.",
        )
    return matching_note

def get_progress_notes(project_id: str) -> list[ProgressNoteRead]:
    try:
        get_project(project_id)
        return [
            note for note in progress_notes_in_memory if note.project_id == project_id
        ]
    except HTTPException:
        return progress_notes_in_memory

def update_progress_note(note_id: str, updated_note: ProgressNoteUpdate) -> ProgressNoteRead:
    matching_note = get_progress_note_by_id(note_id)

    merge_ready_note = updated_note.model_dump(exclude_none=True)
    merge_ready_note["updated_at"] = datetime.now(timezone.utc)

    merged_note = {
        **matching_note.model_dump(),
        **merge_ready_note,
    }

    note_index = progress_notes_in_memory.index(matching_note)
    progress_notes_in_memory[note_index] = ProgressNoteRead(**merged_note)

    return ProgressNoteRead(**merged_note)

def delete_progress_note(note_id: str) -> None:
    matching_note = get_progress_note_by_id(note_id)
    note_index = progress_notes_in_memory.index(matching_note)
    del progress_notes_in_memory[note_index]
    # TODO: change the parameter from str type to a validation (similar to Depends(validate_project_id(project_id) or NonEmptyString at least)