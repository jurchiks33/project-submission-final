from __future__ import annotations

from datetime import datetime, timedelta, timezone
from typing import Optional


UTC = timezone.utc


def _drivers(momentum_up: bool, trend_up: bool, vol_ok: bool) -> list[dict]:
    return [
        {
            "feature": "RSI",
            "direction": "up" if momentum_up else "down",
            "impact": 0.71 if momentum_up else 0.42,
            "category": "momentum",
            "human_reason": "Momentum remained supportive over the recent lookback window."
            if momentum_up
            else "Momentum softened and reduced conviction in the long setup.",
        },
        {
            "feature": "MA200 Trend",
            "direction": "up" if trend_up else "down",
            "impact": 0.64 if trend_up else 0.56,
            "category": "trend",
            "human_reason": "Price stayed above the longer-term trend filter."
            if trend_up
            else "The longer-term trend filter was not supportive.",
        },
        {
            "feature": "ATRp",
            "direction": "up" if vol_ok else "down",
            "impact": 0.33 if vol_ok else 0.59,
            "category": "volatility",
            "human_reason": "Volatility remained inside the acceptable operating band."
            if vol_ok
            else "Volatility moved outside the allowed band and reduced execution quality.",
        },
        {
            "feature": "Market Breadth",
            "direction": "up",
            "impact": 0.28,
            "category": "market",
            "human_reason": "Market breadth provided a mild supportive regime backdrop.",
        },
    ]


def _explanation(
    *,
    action: str,
    probability: float,
    trend_gate: bool,
    vol_gate: bool,
    quality_gate: Optional[bool],
    summary: str,
    decision_type: str,
    notes: list[str],
) -> dict:
    return {
        "plain_summary": summary,
        "model_probability": probability,
        "decision_type": decision_type,
        "final_action": action,
        "key_drivers": _drivers(probability >= 0.55, trend_gate, vol_gate),
        "gate_reasoning": {
            "trend_gate": trend_gate,
            "vol_gate": vol_gate,
            "quality_gate": quality_gate,
            "notes": notes,
        },
    }


