from datetime import datetime, timezone

from fastapi.concurrency import run_in_threadpool

from app.adapters import pipeline_adapter
from app.models.schemas import PipelineRunResponse, PipelineStatus


def _utc_now() -> datetime:
    return datetime.now(tz=timezone.utc).replace(microsecond=0)


async def run_universe_pipeline() -> PipelineRunResponse:
    started_at = _utc_now()
    state = await run_in_threadpool(pipeline_adapter.run_universe_pipeline_job)
    completed_at = _utc_now()
    return PipelineRunResponse(
        status="success",
        message="Universe pipeline completed.",
        run_type="universe",
        started_at=started_at,
        completed_at=completed_at,
        summary={
            "tickers_processed": state["status"]["tickers_processed"],
            "latest_signal_date": state["status"]["latest_signal_date"],
        },
    )


async def run_ticker_pipeline(ticker: str) -> PipelineRunResponse:
    started_at = _utc_now()
    state = await run_in_threadpool(pipeline_adapter.run_ticker_pipeline_job, ticker)
    completed_at = _utc_now()
    return PipelineRunResponse(
        status="success",
        message=f"Ticker pipeline completed for {ticker.upper()}.",
        run_type="ticker",
        ticker=ticker.upper(),
        started_at=started_at,
        completed_at=completed_at,
        summary={
            "tickers_processed": state["status"]["tickers_processed"],
            "latest_signal_date": state["status"]["latest_signal_date"],
        },
    )


def get_pipeline_status() -> PipelineStatus:
    return PipelineStatus.model_validate(pipeline_adapter.get_pipeline_status())
