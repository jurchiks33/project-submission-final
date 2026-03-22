export type ActionType =
  | "Enter Next Opening"
  | "Exit Next Opening"
  | "Hold Long Position"
  | "Flat"
  | "Awaiting Next Open Fill";

export type DriverCategory = "momentum" | "trend" | "volatility" | "market" | "other";

export interface KeyDriver {
  feature: string;
  direction: "up" | "down";
  impact: number;
  category: DriverCategory;
  human_reason: string;
}

export interface GateReasoning {
  trend_gate: boolean;
  vol_gate: boolean;
  quality_gate: boolean | null;
  notes: string[];
}

export interface ExplanationPayload {
  plain_summary: string;
  model_probability: number;
  decision_type: string;
  final_action: ActionType;
  key_drivers: KeyDriver[];
  gate_reasoning: GateReasoning;
}

export interface SignalRow {
  ticker: string;
  signal_date: string;
  action: ActionType;
  current_state: string;
  probability: number;
  entry_band: number;
  exit_band: number;
  trend_gate: boolean;
  vol_gate: boolean;
  quality_gate: boolean | null;
  last_close: number;
  short_explanation: string;
  latest_message: string;
  pending_action: string | null;
  rank: number | null;
  gate_blocked: boolean;
  explanation: ExplanationPayload;
}

export interface TickerDetail extends SignalRow {
  state_transitions: string[];
  risk_notes: string[];
}

export interface Position {
  ticker: string;
  state: string;
  entry_date: string | null;
  entry_price: number | null;
  entry_display_price: number | null;
  current_close: number;
  unrealized_pnl: number;
  unrealized_pnl_pct: number;
  probability: number;
  entry_band: number;
  exit_band: number;
  latest_message: string;
  pending_action: string | null;
}

export interface PipelineStatus {
  status: "idle" | "running" | "succeeded" | "failed";
  latest_run_time: string | null;
  latest_signal_date: string | null;
  tickers_processed: number;
  last_error: string | null;
  last_run_mode: string | null;
}

export interface DashboardSummary {
  active_long_positions: number;
  new_entries: number;
  new_exits: number;
  blocked_signals: number;
  aggregate_return: number;
  baseline_comparison_count: number;
}

export interface DashboardPayload {
  status: PipelineStatus;
  summary: DashboardSummary;
  signals: SignalRow[];
}

export interface EquityPoint {
  date: string;
  strategy: number;
  baseline: number | null;
}

export interface BacktestSummary {
  total_start_value: number;
  total_end_value: number;
  total_pnl: number;
  total_return_pct: number;
  tickers_processed: number;
  beat_baseline_count: number;
}

export interface BacktestMetricSet {
  total_return_pct: number;
  max_drawdown_pct: number;
  volatility_pct: number;
  total_trades: number;
  win_rate_pct: number;
  profit_factor: number;
  expectancy: number;
}

export interface BacktestDetail {
  ticker: string;
  period_label: string;
  metrics: BacktestMetricSet;
  baseline_metrics: BacktestMetricSet | null;
  equity_curve: EquityPoint[];
}

export interface RuntimeSettings {
  seq_len: number;
  epochs: number;
  patience: number;
  split_mode: string;
  val_years: number;
  test_years: number;
  target_mode: string;
  use_band: boolean;
  thr_entry: number;
  thr_exit: number;
  use_trend_gate: boolean;
  use_vol_gate: boolean;
  fees: number;
  slippage: number;
}

export interface PipelineRunResponse {
  status: "success" | "error";
  message: string;
  run_type: "universe" | "ticker" | "refresh";
  ticker: string | null;
  started_at: string;
  completed_at: string;
  summary: Record<string, unknown>;
}
