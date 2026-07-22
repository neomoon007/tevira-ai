from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from sqlalchemy import select, func, delete, desc, cast, Integer
from src.app.db.models import Project
from src.app.schemas import ProjectRead


class ProjectRepository:
    def __init__(self, session: Session):
        self.session = session

    def create(self, project: Project) -> Project:
        self.session.add(project)
        self.session.commit()
        self.session.refresh(project)

        return project

    def get_highest_id(self, owner_id: str) -> int:
        clean_number = func.regexp_replace(Project.id, r"\D", "", "g")
        num_only_from_id = cast(clean_number, Integer)
        query = (
            select(num_only_from_id)
            .where(Project.owner_id == owner_id)
            .order_by(desc(num_only_from_id))
            .limit(1)
        )

        highest_project_id = self.session.scalars(query).first()

        return highest_project_id if highest_project_id is not None else 0

    def get_by_id(self, owner_id: str, project_id: str) -> Project | None:
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

    def delete(self, owner_id: str, project_id: str):
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
