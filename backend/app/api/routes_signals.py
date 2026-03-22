from fastapi import APIRouter

from app.models.schemas import SignalRow, TickerSignalDetail
from app.services import signal_service

router = APIRouter(prefix="/signals", tags=["signals"])


@router.get("", response_model=list[SignalRow])
def list_signals() -> list[SignalRow]:
    return signal_service.list_signals()


@router.get("/{ticker}", response_model=TickerSignalDetail)
def get_signal_detail(ticker: str) -> TickerSignalDetail:
    return signal_service.get_signal_detail(ticker)
