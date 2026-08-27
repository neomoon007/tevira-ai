from typing import Annotated
from uuid import UUID

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.tevira_ai.db.database import get_db

DEV_OWNER_ID = UUID("00000000-0000-0000-0000-000000000001")


def get_current_owner_id() -> UUID:
    return DEV_OWNER_ID


type CurrentUserId = Annotated[UUID, Depends(get_current_owner_id)]
type DBSession = Annotated[AsyncSession, Depends(get_db)]
