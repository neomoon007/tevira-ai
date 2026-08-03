from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from src.app.db.database import get_db
from src.app.schemas import ContextRead
from src.app.services.context import restore_context

router = APIRouter(prefix="/context", tags=["Context"])


@router.get("/{project_id}")
def restore_context_endpoint(
    project_id: str, db: Session = Depends(get_db)
) -> ContextRead:
    return restore_context(db, project_id)
