from __future__ import annotations

import importlib
import json
import re
import subprocess
import tempfile
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Callable, Optional

from app.adapters.file_adapter import ensure_runtime_state, read_runtime_state, write_runtime_state
from app.core.config import get_settings

SIGNAL_LINE_RE = re.compile(
    r"^(?P<label>.+?) \((?P<ticker>[A-Z0-9.\-]+)\) \((?P<date>\d{4}-\d{2}-\d{2})\)\s+\|\s+prob_up=(?P<prob>[\d.]+)%(?P<rest>.*)$"
)
BACKTEST_LINE_RE = re.compile(
    r"^\[(?P<ticker>[A-Z0-9.\-]+)\] model_ret=(?P<ret>-?[\d.]+)% \| vol=(?P<vol>[\d.]+)% \| "
    r"mdd=(?P<mdd>[\d.]+)% \| baseline_ret=(?P<baseline>-?[\d.]+)%$"
)


def _utc_now() -> datetime:
    return datetime.now(tz=timezone.utc).replace(microsecond=0)


def _load_engine_module():
    settings = get_settings()
    module_name = settings.trading_engine_module
    if not module_name:
        return None
    return importlib.import_module(module_name)


def _resolve_function(name: str) -> Optional[Callable[..., Any]]:
    module = _load_engine_module()
    if module is None:
        return None
    return getattr(module, name, None)


def _project_root() -> Path:
    return Path(__file__).resolve().parents[3]


def _notebook_path() -> Path:
    return get_settings().notebook_path


def _engine_python_path() -> Path:
    configured = get_settings().engine_python_path
    return configured if configured.exists() else Path("python3")


def _load_band_for_ticker(ticker: str) -> tuple[float, float]:
    band_path = _project_root() / "artifacts" / "bands" / f"{ticker}_band.json"
    if band_path.exists():
        data = json.loads(band_path.read_text(encoding="utf-8"))
        return float(data.get("entry", 0.6)), float(data.get("exit", 0.45))
    return 0.6, 0.45


def _build_explanation(action: str, probability: float, trend_gate: bool, vol_gate: bool, line: str) -> dict[str, Any]:
    if action == "Enter Next Opening":
        plain_summary = "Entry signal supported by model probability clearing the band and the required gates passing."
        decision_type = "enter"
        notes = [
            "Probability cleared the entry band.",
            "Trend gate passed.",
            "Volatility gate passed.",
        ]
    elif action == "Exit Next Opening":
        plain_summary = "Exit scheduled because the active long setup no longer satisfies the holding conditions."
        decision_type = "exit"
        notes = [
            "The long position is being unwound at the next opening print.",
            "Model/rule state no longer supports holding the position.",
        ]
    elif action == "Hold Long Position":
        plain_summary = "Long position remains valid because the state machine did not trigger an exit."
        decision_type = "hold"
        notes = [
            "The ledger is already long.",
            "No exit rule was triggered on the latest after-close pass.",
        ]
    elif "trend gate blocked" in line.lower():
        plain_summary = "Flat because the trend gate failed even though the raw model score was constructive."
        decision_type = "blocked"
        notes = [
            "Trend gate failed.",
            "Entry is blocked until the broader trend condition improves.",
        ]
    elif "vol gate blocked" in line.lower():
        plain_summary = "Flat because the volatility gate failed and the setup was considered too unstable."
        decision_type = "blocked"
        notes = [
            "Volatility gate failed.",
            "Entry is blocked until volatility returns to the acceptable range.",
        ]
    else:
        plain_summary = "Flat because the probability did not clear the entry band."
        decision_type = "flat"
        notes = [
            "Probability remained below the required entry band.",
            "No new long was approved for the next open.",
        ]

    return {
        "plain_summary": plain_summary,
        "model_probability": probability,
        "decision_type": decision_type,
        "final_action": action,
        "key_drivers": [
            {
                "feature": "Model probability",
                "direction": "up" if probability >= 0.5 else "down",
                "impact": round(abs(probability - 0.5) * 2, 2),
                "category": "momentum",
                "human_reason": "The final classifier probability was a primary input into the trading decision.",
            },
            {
                "feature": "Trend gate",
                "direction": "up" if trend_gate else "down",
                "impact": 0.7 if trend_gate else 0.7,
                "category": "trend",
                "human_reason": "The system checks whether the broader trend regime is supportive before allowing entries.",
            },
            {
                "feature": "Volatility gate",
                "direction": "up" if vol_gate else "down",
                "impact": 0.55,
                "category": "volatility",
                "human_reason": "Volatility must remain inside the configured band for a fresh entry to be considered tradable.",
            },
            {
                "feature": "Market regime",
                "direction": "up" if trend_gate and vol_gate else "down",
                "impact": 0.35,
                "category": "market",
                "human_reason": "The final action combines raw model output with regime-style rule filters.",
            },
        ],
        "gate_reasoning": {
            "trend_gate": trend_gate,
            "vol_gate": vol_gate,
            "quality_gate": None,
            "notes": notes,
        },
    }


