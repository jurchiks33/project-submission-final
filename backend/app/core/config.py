from functools import lru_cache
from pathlib import Path
from typing import Optional

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "Trading Advisor Bot API"
    app_env: str = "development"
    api_prefix: str = "/api"
    cors_origins: list[str] = ["http://localhost:5173"]
    data_dir: Path = Path(__file__).resolve().parents[2] / "data"
    runtime_state_file: str = "runtime_state.json"
    notebook_path: Path = Path(__file__).resolve().parents[3] / "SCANNING USE THIS ONE v3 .ipynb"
    engine_python_path: Path = Path(__file__).resolve().parents[3] / "ZOE ML" / "bin" / "python"
    trading_engine_module: Optional[str] = None
    trading_universe_function: str = "run_universe_pipeline"
    trading_ticker_function: str = "run_ticker_pipeline"
    trading_snapshot_function: str = "get_latest_signal_snapshot"
    trading_detail_function: str = "get_ticker_signal_detail"
    trading_positions_function: str = "get_positions_snapshot"
    trading_backtest_summary_function: str = "get_backtest_summary"
    trading_backtest_ticker_function: str = "get_ticker_backtest"

    model_config = SettingsConfigDict(
        env_prefix="TRADING_APP_",
        env_file=".env",
        extra="ignore",
    )

    @property
    def runtime_state_path(self) -> Path:
        return self.data_dir / self.runtime_state_file


@lru_cache
def get_settings() -> Settings:
    return Settings()
