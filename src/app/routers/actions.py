from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from src.app.db.database import get_db
from src.app.schemas import (
    ApplyActionResponse,
    ProposedAction,
)
from src.app.services.actions import apply_action

router = APIRouter(prefix="/actions", tags=["Actions"])


@router.post("/apply", status_code=201)
def apply_action_endpoint(
    action: ProposedAction, db: Session = Depends(get_db)
) -> ApplyActionResponse:
    return apply_action(db, action)
