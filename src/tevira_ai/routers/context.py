import uuid

from fastapi import APIRouter

from src.tevira_ai.dependencies import CurrentUserId, DBSession
from src.tevira_ai.schemas import ContextRead
from src.tevira_ai.services.context import restore_context

router = APIRouter(prefix="/context", tags=["Context"])


@router.get("/{project_id}")
async def restore_context_endpoint(
    project_id: uuid.UUID, owner_id: CurrentUserId, db: DBSession
) -> ContextRead:
    return await restore_context(owner_id, db, project_id)
