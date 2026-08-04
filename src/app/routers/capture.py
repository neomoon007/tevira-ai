from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from src.app.db.database import get_db
from src.app.schemas import CaptureRead, NonEmptyString
from src.app.services.capture import capture_from_text

router = APIRouter(prefix="/capture", tags=["Capture"])


@router.post("/text")
def capture_from_text_endpoint(
    input: NonEmptyString, db: Session = Depends(get_db)
) -> CaptureRead:
    return capture_from_text(db, input)
