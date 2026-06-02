from fastapi.testclient import TestClient
from src.app.main import app, tasks

client = TestClient(app) # create instance

def test_health():
    response = client.get("/health") # just like 'curl URL' in terminal

    # tests expected behavior from server
    assert response.status_code == 200
    assert response.json() == {
        "status": "ok",
        "service": "tevira-ai",
    }

def test_create_test():
    tasks.clear()

    response = client.post(
        "/tasks",
        json={
            "title": "Hello, World! This is my first task",
            "priority": "high",
            "due_date": None,
            "project_id": None,
        }
    )

    assert response.status_code == 201
    
    data = response.json()

    assert data["id"] == "task_1"
    assert data["status"] == "open"
    assert data["title"] == "Hello, World! This is my first task"
    assert data["priority"] == "high"
    assert data["due_date"] is None
    assert data["project_id"] is None