def _parse_signal_line(line: str) -> Optional[dict[str, Any]]:
    match = SIGNAL_LINE_RE.match(line.strip())
    if not match:
        return None

    label = match.group("label")
    ticker = match.group("ticker")
    signal_date = match.group("date")
    probability = float(match.group("prob")) / 100.0
    rest = match.group("rest")
    entry_band_file, exit_band = _load_band_for_ticker(ticker)

    entry_match = re.search(r"(?:entry≥|band≥)([\d.]+)", rest)
    entry_band = float(entry_match.group(1)) if entry_match else entry_band_file
    close_match = re.search(r"close=([\d,]+\.\d+)", rest)
    last_close = float(close_match.group(1).replace(",", "")) if close_match else 0.0

    if label.startswith("Enter Next Opening"):
        action = "Enter Next Opening"
        current_state = "Flat"
        pending_action = "Awaiting Next Open Fill"
    elif label.startswith("Exit Next Opening"):
        action = "Exit Next Opening"
        current_state = "Long"
        pending_action = "Exit queued for next open"
    elif label.startswith("Hold Long Position"):
        action = "Hold Long Position"
        current_state = "Long"
        pending_action = None
    else:
        action = "Flat"
        current_state = "Flat"
        pending_action = None

    trend_gate = "trend gate blocked" not in label.lower() and "trend=BLOCK" not in rest
    vol_gate = "vol gate blocked" not in label.lower() and "vol=BLOCK" not in rest
    gate_blocked = action == "Flat"

    short_explanation = _build_explanation(action, probability, trend_gate, vol_gate, line)["plain_summary"]
    explanation = _build_explanation(action, probability, trend_gate, vol_gate, line)

    return {
        "ticker": ticker,
        "signal_date": signal_date,
        "action": action,
        "current_state": current_state,
        "probability": probability,
        "entry_band": entry_band,
        "exit_band": exit_band,
        "trend_gate": trend_gate,
        "vol_gate": vol_gate,
        "quality_gate": None,
        "last_close": last_close,
        "short_explanation": short_explanation,
        "latest_message": line.strip(),
        "pending_action": pending_action,
        "rank": None,
        "gate_blocked": gate_blocked,
        "explanation": explanation,
        "state_transitions": [
            f"Latest after-close evaluation produced action: {action}.",
            f"Current state is interpreted as {current_state}.",
        ],
        "risk_notes": [
            "Signals are decision-support outputs for the next market open, not immediate execution orders.",
        ],
    }


