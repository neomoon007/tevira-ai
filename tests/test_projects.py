from app.utils import validate_project_id
from src.app.state.memory import projects_in_memory
import pytest
from fastapi import HTTPException


def test_validate_project_id_accepts_existing_id(temp_projects: dict):
    response = validate_project_id("project_1")

    assert response == "project_1"
    assert "project_1" in temp_projects


def test_validate_project_id_raises_400_for_empty_string(temp_projects: dict):
    with pytest.raises(HTTPException) as exception_info:
        validate_project_id("")

    assert exception_info.value.status_code == 400


def test_validate_project_id_raises_404_for_non_existing_project(temp_projects: dict):
    with pytest.raises(HTTPException) as exception_info:
        validate_project_id("project_42")

    assert exception_info.value.status_code == 404


def test_create_project_accepts_valid_project_object(temp_projects, client):
    projects_in_memory.clear()

    response = client.post(
        "/projects",
        json={"name": "Magnum Opus"},
    )

    assert response.status_code == 201

    data = response.json()
    assert data["name"] == "Magnum Opus"
    assert data["id"] == "project_1"
    projects_in_memory.clear()


def test_show_project_returns_200_for_existing_project(temp_projects, client):
    given_project_id = "project_1"

    response = client.get(f"/projects/{given_project_id}")

    assert response.status_code == 200


def test_show_project_returns_404_for_non_existing_project(temp_projects, client):
    given_project_id = "project_42"

    response = client.get(f"/projects/{given_project_id}")

    assert response.status_code == 404


def test_rename_project_returns_200_for_valid_request(temp_projects, client):
    given_project_id = "project_1"

    response = client.patch(
        f"/projects/{given_project_id}", json={"name": "This project name was altered"}
    )

    assert response.status_code == 200

    data = response.json()
    assert data["name"] == "This project name was altered"
    assert data["id"] == "project_1"
    projects_in_memory.clear()


def test_delete_project_returns_204(temp_projects, client):
    given_project_id = "project_1"
    response = client.delete(f"/projects/{given_project_id}")

    assert response.status_code == 204

    with pytest.raises(KeyError):
        projects_in_memory[given_project_id]