def build_initial_state() -> dict:
    now = datetime.now(tz=UTC).replace(microsecond=0)
    signal_date = "2026-03-17"
    signals = [
        {
            "ticker": "MSFT",
            "signal_date": signal_date,
            "action": "Hold Long Position",
            "current_state": "Long",
            "probability": 0.68,
            "entry_band": 0.61,
            "exit_band": 0.45,
            "trend_gate": True,
            "vol_gate": True,
            "quality_gate": True,
            "last_close": 421.18,
            "short_explanation": "Long signal remains valid with gates passing.",
            "latest_message": "Hold Long Position (MSFT) | prob_up=68.00% | close=421.18",
            "pending_action": None,
            "rank": 2,
            "gate_blocked": False,
            "explanation": _explanation(
                action="Hold Long Position",
                probability=0.68,
                trend_gate=True,
                vol_gate=True,
                quality_gate=True,
                summary="Long signal supported by positive trend and acceptable volatility.",
                decision_type="hold",
                notes=[
                    "Probability remains above the exit band.",
                    "Trend and volatility filters both passed.",
                    "Ledger already shows an open long position.",
                ],
            ),
            "state_transitions": [
                "Entered on prior signal.",
                "Remains long after latest after-close evaluation.",
            ],
            "risk_notes": [
                "Position remains exposed to overnight gap risk.",
                "No new entry is required because the ledger is already long.",
            ],
        },
        {
            "ticker": "NVDA",
            "signal_date": signal_date,
            "action": "Enter Next Opening",
            "current_state": "Flat",
            "probability": 0.74,
            "entry_band": 0.64,
            "exit_band": 0.48,
            "trend_gate": True,
            "vol_gate": True,
            "quality_gate": True,
            "last_close": 913.44,
            "short_explanation": "Probability cleared the entry band and all gates passed.",
            "latest_message": "Enter Next Opening (NVDA) | prob_up=74.00% | close=913.44",
            "pending_action": "Awaiting Next Open Fill",
            "rank": 1,
            "gate_blocked": False,
            "explanation": _explanation(
                action="Enter Next Opening",
                probability=0.74,
                trend_gate=True,
                vol_gate=True,
                quality_gate=True,
                summary="Entry signal supported by strong model probability, positive trend, and acceptable volatility.",
                decision_type="enter",
                notes=[
                    "Probability cleared the entry band.",
                    "Trend gate passed.",
                    "Volatility gate passed.",
                    "Ticker ranked inside the allowed quality bucket.",
                ],
            ),
            "state_transitions": [
                "Current state is flat.",
                "System will attempt entry on the next market open.",
            ],
            "risk_notes": [
                "Entry is queued for the next session open, not immediate execution.",
            ],
        },
        {
            "ticker": "META",
            "signal_date": signal_date,
            "action": "Flat",
            "current_state": "Flat",
            "probability": 0.57,
            "entry_band": 0.63,
            "exit_band": 0.46,
            "trend_gate": True,
            "vol_gate": True,
            "quality_gate": False,
            "last_close": 507.82,
            "short_explanation": "Probability was decent, but ranking and entry threshold were not strong enough.",
            "latest_message": "Flat: No long (META) | prob_up=57.00% | entry>=0.63 | close=507.82",
            "pending_action": None,
            "rank": 8,
            "gate_blocked": True,
            "explanation": _explanation(
                action="Flat",
                probability=0.57,
                trend_gate=True,
                vol_gate=True,
                quality_gate=False,
                summary="Flat because the probability did not clear the entry band and the quality filter did not approve the setup.",
                decision_type="blocked",
                notes=[
                    "Probability stayed below the configured entry band.",
                    "Quality or rank filter rejected the setup.",
                ],
            ),
            "state_transitions": [
                "Remains flat because no entry condition was fully satisfied.",
            ],
            "risk_notes": [
                "Setup is watchlist-worthy, but not strong enough for the next open.",
            ],
        },
        {
            "ticker": "AAPL",
            "signal_date": signal_date,
            "action": "Exit Next Opening",
            "current_state": "Long",
            "probability": 0.39,
            "entry_band": 0.6,
            "exit_band": 0.45,
            "trend_gate": False,
            "vol_gate": True,
            "quality_gate": True,
            "last_close": 213.57,
            "short_explanation": "Exit triggered after probability fell below the exit threshold and trend weakened.",
            "latest_message": "Exit Next Opening (AAPL) | prob_up=39.00% | close=213.57",
            "pending_action": "Exit queued for next open",
            "rank": 12,
            "gate_blocked": True,
            "explanation": _explanation(
                action="Exit Next Opening",
                probability=0.39,
                trend_gate=False,
                vol_gate=True,
                quality_gate=True,
                summary="Exit scheduled because the model probability fell below the exit band and the trend filter turned negative.",
                decision_type="exit",
                notes=[
                    "Probability moved below the exit threshold.",
                    "Trend gate failed.",
                    "System is long in the ledger, so the state transition becomes an exit.",
                ],
            ),
            "state_transitions": [
                "Current state is long.",
                "Exit will be processed on the next market open.",
            ],
            "risk_notes": [
                "Exposure remains overnight until the next open exit is completed.",
            ],
        },
        {
            "ticker": "GOOGL",
            "signal_date": signal_date,
            "action": "Flat",
            "current_state": "Flat",
            "probability": 0.51,
            "entry_band": 0.62,
            "exit_band": 0.46,
            "trend_gate": True,
            "vol_gate": False,
            "quality_gate": True,
            "last_close": 172.4,
            "short_explanation": "Entry blocked by volatility gate despite a neutral-to-positive probability.",
            "latest_message": "Flat: Band passed but vol gate blocked (GOOGL) | prob_up=51.00% | close=172.40",
            "pending_action": None,
            "rank": 6,
            "gate_blocked": True,
            "explanation": _explanation(
                action="Flat",
                probability=0.51,
                trend_gate=True,
                vol_gate=False,
                quality_gate=True,
                summary="Flat because the setup failed the volatility gate, even though the overall regime was supportive.",
                decision_type="blocked",
                notes=[
                    "Volatility moved outside the acceptable band.",
                    "Trend gate passed, but rules require both key gates.",
                ],
            ),
            "state_transitions": [
                "State remains flat because no valid entry was allowed.",
            ],
            "risk_notes": [
                "Waiting for calmer volatility before allowing a new long.",
            ],
        },
    ]

    positions = [
        {
            "ticker": "MSFT",
            "state": "Long",
            "entry_date": "2026-03-11",
            "entry_price": 409.12,
            "current_close": 421.18,
            "unrealized_pnl": 2.95,
            "probability": 0.68,
            "entry_band": 0.61,
            "exit_band": 0.45,
            "latest_message": "Hold Long Position (MSFT)",
            "pending_action": None,
        },
        {
            "ticker": "AAPL",
            "state": "Long",
            "entry_date": "2026-03-05",
            "entry_price": 219.31,
            "current_close": 213.57,
            "unrealized_pnl": -2.62,
            "probability": 0.39,
            "entry_band": 0.60,
            "exit_band": 0.45,
            "latest_message": "Exit Next Opening (AAPL)",
            "pending_action": "Exit queued for next open",
        },
        {
            "ticker": "NVDA",
            "state": "Awaiting Next Open Fill",
            "entry_date": None,
            "entry_price": None,
            "current_close": 913.44,
            "unrealized_pnl": 0.0,
            "probability": 0.74,
            "entry_band": 0.64,
            "exit_band": 0.48,
            "latest_message": "Enter Next Opening (NVDA)",
            "pending_action": "Awaiting Next Open Fill",
        },
    ]

    equity_curve = [
        {"date": (now - timedelta(days=6 - idx)).date().isoformat(), "strategy": value, "baseline": base}
        for idx, (value, base) in enumerate(
            [
                (10000, 10000),
                (10085, 10032),
                (10162, 10094),
                (10131, 10070),
                (10244, 10108),
                (10302, 10166),
                (10388, 10204),
            ]
        )
    ]

    backtest_detail = {
        "ticker": "MSFT",
        "period_label": "Test window (latest 2 years)",
        "metrics": {
            "total_return_pct": 18.6,
            "max_drawdown_pct": 7.9,
            "volatility_pct": 13.1,
            "total_trades": 24,
            "win_rate_pct": 62.5,
            "profit_factor": 1.83,
            "expectancy": 142.2,
        },
        "baseline_metrics": {
            "total_return_pct": 11.2,
            "max_drawdown_pct": 12.4,
            "volatility_pct": 15.6,
            "total_trades": 1,
            "win_rate_pct": 100.0,
            "profit_factor": 1.0,
            "expectancy": 0.0,
        },
        "equity_curve": equity_curve,
    }

    return {
        "status": {
            "status": "idle",
            "latest_run_time": now.isoformat(),
            "latest_signal_date": signal_date,
            "tickers_processed": len(signals),
            "last_error": None,
            "last_run_mode": "universe",
        },
        "signals": signals,
        "positions": positions,
        "backtests": {
            "summary": {
                "total_start_value": 10000.0,
                "total_end_value": 10388.0,
                "total_pnl": 388.0,
                "total_return_pct": 3.88,
                "tickers_processed": len(signals),
                "beat_baseline_count": 3,
            },
            "details": {
                "MSFT": backtest_detail,
                "NVDA": {
                    **backtest_detail,
                    "ticker": "NVDA",
                    "metrics": {
                        "total_return_pct": 23.4,
                        "max_drawdown_pct": 9.4,
                        "volatility_pct": 18.9,
                        "total_trades": 19,
                        "win_rate_pct": 57.9,
                        "profit_factor": 1.94,
                        "expectancy": 188.0,
                    },
                },
                "META": {
                    **backtest_detail,
                    "ticker": "META",
                    "metrics": {
                        "total_return_pct": 9.7,
                        "max_drawdown_pct": 8.1,
                        "volatility_pct": 14.8,
                        "total_trades": 18,
                        "win_rate_pct": 55.6,
                        "profit_factor": 1.42,
                        "expectancy": 86.2,
                    },
                },
                "AAPL": {
                    **backtest_detail,
                    "ticker": "AAPL",
                    "metrics": {
                        "total_return_pct": 7.3,
                        "max_drawdown_pct": 10.6,
                        "volatility_pct": 15.3,
                        "total_trades": 21,
                        "win_rate_pct": 52.4,
                        "profit_factor": 1.27,
                        "expectancy": 54.0,
                    },
                },
                "GOOGL": {
                    **backtest_detail,
                    "ticker": "GOOGL",
                    "metrics": {
                        "total_return_pct": 6.9,
                        "max_drawdown_pct": 6.8,
                        "volatility_pct": 12.9,
                        "total_trades": 14,
                        "win_rate_pct": 57.1,
                        "profit_factor": 1.35,
                        "expectancy": 49.8,
                    },
                },
            },
        },
        "settings": {
            "seq_len": 30,
            "epochs": 120,
            "patience": 8,
            "split_mode": "by_date",
            "val_years": 3,
            "test_years": 5,
            "target_mode": "riskadj_sign",
            "use_band": True,
            "thr_entry": 0.60,
            "thr_exit": 0.45,
            "use_trend_gate": True,
            "use_vol_gate": True,
            "fees": 0.001,
            "slippage": 0.001,
        },
    }
