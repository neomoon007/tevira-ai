from fastapi import APIRouter

from src.tevira_ai.dependencies import DBSession
from src.tevira_ai.schemas import HealthResponse
from src.tevira_ai.services.health import check_health

router = APIRouter(prefix="/health", tags=["Health"])


# -- "/health" --
@router.get("")
async def check_health_endpoint(db: DBSession) -> HealthResponse:
    return await check_health(db)
