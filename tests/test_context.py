from datetime import date

def test_restore_context_accepts_valid_project_with_existing_note(
    temp_notes, temp_projects, temp_tasks, client
):
    lookup_project = "project_1"
    response = client.get(f"/context/{lookup_project}")

    assert response.status_code == 200

    data = response.json()

    assert data["project"] == {"id": "project_1", "name": "SAT"}
    assert data["current_state"] == "Week 08 got to finish soon"
    assert data["open_loops"] == ["not finished", "WIP", "TBA"]
    assert data["open_tasks"] == [
        {
            "title": "Hello World!",
            "priority": "high",
            "due_date": str(date.today()),
            "project_id": "project_1",
            "id": "task_1",
            "status": "open",
        },
        {
            "title": "SAT",
            "priority": "medium",
            "due_date": str(date.today()),
            "project_id": "project_1",
            "id": "task_2",
            "status": "open",
        },
    ]
    assert data["next_actions"] == "Finish week 08"
    assert data["important_context"] == "One step at a time"


def test_restore_context_raises_404_for_non_existent_project(
    temp_notes, temp_projects, temp_tasks, client
):
    lookup_project = "project_42"
    response = client.get(f"/context/{lookup_project}")

    assert response.status_code == 404


def test_restore_context_raises_404_for_missing_progress_note(
    temp_projects, temp_tasks, client
):
    lookup_project = "project_1"
    response = client.get(f"/context/{lookup_project}")

    assert response.status_code == 404