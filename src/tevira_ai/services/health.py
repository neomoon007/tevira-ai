from sqlalchemy.ext.asyncio import AsyncSession

from src.tevira_ai.repository.health import HealthRepository
from src.tevira_ai.schemas import HealthResponse


async def check_health(db: AsyncSession) -> HealthResponse:
    repository = HealthRepository(db)

    await repository.check()
    return HealthResponse()
