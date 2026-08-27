from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession

from src.tevira_ai.exceptions import ResourceNotFoundError
from src.tevira_ai.repository.projects import Project, ProjectRepository
from src.tevira_ai.schemas import ProjectCreate, ProjectRead


async def get_project(
    owner_id: UUID, db: AsyncSession, project_id: UUID
) -> ProjectRead:
    repository = ProjectRepository(db)

    project_from_db = await repository.get_by_id(owner_id, project_id)

    if not project_from_db:
        raise ResourceNotFoundError(
            resource_type="Project",
            resource_id=str(project_id),
        )

    return ProjectRead.model_validate(project_from_db)


async def create_project(
    owner_id: UUID, db: AsyncSession, project: ProjectCreate
) -> ProjectRead:
    repository = ProjectRepository(db)

    project_in = Project(
        **project.model_dump(),
        owner_id=owner_id,
    )

    project_out = await repository.create(project_in)

    return ProjectRead.model_validate(project_out)


async def list_projects(owner_id: UUID, db: AsyncSession) -> list[ProjectRead]:
    repository = ProjectRepository(db)

    projects_from_db = await repository.get_all(owner_id)

    return [ProjectRead.model_validate(project) for project in projects_from_db]


async def rename_project(
    owner_id: UUID, db: AsyncSession, new_title: ProjectCreate, project_id: UUID
) -> ProjectRead:
    await get_project(owner_id, db, project_id)

    renamed_project = ProjectRead(
        **new_title.model_dump(),
        id=project_id,
    )

    repository = ProjectRepository(db)

    project_result = await repository.rename(owner_id, renamed_project)

    return ProjectRead.model_validate(project_result)


async def delete_project(owner_id: UUID, db: AsyncSession, project_id: UUID) -> None:
    await get_project(owner_id, db, project_id)

    repository = ProjectRepository(db)
    await repository.delete(owner_id, project_id)
