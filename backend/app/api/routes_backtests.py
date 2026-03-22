from fastapi import APIRouter

from app.models.schemas import BacktestDetail, BacktestSummary
from app.services import backtest_service

router = APIRouter(prefix="/backtests", tags=["backtests"])


@router.get("/summary", response_model=BacktestSummary)
def get_summary() -> BacktestSummary:
    return backtest_service.get_backtest_summary()


@router.get("/{ticker}", response_model=BacktestDetail)
def get_ticker_backtest(ticker: str) -> BacktestDetail:
    return backtest_service.get_ticker_backtest(ticker)
