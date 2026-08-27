from uuid import UUID

from sqlalchemy import delete, select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from src.tevira_ai.db.models import Project
from src.tevira_ai.exceptions import DomainException, ResourceInUseError
from src.tevira_ai.schemas import ProjectRead


class ProjectRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create(self, project: Project) -> Project:
        self.session.add(project)
        await self.session.commit()
        await self.session.refresh(project)

        return project

    async def get_by_id(self, owner_id: UUID, project_id: UUID) -> Project | None:
        query_result = await self.session.scalar(
            select(Project).where(
                Project.owner_id == owner_id, Project.id == project_id
            )
        )

        return query_result

    async def get_all(self, owner_id: UUID) -> list[Project]:
        query_result = await self.session.scalars(
            select(Project).where(Project.owner_id == owner_id)
        )

        return list(query_result.all())

    async def rename(
        self, owner_id: UUID, renamed_project: ProjectRead
    ) -> Project | None:
        project = await self.session.scalar(
            select(Project).where(
                Project.owner_id == owner_id, Project.id == renamed_project.id
            )
        )

        if project:
            project.title = renamed_project.title

            await self.session.commit()
            await self.session.refresh(project)

            return project

    async def delete(self, owner_id: UUID, project_id: UUID):
        try:
            await self.session.execute(
                delete(Project).where(
                    Project.owner_id == owner_id, Project.id == project_id
                )
            )
            await self.session.commit()

        except IntegrityError:
            await self.session.rollback()

            raise ResourceInUseError(
                resource_type="Project",
                resource_id=str(project_id),
            )

    async def get_default_project_id(self, owner_id: UUID) -> UUID:
        default_project_id = await self.session.scalar(
            select(Project.id)
            .where(Project.owner_id == owner_id)
            .order_by(Project.id.asc())
        )

        if not default_project_id:
            raise DomainException(
                status_code=404,
                error_code="NO_DEFAULT_PROJECT",
                message="No projects in the database to use as default project.",
            )

        return default_project_id

    async def get_project_id_by_title(self, owner_id: UUID, title_list: list) -> UUID:
        project_id = await self.session.scalar(
            select(Project.id).where(
                Project.owner_id == owner_id, Project.title.in_(title_list)
            )
        )

        if project_id:
            return project_id

        return await self.get_default_project_id(owner_id=owner_id)
