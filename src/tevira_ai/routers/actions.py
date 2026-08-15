from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.tevira_ai.db.database import get_db
from src.tevira_ai.schemas import (
    ApplyActionResponse,
    ProposedAction,
)
from src.tevira_ai.services.actions import apply_action

router = APIRouter(prefix="/actions", tags=["Actions"])


@router.post("/apply", status_code=201)
async def apply_action_endpoint(
    action: ProposedAction, db: AsyncSession = Depends(get_db)
) -> ApplyActionResponse:
    return await apply_action(db, action)
