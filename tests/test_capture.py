def test_capture_accepts_valid_input(client):
    task = "finish tests for Tevira-AI"
    due_date = "today."
    next_action = "deploy app."
    project_id = "project_2"

    response = client.post(
        "/capture/text",
        params={"input": f"Need to {task} before {due_date} Next, {next_action}"},
    )

    assert response.status_code == 200

    data = response.json()

    assert data["proposed_actions"][0]["data"]["title"] == task
    assert data["proposed_actions"][0]["data"]["due_date_hint"] == due_date
    assert data["proposed_actions"][0]["data"]["project_hint"] == project_id

    assert data["proposed_actions"][1]["data"]["next_action"] == next_action
