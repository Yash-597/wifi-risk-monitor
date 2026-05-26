from __future__ import annotations
import json
from pathlib import Path
from typing import Any
from core.models import AuditEvent
from core.paths import AUDIT_LOG_FILE


def write_event(event: AuditEvent, path: Path = AUDIT_LOG_FILE) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a", encoding="utf-8") as file:
        file.write(json.dumps(event.to_dict()) + "\n")


def read_events(path: Path = AUDIT_LOG_FILE, limit: int = 200) -> list[dict[str, Any]]:
    if not path.exists():
        return []

    events: list[dict[str, Any]] = []
    with path.open("r", encoding="utf-8") as file:
        for line in file:
            try:
                events.append(json.loads(line))
            except json.JSONDecodeError:
                continue

    return events[-limit:]


def clear_events(path: Path = AUDIT_LOG_FILE) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("", encoding="utf-8")
