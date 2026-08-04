import pytest
from fastapi import HTTPException
from sqlalchemy import select

from src.app.db.models import Project
from src.app.services.projects import get_project


def test_can_insert_project(db_session):
    owner_id = "local_user"
    project_id = "project_1"
    title = "foo"

    project = Project(id=project_id, owner_id=owner_id, title=title)

    db_session.add(project)
    db_session.commit()

    saved = db_session.scalars(
        select(Project).where(
            Project.id == project_id,
            Project.owner_id == owner_id,
            Project.title == title,
        )
    ).first()

    assert saved is not None
    assert saved.id == project_id


def test_validate_project_id_accepts_existing_project(db_session, test_project):
    response = get_project(db_session, "project_1")

    assert response.id == "project_1"


def test_validate_project_id_raises_400_for_empty_string(db_session, test_project):
    with pytest.raises(HTTPException) as exception_info:
        get_project(db_session, "")

    assert exception_info.value.status_code == 400


def test_validate_project_id_raises_404_for_non_existing_project(
    db_session, test_project
):
    with pytest.raises(HTTPException) as exception_info:
        get_project(db_session, "project_999")

    assert exception_info.value.status_code == 404


def test_create_project_accepts_valid_project_object(client):
    response = client.post("/projects", json={"title": "Magnum Opus"})

    assert response.status_code == 201

    data = response.json()
    assert data["title"] == "Magnum Opus"
    assert data["id"] == "project_1"


def test_show_project_returns_200_for_existing_project(client, test_project):
    project_id = "project_1"

    response = client.get(f"/projects/{project_id}")

    assert response.status_code == 200


def test_show_project_returns_404_for_non_existing_project(client, test_project):
    project_id = "project_999"

    response = client.get(f"/projects/{project_id}")

    assert response.status_code == 404


def test_rename_project_returns_200_for_valid_request(client, test_project):
    project_id = "project_1"

    response = client.patch(
        f"/projects/{project_id}", json={"title": "This project title was renamed"}
    )

    assert response.status_code == 200

    data = response.json()
    assert data["title"] == "This project title was renamed"
    assert data["id"] == "project_1"


def test_delete_project_returns_204(client, test_project):
    project_id = "project_1"

    response = client.delete(f"/projects/{project_id}")

    assert response.status_code == 204


def test_delete_project_returns_404_for_non_existing_project(client, test_project):
    project_id = "project_999"

    response = client.delete(f"/projects/{project_id}")

    assert response.status_code == 404