def _build_positions(signals: list[dict[str, Any]], previous_positions: Optional[list[dict[str, Any]]] = None) -> list[dict[str, Any]]:
    previous_by_ticker = {
        item["ticker"].upper(): item for item in (previous_positions or []) if item.get("ticker")
    }
    positions: list[dict[str, Any]] = []
    for signal in signals:
        if signal["current_state"] == "Long" or signal["pending_action"]:
            previous = previous_by_ticker.get(signal["ticker"].upper(), {})
            current_close = signal["last_close"]

            entry_display_price = previous.get("entry_display_price")
            if entry_display_price is None:
                entry_display_price = previous.get("entry_price")

            entry_price = previous.get("entry_price")
            entry_date = previous.get("entry_date")

            if entry_display_price is None:
                # Display-only fallback: preserve the first observed reference close for the open trade.
                entry_display_price = current_close
            if entry_price is None:
                entry_price = entry_display_price
            if entry_date is None and (signal["current_state"] == "Long" or signal["pending_action"]):
                entry_date = signal["signal_date"]

            unrealized_pnl_pct = 0.0
            if entry_display_price:
                unrealized_pnl_pct = ((current_close / entry_display_price) - 1.0) * 100.0

            positions.append(
                {
                    "ticker": signal["ticker"],
                    "state": signal["pending_action"] or signal["current_state"],
                    "entry_date": entry_date,
                    "entry_price": entry_price,
                    "entry_display_price": entry_display_price,
                    "current_close": current_close,
                    "unrealized_pnl": unrealized_pnl_pct,
                    "unrealized_pnl_pct": unrealized_pnl_pct,
                    "probability": signal["probability"],
                    "entry_band": signal["entry_band"],
                    "exit_band": signal["exit_band"],
                    "latest_message": signal["latest_message"],
                    "pending_action": signal["pending_action"],
                }
            )
    return positions


def _build_backtests(output_text: str, fallback_tickers: list[str]) -> dict[str, Any]:
    summary = {
        "total_start_value": 0.0,
        "total_end_value": 0.0,
        "total_pnl": 0.0,
        "total_return_pct": 0.0,
        "tickers_processed": len(fallback_tickers),
        "beat_baseline_count": 0,
    }
    details: dict[str, Any] = {}

    for raw_line in output_text.splitlines():
        line = raw_line.strip()
        metrics_match = BACKTEST_LINE_RE.match(line)
        if metrics_match:
            ticker = metrics_match.group("ticker")
            total_return = float(metrics_match.group("ret"))
            vol = float(metrics_match.group("vol"))
            mdd = float(metrics_match.group("mdd"))
            baseline_return = float(metrics_match.group("baseline"))
            details[ticker] = {
                "ticker": ticker,
                "period_label": "Notebook test window",
                "metrics": {
                    "total_return_pct": total_return,
                    "max_drawdown_pct": mdd,
                    "volatility_pct": vol,
                    "total_trades": 0,
                    "win_rate_pct": 0.0,
                    "profit_factor": 0.0,
                    "expectancy": 0.0,
                },
                "baseline_metrics": {
                    "total_return_pct": baseline_return,
                    "max_drawdown_pct": 0.0,
                    "volatility_pct": 0.0,
                    "total_trades": 0,
                    "win_rate_pct": 0.0,
                    "profit_factor": 0.0,
                    "expectancy": 0.0,
                },
                "equity_curve": [
                    {"date": "start", "strategy": 100.0, "baseline": 100.0},
                    {"date": "end", "strategy": 100.0 + total_return, "baseline": 100.0 + baseline_return},
                ],
            }
            continue

        if line.startswith("Tickers processed:"):
            if "| Beat baseline on " in line:
                left, right = line.split("| Beat baseline on ")
                summary["tickers_processed"] = int(left.split(":")[1].strip())
                summary["beat_baseline_count"] = int(right.strip())
            continue

        if line.startswith("Total Start Value:"):
            summary["total_start_value"] = float(line.split("$", 1)[1].replace(",", ""))
            continue

        if line.startswith("Total End Value:"):
            summary["total_end_value"] = float(line.split("$", 1)[1].replace(",", ""))
            continue

        if line.startswith("Total PnL:"):
            pnl_match = re.search(r"\$([\d,]+\.\d+).*?\(([-\d.]+)%\)", line)
            if pnl_match:
                summary["total_pnl"] = float(pnl_match.group(1).replace(",", ""))
                summary["total_return_pct"] = float(pnl_match.group(2))

    for ticker in fallback_tickers:
        details.setdefault(
            ticker,
            {
                "ticker": ticker,
                "period_label": "Notebook test window",
                "metrics": {
                    "total_return_pct": 0.0,
                    "max_drawdown_pct": 0.0,
                    "volatility_pct": 0.0,
                    "total_trades": 0,
                    "win_rate_pct": 0.0,
                    "profit_factor": 0.0,
                    "expectancy": 0.0,
                },
                "baseline_metrics": {
                    "total_return_pct": 0.0,
                    "max_drawdown_pct": 0.0,
                    "volatility_pct": 0.0,
                    "total_trades": 0,
                    "win_rate_pct": 0.0,
                    "profit_factor": 0.0,
                    "expectancy": 0.0,
                },
                "equity_curve": [
                    {"date": "start", "strategy": 100.0, "baseline": 100.0},
                    {"date": "end", "strategy": 100.0, "baseline": 100.0},
                ],
            },
        )

    return {"summary": summary, "details": details}


