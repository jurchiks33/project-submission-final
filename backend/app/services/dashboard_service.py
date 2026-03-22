from app.models.schemas import DashboardPayload, DashboardSummary
from app.services import backtest_service, pipeline_service, signal_service


def get_dashboard() -> DashboardPayload:
    signals = signal_service.list_signals()
    backtest_summary = backtest_service.get_backtest_summary()
    summary = DashboardSummary(
        active_long_positions=sum(1 for item in signals if item.current_state == "Long"),
        new_entries=sum(1 for item in signals if item.action == "Enter Next Opening"),
        new_exits=sum(1 for item in signals if item.action == "Exit Next Opening"),
        blocked_signals=sum(1 for item in signals if item.gate_blocked),
        aggregate_return=backtest_summary.total_return_pct,
        baseline_comparison_count=backtest_summary.beat_baseline_count,
    )
    return DashboardPayload(
        status=pipeline_service.get_pipeline_status(),
        summary=summary,
        signals=signals,
    )
