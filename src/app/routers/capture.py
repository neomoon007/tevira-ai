from fastapi import APIRouter
from src.app.schemas import NonEmptyString, CaptureRead
from src.app.services.capture import capture_from_text

router = APIRouter(prefix="/capture", tags=["Capture"])


@router.post("/text")
def capture_from_text_endpoint(input: NonEmptyString) -> CaptureRead:
    return capture_from_text(input)