def _extract_tickers_from_source(source: str) -> list[str]:
    start = source.rfind("tickers = [")
    if start == -1:
        return []
    end = source.find("]", start)
    if end == -1:
        return []
    block = source[start:end]
    return re.findall(r'"([A-Z0-9.\-]+)"', block)


def _parse_state_from_output(output_text: str, source: str) -> Optional[dict[str, Any]]:
    signals = []
    in_signal_section = False

    for raw_line in output_text.splitlines():
        line = raw_line.strip()
        if line.startswith("=== After-Close Signals"):
            in_signal_section = True
            continue
        if in_signal_section and not line:
            continue
        if in_signal_section and line.startswith("[MAIN] Cross-sectional run complete."):
            break
        if in_signal_section:
            parsed = _parse_signal_line(line)
            if parsed:
                signals.append(parsed)

    if not signals:
        return None

    tickers = _extract_tickers_from_source(source)
    backtests = _build_backtests(output_text, fallback_tickers=tickers or [item["ticker"] for item in signals])
    previous_state = ensure_runtime_state()
    previous_positions = previous_state.get("positions", [])
    state = previous_state
    state["signals"] = signals
    state["positions"] = _build_positions(signals, previous_positions=previous_positions)
    state["backtests"] = backtests
    state["status"]["status"] = "succeeded"
    state["status"]["latest_run_time"] = _utc_now().isoformat()
    state["status"]["latest_signal_date"] = signals[0]["signal_date"]
    state["status"]["tickers_processed"] = len(signals)
    state["status"]["last_error"] = None
    state["status"]["last_run_mode"] = "universe"
    write_runtime_state(state)
    return state


def _load_notebook() -> Optional[dict[str, Any]]:
    notebook_path = _notebook_path()
    if not notebook_path.exists():
        return None
    return json.loads(notebook_path.read_text(encoding="utf-8"))


def _find_active_notebook_cell(notebook: dict[str, Any]) -> tuple[Optional[int], Optional[dict[str, Any]]]:
    for index, cell in enumerate(notebook.get("cells", [])):
        if cell.get("cell_type") != "code":
            continue
        source = "".join(cell.get("source", []))
        executable_lines = [
            line for line in source.splitlines() if line.strip() and not line.lstrip().startswith("#")
        ]
        if '"MSFT", "NVDA", "META"' in source and "if __name__ == \"__main__\":" in source and executable_lines:
            return index, cell
    return None, None


def _output_text_from_cell(cell: dict[str, Any]) -> str:
    chunks: list[str] = []
    for output in cell.get("outputs", []):
        if "text" in output:
            chunks.append("".join(output["text"]))
        elif "data" in output and "text/plain" in output["data"]:
            chunks.append("".join(output["data"]["text/plain"]))
    return "\n".join(chunks)


