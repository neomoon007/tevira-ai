from sqlalchemy.ext.asyncio import AsyncSession

from src.tevira_ai.repository.health import HealthRepository


async def check_health(db: AsyncSession):
    repository = HealthRepository(db)

    try:
        health_status_from_db = await repository.check()
        return health_status_from_db
    except Exception as e:
        return f"DB NOT WORKING: {e}"
