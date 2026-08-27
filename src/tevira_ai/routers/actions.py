from fastapi import APIRouter

from src.tevira_ai.dependencies import CurrentUserId, DBSession
from src.tevira_ai.schemas import (
    ApplyActionResponse,
    ProposedAction,
)
from src.tevira_ai.services.actions import apply_action

router = APIRouter(prefix="/actions", tags=["Actions"])


@router.post("/apply", status_code=201)
async def apply_action_endpoint(
    action: ProposedAction, owner_id: CurrentUserId, db: DBSession
) -> ApplyActionResponse:
    return await apply_action(owner_id, db, action)