def _sync_state_from_notebook() -> Optional[dict[str, Any]]:
    notebook = _load_notebook()
    if not notebook:
        return None
    _, cell = _find_active_notebook_cell(notebook)
    if not cell:
        return None
    source = "".join(cell.get("source", []))
    output_text = _output_text_from_cell(cell)
    if not output_text.strip():
        return None
    return _parse_state_from_output(output_text, source)


def _replace_tickers_for_single_run(source: str, ticker: str) -> str:
    marker = "tickers = ["
    start = source.rfind(marker)
    if start == -1:
        return source
    end = source.find("]", start)
    if end == -1:
        return source
    replacement = f'tickers = [\n        "{ticker.upper()}",\n    ]'
    return f"{source[:start]}{replacement}{source[end + 1:]}"


def _write_notebook_output(stdout: str, stderr: str, source: str) -> None:
    notebook = _load_notebook()
    if not notebook:
        return
    index, cell = _find_active_notebook_cell(notebook)
    if cell is None or index is None:
        return
    cell["outputs"] = [{"name": "stdout", "output_type": "stream", "text": stdout.splitlines(True)}]
    if stderr.strip():
        cell["outputs"].append({"name": "stderr", "output_type": "stream", "text": stderr.splitlines(True)})
    cell["execution_count"] = int(cell.get("execution_count") or 1)
    notebook["cells"][index] = cell
    _notebook_path().write_text(json.dumps(notebook, indent=1), encoding="utf-8")


def _run_notebook_source(source: str) -> dict[str, Any]:
    python_path = _engine_python_path()
    with tempfile.NamedTemporaryFile("w", suffix=".py", delete=False, encoding="utf-8") as handle:
        handle.write(source)
        temp_path = Path(handle.name)

    try:
        result = subprocess.run(
            [str(python_path), str(temp_path)],
            cwd=str(_project_root()),
            capture_output=True,
            text=True,
            timeout=60 * 60,
        )
    finally:
        temp_path.unlink(missing_ok=True)

    if result.returncode != 0:
        raise RuntimeError(result.stderr.strip() or "Notebook execution failed.")

    _write_notebook_output(result.stdout, result.stderr, source)
    parsed = _parse_state_from_output(result.stdout, source)
    if not parsed:
        raise RuntimeError("Notebook run completed but no signals could be parsed from stdout.")
    return parsed


def _bump_run_metadata(
    state: dict[str, Any],
    run_mode: str,
    tickers_processed: Optional[int] = None,
    error: Optional[str] = None,
) -> dict[str, Any]:
    state["status"]["latest_run_time"] = _utc_now().isoformat()
    state["status"]["last_run_mode"] = run_mode
    if tickers_processed is not None:
        state["status"]["tickers_processed"] = tickers_processed
    state["status"]["latest_signal_date"] = state["signals"][0]["signal_date"] if state.get("signals") else None
    state["status"]["last_error"] = error
    state["status"]["status"] = "failed" if error else "succeeded"
    return state


def _apply_real_result_to_state(result: Any, run_mode: str, ticker: Optional[str] = None) -> dict[str, Any]:
    state = read_runtime_state()

    # TODO: Replace this merge logic with direct serialization of your real engine outputs.
    # The expectation is that your imported engine functions return dictionaries shaped similarly
    # to the API schemas, or that you map them here once your engine module is connected.
    if isinstance(result, dict):
        if "signals" in result:
            state["signals"] = result["signals"]
        if "positions" in result:
            state["positions"] = result["positions"]
        if "backtests" in result:
            state["backtests"] = result["backtests"]
        if "settings" in result:
            state["settings"] = result["settings"]
        if "status" in result:
            state["status"].update(result["status"])

    processed = len(state.get("signals", []))
    _bump_run_metadata(state, run_mode=run_mode, tickers_processed=processed)
    write_runtime_state(state)
    return state


