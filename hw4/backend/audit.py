"""Summarized append-only JSON audit trail for agent activity."""
from __future__ import annotations
import json
import threading
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

AUDIT_PATH = Path(__file__).resolve().parents[1] / "output" / "audit_trail.json"
_LOCK = threading.Lock()
_MAX_TEXT = 240

def _short(value: Any) -> Any:
    if isinstance(value, str):
        return value if len(value) <= _MAX_TEXT else value[:_MAX_TEXT] + "…"
    if isinstance(value, (int, float, bool)) or value is None:
        return value
    if isinstance(value, dict):
        return {str(k): _short(v) for k, v in list(value.items())[:20]}
    if isinstance(value, (list, tuple)):
        return [_short(v) for v in list(value)[:20]]
    return _short(str(value))

def record(*, event: str, tool_name: str, arguments: Any = None, result: Any = None, stop_reason: str | None = None) -> None:
    entry = {"time": datetime.now(timezone.utc).isoformat(), "event": event, "tool_name": tool_name, "arguments": _short(arguments), "result": _short(result)}
    if stop_reason is not None:
        entry["stop_reason"] = _short(stop_reason)
    try:
        with _LOCK:
            AUDIT_PATH.parent.mkdir(parents=True, exist_ok=True)
            try:
                entries = json.loads(AUDIT_PATH.read_text(encoding="utf-8"))
                if not isinstance(entries, list): entries = []
            except (FileNotFoundError, json.JSONDecodeError):
                entries = []
            entries.append(entry)
            AUDIT_PATH.write_text(json.dumps(entries, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    except OSError:
        pass
