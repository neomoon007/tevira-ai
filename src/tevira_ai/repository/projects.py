import uuid

from sqlalchemy import delete, select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from src.tevira_ai.db.models import Project
from src.tevira_ai.schemas import ProjectRead


class ProjectRepository:
    def __init__(self, session: Session):
        self.session = session

    def create(self, project: Project) -> Project:
        self.session.add(project)
        self.session.commit()
        self.session.refresh(project)

        return project

    def get_by_id(self, owner_id: str, project_id: uuid.UUID) -> Project | None:
        query_result = self.session.scalars(
            select(Project).where(
                Project.owner_id == owner_id, Project.id == project_id
            )
        ).first()

        return query_result

    def get_all(self, owner_id: str) -> list[Project]:
        query_result = list(
            self.session.scalars(
                select(Project).where(Project.owner_id == owner_id)
            ).all()
        )

        return query_result

    def rename(self, owner_id: str, renamed_project: ProjectRead) -> Project | None:
        project = self.session.scalars(
            select(Project).where(
                Project.owner_id == owner_id, Project.id == renamed_project.id
            )
        ).first()

        if project:
            project.title = renamed_project.title

            self.session.commit()
            self.session.refresh(project)

            return project

    def delete(self, owner_id: str, project_id: uuid.UUID):
        try:
            self.session.execute(
                delete(Project).where(
                    Project.owner_id == owner_id, Project.id == project_id
                )
            )
            self.session.commit()
        except IntegrityError:
            self.session.rollback()

            raise
