import uuid

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.tevira_ai.db.database import get_db
from src.tevira_ai.schemas import ContextRead
from src.tevira_ai.services.context import restore_context

router = APIRouter(prefix="/context", tags=["Context"])


@router.get("/{project_id}")
async def restore_context_endpoint(
    project_id: uuid.UUID, db: AsyncSession = Depends(get_db)
) -> ContextRead:
    return await restore_context(db, project_id)
