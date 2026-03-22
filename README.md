# Trading Advisor Bot

Full-stack prototype for an after-close trading decision-support dashboard. The app is built as a real React + FastAPI stack and is structured so your existing Python trading engine can be plugged into a single backend adapter layer.

## Folder Tree

```text
backend/
  app/
    adapters/
      file_adapter.py
      pipeline_adapter.py
    api/
      routes_backtests.py
      routes_dashboard.py
      routes_pipeline.py
      routes_positions.py
      routes_settings.py
      routes_signals.py
    core/
      config.py
    mock_data/
      sample_data.py
    models/
      schemas.py
    services/
      backtest_service.py
      dashboard_service.py
      explanation_service.py
      ledger_service.py
      pipeline_service.py
      settings_service.py
      signal_service.py
    main.py
  data/
  requirements.txt
frontend/
  src/
    api/
      client.ts
      index.ts
    app/
      App.tsx
      AppShell.tsx
    components/
      ui/
        Button.tsx
        Card.tsx
      BaselineComparisonChart.tsx
      DriverImpactList.tsx
      EmptyState.tsx
      EquityCurveChart.tsx
      ExplanationPanel.tsx
      GateBadge.tsx
      LoadingState.tsx
      MetricCard.tsx
      PageHeader.tsx
      PipelineStatusCard.tsx
      PositionsTable.tsx
      ProbabilityBand.tsx
      RunControls.tsx
      SignalBadge.tsx
      SignalsTable.tsx
      SummaryCard.tsx
    hooks/
      useBacktests.ts
      useDashboard.ts
      usePipelineActions.ts
      usePositions.ts
      useSettings.ts
      useSignals.ts
    lib/
      utils.ts
    pages/
      BacktestsPage.tsx
      DashboardPage.tsx
      PositionsPage.tsx
      SettingsPage.tsx
      SignalsLogPage.tsx
      TickerDetailPage.tsx
    types/
      models.ts
    index.css
    main.tsx
  index.html
  package.json
  postcss.config.js
  tailwind.config.ts
  tsconfig.app.json
  tsconfig.json
  tsconfig.node.json
  vite.config.ts
README.md
```

## What Works

- FastAPI backend with real endpoints:
  - `POST /api/pipeline/run-universe`
  - `POST /api/pipeline/run-ticker/{ticker}`
  - `GET /api/pipeline/status`
  - `GET /api/dashboard`
  - `GET /api/signals`
  - `GET /api/signals/{ticker}`
  - `GET /api/positions`
  - `GET /api/backtests/summary`
  - `GET /api/backtests/{ticker}`
  - `GET /api/settings`
- React dashboard connected to those endpoints with React Query.
- File-backed fallback state under `backend/data/runtime_state.json` so the app is usable immediately.
- Integration-ready adapter boundary in `backend/app/adapters/pipeline_adapter.py`.

## Run Locally

### Backend

```bash
cd backend
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000
```

### Frontend

```bash
cd frontend
npm install
npm run dev
```

Open `http://localhost:5173`.

## Trading Engine Integration

The key integration file is:

- `backend/app/adapters/pipeline_adapter.py`

That adapter already exposes the functions your app needs:

- `run_universe_pipeline_job()`
- `run_ticker_pipeline_job(ticker: str)`
- `get_latest_signal_snapshot()`
- `get_ticker_signal_detail(ticker: str)`
- `get_positions_snapshot()`
- `get_backtest_summary()`
- `get_ticker_backtest(ticker: str)`

### How to connect your real engine

1. Make your trading engine importable as a Python module.
2. Set `TRADING_APP_TRADING_ENGINE_MODULE` to that module path.
3. If your function names differ, set the matching env vars in `backend/app/core/config.py` or add them to `.env`.

### Example integration shape

Inside `pipeline_adapter.py`, replace or extend the `TODO` section so your real engine returns dictionaries shaped like the API schemas.

Conceptually:

```python
from your_engine_module import run_universe_pipeline, run_ticker_pipeline

def run_universe_pipeline_job():
    result = run_universe_pipeline()
    return _apply_real_result_to_state(result, run_mode="universe")
```

If your engine currently returns custom classes or plain prints, map them in the adapter once and keep the rest of the backend unchanged.

## Notes

- The app is a decision-support system, not an execution broker.
- The frontend shows explanations, gate results, probability bands, positions, and backtests in one place.
- The fallback state is only there to make the full stack runnable immediately. The architecture is not locked to fake demo routes.
