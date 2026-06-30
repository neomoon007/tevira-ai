from src.app.schemas import ProgressNoteRead
from src.app.validator import validate_progress_note
from src.app.state.memory import progress_notes_in_memory
import pytest
from fastapi import HTTPException
from pydantic import TypeAdapter


def test_validate_progress_note_accepts_existing_note(
    temp_notes: list[ProgressNoteRead],
):
    response = validate_progress_note("project_1")
    assert response == "project_1"


def test_validate_progress_note_raises_404_for_non_existing_note(
    temp_notes: list[ProgressNoteRead],
):
    with pytest.raises(HTTPException) as exception_info:
        validate_progress_note("project_42")

    assert exception_info.value.status_code == 404


def test_create_progress_note_accepts_valid_note_object(client):
    progress_notes_in_memory.clear()

    response = client.post(
        "/progress-notes",
        json={
            "project_id": "project_1",
            "current_state": "Just created main.py",
            "last_session": "Created github repo",
            "open_loops": ["Create roadmap", "Follow roadmap"],
            "next_actions": "Create fastapi instance",
            "important_context": "Read documentation",
            "blockers": ["Nothing"],
            "confidence": "high",
        },
    )

    assert response.status_code == 201

    data = response.json()
    assert data["project_id"] == "project_1"
    assert data["current_state"] == "Just created main.py"
    assert data["last_session"] == "Created github repo"
    assert data["open_loops"] == ["Create roadmap", "Follow roadmap"]
    assert data["next_actions"] == "Create fastapi instance"
    assert data["important_context"] == "Read documentation"
    assert data["blockers"] == ["Nothing"]
    assert data["confidence"] == "high"
    progress_notes_in_memory.clear()
