from fastapi import APIRouter

from app.models.schemas import Position
from app.services import ledger_service

router = APIRouter(prefix="/positions", tags=["positions"])


@router.get("", response_model=list[Position])
def get_positions() -> list[Position]:
    return ledger_service.get_positions()
