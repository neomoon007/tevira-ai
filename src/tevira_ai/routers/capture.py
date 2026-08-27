from fastapi import APIRouter

from src.tevira_ai.dependencies import CurrentUserId, DBSession
from src.tevira_ai.schemas import CaptureRead, NonEmptyString
from src.tevira_ai.services.capture import capture_from_text

router = APIRouter(prefix="/capture", tags=["Capture"])


@router.post("/text")
async def capture_from_text_endpoint(
    input: NonEmptyString, owner_id: CurrentUserId, db: DBSession
) -> CaptureRead:
    return await capture_from_text(owner_id, db, input)
