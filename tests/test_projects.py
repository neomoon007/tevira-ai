from sqlalchemy import select

from src.app.db.models import Project


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
