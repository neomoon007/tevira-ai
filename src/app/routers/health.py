from fastapi import APIRouter

router = APIRouter(prefix="/health")


# -- "/health" --
@router.get("")
def check_health():
    return {"status": "ok", "service": "tevira-ai"}
