from fastapi import APIRouter

from app.models.schemas import PipelineRunResponse, PipelineStatus
from app.services import pipeline_service

router = APIRouter(prefix="/pipeline", tags=["pipeline"])


@router.post("/run-universe", response_model=PipelineRunResponse)
async def run_universe() -> PipelineRunResponse:
    return await pipeline_service.run_universe_pipeline()


@router.post("/run-ticker/{ticker}", response_model=PipelineRunResponse)
async def run_ticker(ticker: str) -> PipelineRunResponse:
    return await pipeline_service.run_ticker_pipeline(ticker)


@router.get("/status", response_model=PipelineStatus)
def get_status() -> PipelineStatus:
    return pipeline_service.get_pipeline_status()
