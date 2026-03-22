from datetime import datetime
from typing import Literal, Optional

from pydantic import BaseModel, Field


ActionType = Literal[
    "Enter Next Opening",
    "Exit Next Opening",
    "Hold Long Position",
    "Flat",
    "Awaiting Next Open Fill",
]

DirectionType = Literal["up", "down"]
ImpactCategory = Literal["momentum", "trend", "volatility", "market", "other"]


class KeyDriver(BaseModel):
    feature: str
    direction: DirectionType
    impact: float
    category: ImpactCategory
    human_reason: str


class GateReasoning(BaseModel):
    trend_gate: bool
    vol_gate: bool
    quality_gate: Optional[bool] = None
    notes: list[str] = Field(default_factory=list)


class ExplanationPayload(BaseModel):
    plain_summary: str
    model_probability: float
    decision_type: str
    final_action: ActionType
    key_drivers: list[KeyDriver] = Field(default_factory=list)
    gate_reasoning: GateReasoning


class SignalRow(BaseModel):
    ticker: str
    signal_date: str
    action: ActionType
    current_state: str
    probability: float
    entry_band: float
    exit_band: float
    trend_gate: bool
    vol_gate: bool
    quality_gate: Optional[bool] = None
    last_close: float
    short_explanation: str
    latest_message: str
    pending_action: Optional[str] = None
    rank: Optional[int] = None
    gate_blocked: bool
    explanation: ExplanationPayload


class TickerSignalDetail(BaseModel):
    ticker: str
    signal_date: str
    action: ActionType
    current_state: str
    pending_action: Optional[str] = None
    latest_message: str
    last_close: float
    probability: float
    entry_band: float
    exit_band: float
    trend_gate: bool
    vol_gate: bool
    quality_gate: Optional[bool] = None
    gate_blocked: bool
    rank: Optional[int] = None
    explanation: ExplanationPayload
    state_transitions: list[str] = Field(default_factory=list)
    risk_notes: list[str] = Field(default_factory=list)


class Position(BaseModel):
    ticker: str
    state: str
    entry_date: Optional[str] = None
    entry_price: Optional[float] = None
    entry_display_price: Optional[float] = None
    current_close: float
    unrealized_pnl: float
    unrealized_pnl_pct: float = 0.0
    probability: float
    entry_band: float
    exit_band: float
    latest_message: str
    pending_action: Optional[str] = None


class PipelineStatus(BaseModel):
    status: Literal["idle", "running", "succeeded", "failed"]
    latest_run_time: Optional[datetime] = None
    latest_signal_date: Optional[str] = None
    tickers_processed: int = 0
    last_error: Optional[str] = None
    last_run_mode: Optional[str] = None


class DashboardSummary(BaseModel):
    active_long_positions: int
    new_entries: int
    new_exits: int
    blocked_signals: int
    aggregate_return: float
    baseline_comparison_count: int


class DashboardPayload(BaseModel):
    status: PipelineStatus
    summary: DashboardSummary
    signals: list[SignalRow]


class EquityPoint(BaseModel):
    date: str
    strategy: float
    baseline: Optional[float] = None


class BacktestSummary(BaseModel):
    total_start_value: float
    total_end_value: float
    total_pnl: float
    total_return_pct: float
    tickers_processed: int
    beat_baseline_count: int


class BacktestMetricSet(BaseModel):
    total_return_pct: float
    max_drawdown_pct: float
    volatility_pct: float
    total_trades: int
    win_rate_pct: float
    profit_factor: float
    expectancy: float


class BacktestDetail(BaseModel):
    ticker: str
    period_label: str
    metrics: BacktestMetricSet
    baseline_metrics: Optional[BacktestMetricSet] = None
    equity_curve: list[EquityPoint] = Field(default_factory=list)


class RuntimeSettings(BaseModel):
    seq_len: int
    epochs: int
    patience: int
    split_mode: str
    val_years: int
    test_years: int
    target_mode: str
    use_band: bool
    thr_entry: float
    thr_exit: float
    use_trend_gate: bool
    use_vol_gate: bool
    fees: float
    slippage: float


class PipelineRunResponse(BaseModel):
    status: Literal["success", "error"]
    message: str
    run_type: Literal["universe", "ticker", "refresh"]
    ticker: Optional[str] = None
    started_at: datetime
    completed_at: datetime
    summary: dict = Field(default_factory=dict)
