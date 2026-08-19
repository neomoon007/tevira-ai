def test_create_progress_note_accepts_valid_note_obj(client, test_project):
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


def test_get_progress_note_returns_existing_note(client, test_project, test_note):
    note_id = "note_1"

    response = client.get(f"/progress-notes/{note_id}")

    assert response.status_code == 200

    data = response.json()

    assert data["id"] == "note_1"
    assert data["project_id"] == "project_1"
    assert data["current_state"] == "test state"
    assert data["last_session"] == "last session log"
    assert data["open_loops"] == ["first open loop", "second open loop"]
    assert data["next_actions"] == "build more, build faster"
    assert data["important_context"] == "this is important"
    assert data["blockers"] == ["bugs"]
    assert data["confidence"] == "medium"


def test_patch_note_router_returns_accepts_valid_input(client, test_project, test_note):
    note_id = "note_1"

    response = client.patch(
        f"/progress-notes/{note_id}", json={"current_state": "new current state"}
    )

    assert response.status_code == 200

    data = response.json()

    assert data["current_state"] == "new current state"


def test_delete_note_returns_204_for_existing_note_id(client, test_project, test_note):
    note_id = "note_1"

    response = client.delete(f"/progress-notes/{note_id}")

    assert response.status_code == 204