def run_universe_pipeline_job() -> dict[str, Any]:
    ensure_runtime_state()
    settings = get_settings()
    real_fn = _resolve_function(settings.trading_universe_function)
    if real_fn:
        result = real_fn()
        return _apply_real_result_to_state(result, run_mode="universe")

    notebook = _load_notebook()
    index, cell = _find_active_notebook_cell(notebook or {})
    if cell:
        source = "".join(cell.get("source", []))
        state = _run_notebook_source(source)
        _bump_run_metadata(state, run_mode="universe", tickers_processed=len(state.get("signals", [])))
        write_runtime_state(state)
        return state

    state = read_runtime_state()
    _bump_run_metadata(state, run_mode="universe", tickers_processed=len(state.get("signals", [])))
    write_runtime_state(state)
    return state


def run_ticker_pipeline_job(ticker: str) -> dict[str, Any]:
    ensure_runtime_state()
    settings = get_settings()
    real_fn = _resolve_function(settings.trading_ticker_function)
    if real_fn:
        result = real_fn(ticker)
        return _apply_real_result_to_state(result, run_mode="ticker", ticker=ticker)

    notebook = _load_notebook()
    index, cell = _find_active_notebook_cell(notebook or {})
    if cell:
        source = "".join(cell.get("source", []))
        source = _replace_tickers_for_single_run(source, ticker)
        state = _run_notebook_source(source)
        _bump_run_metadata(state, run_mode="ticker", tickers_processed=len(state.get("signals", [])))
        write_runtime_state(state)
        return state

    state = read_runtime_state()
    _bump_run_metadata(state, run_mode="ticker", tickers_processed=1)
    write_runtime_state(state)
    return state


def get_pipeline_status() -> dict[str, Any]:
    state = _sync_state_from_notebook() or ensure_runtime_state()
    return state["status"]


def get_latest_signal_snapshot() -> list[dict[str, Any]]:
    settings = get_settings()
    real_fn = _resolve_function(settings.trading_snapshot_function)
    if real_fn:
        result = real_fn()
        if result is not None:
            return result
    state = _sync_state_from_notebook() or ensure_runtime_state()
    return state["signals"]


def get_ticker_signal_detail(ticker: str) -> dict[str, Any]:
    settings = get_settings()
    real_fn = _resolve_function(settings.trading_detail_function)
    if real_fn:
        result = real_fn(ticker)
        if result is not None:
            return result

    state = _sync_state_from_notebook() or ensure_runtime_state()
    for signal in state["signals"]:
        if signal["ticker"].upper() == ticker.upper():
            return signal
    raise KeyError(f"Ticker {ticker} not found")


def get_positions_snapshot() -> list[dict[str, Any]]:
    settings = get_settings()
    real_fn = _resolve_function(settings.trading_positions_function)
    if real_fn:
        result = real_fn()
        if result is not None:
            return result
    state = _sync_state_from_notebook() or ensure_runtime_state()
    return state["positions"]


def get_backtest_summary() -> dict[str, Any]:
    settings = get_settings()
    real_fn = _resolve_function(settings.trading_backtest_summary_function)
    if real_fn:
        result = real_fn()
        if result is not None:
            return result
    state = _sync_state_from_notebook() or ensure_runtime_state()
    return state["backtests"]["summary"]


def get_ticker_backtest(ticker: str) -> dict[str, Any]:
    settings = get_settings()
    real_fn = _resolve_function(settings.trading_backtest_ticker_function)
    if real_fn:
        result = real_fn(ticker)
        if result is not None:
            return result

    state = _sync_state_from_notebook() or ensure_runtime_state()
    detail = state["backtests"]["details"].get(ticker.upper())
    if detail:
        return detail
    first = next(iter(state["backtests"]["details"].values()))
    return {**first, "ticker": ticker.upper()}


def get_settings_snapshot() -> dict[str, Any]:
    state = _sync_state_from_notebook() or ensure_runtime_state()
    return state["settings"]
