from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from src.tevira_ai.db.database import get_db
from src.tevira_ai.schemas import CaptureRead, NonEmptyString
from src.tevira_ai.services.capture import capture_from_text

router = APIRouter(prefix="/capture", tags=["Capture"])


@router.post("/text")
def capture_from_text_endpoint(
    input: NonEmptyString, db: Session = Depends(get_db)
) -> CaptureRead:
    return capture_from_text(db, input)
