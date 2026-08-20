from datetime import date

from httpx import AsyncClient

from src.tevira_ai.db.models import Project


async def test_actions_accepts_valid_create_task_object(
    client: AsyncClient, test_project: list[Project]
):
    title = "finish tests for portfolio project"
    due_date_hint = "today."
    project_id_hint = str(test_project[0].id)

    response = await client.post(
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

    data = response.json()

    assert data["status"] == "applied"
    assert data["result"]["due_date"] == date.today().strftime("%Y-%m-%d")
