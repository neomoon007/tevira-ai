from fastapi import APIRouter
from src.app.schemas import NonEmptyString, CaptureRead, ProposedAction, CreateProgressNoteProposal, CreateTaskProposal
from src.app.parser import parse_note
from src.app.state.memory import projects_in_memory
from src.app.utils import capture_from_text

router = APIRouter(prefix="/capture", tags=["Capture"])


@router.post("/text")
def capture_text(input: NonEmptyString) -> CaptureRead:
    return capture_from_text(input)