from __future__ import annotations

from dataclasses import asdict, dataclass
from datetime import datetime, timezone
from typing import Any


@dataclass(frozen=True)
class TelemetryEvent:
    event_type: str
    goal_id: str
    provider: str | None = None
    session_id: str | None = None
    checkpoint_id: str | None = None
    context_units: int | None = None
    memory_bytes: int | None = None
    cpu_percent: float | None = None
    outcome: str | None = None
    failure_class: str | None = None
    evidence_digest: str | None = None


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")


def serialize_event(event: TelemetryEvent, extra: dict[str, Any] | None = None) -> dict[str, Any]:
    payload = asdict(event)
    payload["observed_at"] = utc_now()
    payload["authority"] = "NON_SSOT_TELEMETRY"
    if extra:
        payload["extra"] = extra
    return payload
