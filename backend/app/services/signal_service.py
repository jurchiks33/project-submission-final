from fastapi import HTTPException

from app.adapters import pipeline_adapter
from app.models.schemas import SignalRow, TickerSignalDetail


def list_signals() -> list[SignalRow]:
    return [SignalRow.model_validate(item) for item in pipeline_adapter.get_latest_signal_snapshot()]


def get_signal_detail(ticker: str) -> TickerSignalDetail:
    try:
        detail = pipeline_adapter.get_ticker_signal_detail(ticker)
    except KeyError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc
    return TickerSignalDetail.model_validate(detail)
