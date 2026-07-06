from fastapi import APIRouter
from src.app.schemas import (
    ProposedAction,
    ApplyActionResponse,
)
from src.app.services.actions import apply_action

router = APIRouter(prefix="/actions", tags=["Actions"])


@router.post("/apply", status_code=201)
def apply_action_endpoint(action: ProposedAction) -> ApplyActionResponse:
    return apply_action(action)
