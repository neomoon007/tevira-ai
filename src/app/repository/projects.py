from sqlalchemy.orm import Session
from sqlalchemy import select, func, desc, cast, Integer
from src.app.db.models import Project


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
