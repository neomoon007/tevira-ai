def test_actions_accepts_valid_create_task_object(client, temp_tasks):
    title = "finish tests for tevira-ai"
    due_date_hint = "today."
    project_id_hint = "project_2"

    response = client.post(
        "/actions/apply",
        json={
            "type": "create_task",
            "data": {
                "title": title,
                "due_date_hint": due_date_hint,
                "project_hint": project_id_hint,
            },
        },
    )

    assert response.status_code == 201
