from datetime import date
from src.app.services.tasks import get_important_task
from src.app.state.memory import tasks_in_memory


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


def test_get_important_task_returns_highest_priority_task(temp_projects, temp_tasks):
    project_id = "project_1"
    response = get_important_task(project_id)
    assert response == tasks_in_memory[0]


def test_restore_context_returns_task_when_missing_next_action(
    temp_notes, temp_projects, temp_tasks, client
):
    project_id = "project_5"
    response = client.get(f"/context/{project_id}")

    assert response.status_code == 200

    data = response.json()

    assert data["next_actions"] == {
        "title": "This is the way",
        "priority": "high",
        "due_date": str(date.today()),
        "project_id": "project_5",
        "id": "task_5",
        "status": "open",
    }
