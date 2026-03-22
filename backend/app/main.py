from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.adapters.file_adapter import ensure_runtime_state
from app.api.routes_backtests import router as backtests_router
from app.api.routes_dashboard import router as dashboard_router
from app.api.routes_pipeline import router as pipeline_router
from app.api.routes_positions import router as positions_router
from app.api.routes_settings import router as settings_router
from app.api.routes_signals import router as signals_router
from app.core.config import get_settings


settings = get_settings()
app = FastAPI(title=settings.app_name)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
def startup() -> None:
    ensure_runtime_state()


@app.get("/health")
def healthcheck() -> dict[str, str]:
    return {"status": "ok"}


app.include_router(pipeline_router, prefix=settings.api_prefix)
app.include_router(dashboard_router, prefix=settings.api_prefix)
app.include_router(signals_router, prefix=settings.api_prefix)
app.include_router(positions_router, prefix=settings.api_prefix)
app.include_router(backtests_router, prefix=settings.api_prefix)
app.include_router(settings_router, prefix=settings.api_prefix)
