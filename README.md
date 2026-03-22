````markdown
# Trading Advisor Bot

Trading Advisor Bot is a full-stack after-close trading decision-support application developed as part of the project submission.

The system combines:
- a Python-based trading pipeline used to generate signals, bands, state transitions, and backtest outputs
- a FastAPI backend that serves the application data through API endpoints
- a React frontend that displays the dashboard, signals, positions, backtests, and settings views

The application is designed as a decision-support system. It is not a live broker execution platform.

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
artifacts/
  bands/
README.md
SCANNING USE THIS ONE v3.ipynb
````

## Project Overview

This repository contains the web application and project files used for the Trading Advisor Bot submission.

The main trading logic is contained in:

* `SCANNING USE THIS ONE v3.ipynb`

The notebook contains the trading pipeline used in the project, including:

* feature generation
* time-based data splits
* model training
* calibration
* band-based signal generation
* entry-only gating
* backtesting

The web application is used to display the latest available outputs from the project in a more usable interface.

## What Works

The implemented system includes:

* FastAPI backend with working endpoints:

  * `POST /api/pipeline/run-universe`
  * `POST /api/pipeline/run-ticker/{ticker}`
  * `GET /api/pipeline/status`
  * `GET /api/dashboard`
  * `GET /api/signals`
  * `GET /api/signals/{ticker}`
  * `GET /api/positions`
  * `GET /api/backtests/summary`
  * `GET /api/backtests/{ticker}`
  * `GET /api/settings`
* React frontend connected to the backend endpoints using React Query
* dashboard view for latest pipeline summary and signal table
* signal log view for chronological signal history
* ticker detail view for decision explanation and gate context
* positions view for ledger and active position tracking
* backtests view for strategy metrics and comparison charts
* settings view for runtime parameter display
* saved band artifacts under `artifacts/bands/`
* backend runtime state under `backend/data/runtime_state.json` used for serving the latest available outputs to the frontend

## How the Project Is Used

The project is run locally.

To use the web application:

1. start the backend
2. start the frontend in a separate terminal
3. open the local frontend URL in the browser
4. view the latest available outputs through the dashboard and supporting pages

The interface is intended to present the results of the project pipeline in a structured way, rather than requiring the user to read notebook output directly.

## Run Locally

### Backend

```bash
cd backend
python -m venv .venv
```

### Activate environment

#### Windows

```bash
.venv\Scripts\activate
```

#### Mac / Linux

```bash
source .venv/bin/activate
```

### Install backend dependencies

```bash
pip install -r requirements.txt
```

### Start backend

```bash
uvicorn app.main:app --reload --port 8000
```

### Frontend

```bash
cd frontend
npm install
npm run dev
```

Then open:

```text
http://localhost:5173
```

## Main Files

### Notebook

* `SCANNING USE THIS ONE v3.ipynb`
  Main project notebook containing the trading pipeline logic used in the project.

### Backend

* `backend/app/main.py`
  FastAPI entry point.
* `backend/app/adapters/pipeline_adapter.py`
  Adapter layer used by the backend to access pipeline-related outputs and state.
* `backend/app/services/`
  Service layer for dashboard, signals, positions, settings, backtests, and explanations.
* `backend/app/api/`
  API route definitions.

### Frontend

* `frontend/src/pages/`
  Main application pages.
* `frontend/src/components/`
  Reusable UI and chart components.
* `frontend/src/hooks/`
  Data-fetching hooks for API communication.
* `frontend/src/api/`
  Frontend API client layer.

## Notes

* The application is an after-close decision-support system
* It is not a broker execution platform
* The frontend is designed to present signals, explanations, gate results, positions, and backtest summaries in one interface
* The backend serves the latest available application state and output data to the frontend
* The repository is published for academic submission and review purposes

## Rights

All rights reserved. This repository is published for academic grading and review purposes only. Reuse, redistribution, or copying of the code or project materials is not permitted without permission from the author.
