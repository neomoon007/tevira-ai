def test_restore_context_accepts_valid_project_with_existing_note(
    client, test_project, test_note
):
    lookup_project = "project_1"
    response = client.get(f"/context/{lookup_project}")

    assert response.status_code == 200

    data = response.json()

    assert data["project"] == {
        "id": "project_1",
        "title": "Test Project",
    }
    assert data["current_state"] == "test state"
    assert data["open_loops"] == ["first open loop", "second open loop"]
    assert data["open_tasks"] == []
    assert data["next_actions"] == "build more, build faster"
    assert data["important_context"] == "this is important"
