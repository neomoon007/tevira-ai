from fastapi.testclient import TestClient
from fastapi import HTTPException
import pytest
from src.app.main import (
    app, tasks, projects, progress_notes,
    validate_progress_note, validate_project_id,
    ProjectRead
    )

client = TestClient(app) # create instance

def test_health():
    response = client.get("/health") 

    # tests expected behavior from server
    assert response.status_code == 200
    assert response.json() == {
        "status": "ok",
        "service": "tevira-ai",
    }

def test_create_task():
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

@pytest.fixture
def temp_projects():
    projects["project_1"] = ProjectRead(
        name="foo",
        id="project_1"
    )    
    projects["project_2"] = ProjectRead(
        name="bar",
        id="project_2"
    )    
    projects["project_3"] = ProjectRead(
        name="hello",
        id="project_3"
    )    
    projects["project_4"] = ProjectRead(
        name="world",
        id="project_4"
    )    

    yield projects
    projects.clear()

def test_validate_project_id_accepts_existing_id(temp_projects):
    response = validate_project_id("project_1")

    assert response == "project_1"
    assert "project_1" in temp_projects

def test_validate_project_id_raises_400_for_empty_string(temp_projects):
    with pytest.raises(HTTPException) as exception_info:
        validate_project_id("")

    assert exception_info.value.status_code == 400

def test_validate_project_id_raises_404_for_non_existing_project(temp_projects):
    with pytest.raises(HTTPException) as exception_info:
        validate_project_id("project_42")

    assert exception_info.value.status_code == 404

# test validate_progress_note function works:
# def test_validate_progress_note_accepts_existing_note():

    # test normal case (should pass)
    # test edge case (shouldn't pass)

# test get_project_tasks function works:
    # test normal case (should pass)
    # test edge case (shouldn't pass)

# test GET "/health" endpoint

# test POST "/tasks" endpoint
    # test normal case (should pass)
    # test edge case (shouldn't pass)

# test GET "/tasks" endpoint
    # test GET "/tasks" with 0 parameters passed
        # test normal case (should pass)
        # test edge case (shouldn't pass)

    # test GET "/tasks" with only 'project_id' passed
        # test normal case (should pass)
        # test edge case (shouldn't pass)
    
    # test GET "/tasks" with only 'task_id' passed
        # test normal case (should pass)
        # test edge case (shouldn't pass)
    
    # test GET "/tasks" with both parameters passed
        # test normal case (should pass)
        # test edge case (shouldn't pass)

# test POST "/projects" endpoint
    # test normal case (should pass)
    # test edge case (shouldn't pass)

# test GET "/projects" endpoint
    # test normal case (should pass)
    # test edge case (shouldn't pass)

# test POST "/progress-notes" endpoint
    # test normal case (should pass)
    # test edge case (shouldn't pass)

# test GET "/progress-notes" endpoint
    # test normal case (should pass)
    # test edge case (shouldn't pass)

# test GET "/context" endpoint
    # test normal case (should pass) - valid project_id and valid progress_note
    # test edge case (shouldn't pass) - invalid project_id
    # test edge case (shouldn't pass) - missing project_id
    # test edge case (shouldn't pass) - missing progress_note