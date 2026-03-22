from app.adapters import pipeline_adapter
from app.models.schemas import BacktestDetail, BacktestSummary


def get_backtest_summary() -> BacktestSummary:
    return BacktestSummary.model_validate(pipeline_adapter.get_backtest_summary())


def get_ticker_backtest(ticker: str) -> BacktestDetail:
    return BacktestDetail.model_validate(pipeline_adapter.get_ticker_backtest(ticker))
