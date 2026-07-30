from src.app.db.models import Project


def test_create_project(db_session):
    saved = db_session.get(Project, "project_1")

    assert saved is not None
    assert saved.title == "Inbox"
