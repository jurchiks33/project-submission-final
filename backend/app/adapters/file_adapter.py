from __future__ import annotations

import json
from copy import deepcopy
from pathlib import Path
from typing import Any

from app.core.config import get_settings
from app.mock_data.sample_data import build_initial_state


def ensure_runtime_state() -> dict[str, Any]:
    settings = get_settings()
    settings.data_dir.mkdir(parents=True, exist_ok=True)
    state_path = settings.runtime_state_path
    if not state_path.exists():
        state = build_initial_state()
        state_path.write_text(json.dumps(state, indent=2), encoding="utf-8")
        return deepcopy(state)
    return read_runtime_state()


def read_runtime_state() -> dict[str, Any]:
    settings = get_settings()
    state_path: Path = settings.runtime_state_path
    if not state_path.exists():
        return ensure_runtime_state()
    return json.loads(state_path.read_text(encoding="utf-8"))


def write_runtime_state(state: dict[str, Any]) -> dict[str, Any]:
    settings = get_settings()
    settings.data_dir.mkdir(parents=True, exist_ok=True)
    settings.runtime_state_path.write_text(json.dumps(state, indent=2), encoding="utf-8")
    return state
