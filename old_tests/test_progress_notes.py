import pytest
from fastapi import HTTPException


def test_validate_progress_note_accepts_existing_note():

    response = validate_progress_note("project_1")
    assert response == "project_1"


def test_validate_progress_note_raises_404_for_non_existing_note():
    with pytest.raises(HTTPException) as exception_info:
        validate_progress_note("project_42")

    assert exception_info.value.status_code == 404


def test_create_progress_note_accepts_valid_note_object(client):
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


def test_get_progress_note_returns_given_note(client):
    note_id = "note_1"

    response = client.get(f"/progress-notes/{note_id}")

    assert response.status_code == 200


def test_patch_note_router_returns_accepts_valid_input(client):
    note_id = "note_1"

    response = client.patch(
        f"/progress-notes/{note_id}",
        json={"current_state": "new current state"},
    )

    assert response.status_code == 200

    data = response.json()
    assert data["current_state"] == "new current state"


def test_delete_note_returns_204_for_existing_note_id(client):
    note_id = "note_1"

    response = client.delete(f"/progress-notes/{note_id}")

    assert response.status_code == 204
