def test_restore_context_accepts_valid_project_with_existing_note(
    client, test_project, test_note
):
    lookup_project = "project_1"
    response = client.get(f"/context/{lookup_project}")

    assert response.status_code == 200

    data = response.json()

    assert data["project"] == {
        "id": "project_1",
        "title": "Test Project 1",
    }
    assert data["current_state"] == "test state"
    assert data["open_loops"] == ["first open loop", "second open loop"]
    assert data["open_tasks"] == []
    assert data["next_actions"] == "build more, build faster"
    assert data["important_context"] == "this is important"


def test_restore_context_raises_404_for_non_existent_project(client, test_project):
    lookup_project = "project_42"
    response = client.get(f"/context/{lookup_project}")

    assert response.status_code == 404


def test_restore_context_raises_404_for_missing_progress_note(client, test_project):
    lookup_project = "project_42"
    response = client.get(f"/context/{lookup_project}")

    assert response.status_code == 404


def test_restore_context_returns_task_when_missing_next_actions(
    client, test_project, test_note, test_task
):
    project_id = "project_2"
    response = client.get(f"/context/{project_id}")

    assert response.status_code == 200

    data = response.json()

    assert data["next_actions"] == {
        "title": "test task 3",
        "priority": "low",
        "due_date": None,
        "project_id": project_id,
        "id": "task_3",
        "status": "open",
    }
