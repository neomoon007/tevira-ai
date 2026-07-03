from fastapi import Depends, APIRouter
from src.app.services.context import restore_context
from src.app.utils import (
    get_project,
)
from src.app.schemas import ContextRead

router = APIRouter(prefix="/context", tags=["Context"])


@router.get("/{project_id}")
def restore_context_endpoint(project_id: str = Depends(get_project)) -> ContextRead:
    return restore_context(project_id)