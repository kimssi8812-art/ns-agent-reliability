from __future__ import annotations

from dataclasses import dataclass

from .contracts import WorkerState


@dataclass(frozen=True)
class HealthSignal:
    source: str
    liveness: str = "UNKNOWN"
    readiness: str = "UNKNOWN"
    dispatch_allowed: bool | None = None
    failure_class: str | None = None
    observed_at: str = ""


@dataclass(frozen=True)
class NormalizedHealth:
    worker_state: WorkerState
    dispatch_allowed: bool
    failure_classes: tuple[str, ...]
    source_conflict: bool
    reason: str


def normalize_health(signals: list[HealthSignal]) -> NormalizedHealth:
    """Normalize independent health sources without equating liveness with readiness."""
    if not signals:
        return NormalizedHealth(WorkerState.UNKNOWN, False, (), False, "NO_HEALTH_SIGNAL")

    failures = tuple(sorted({s.failure_class for s in signals if s.failure_class}))
    hard_deny = [s for s in signals if s.dispatch_allowed is False]
    authoritative_allow = [s for s in signals if s.dispatch_allowed is True]
    liveness = {s.liveness.upper() for s in signals if s.liveness}
    readiness = {s.readiness.upper() for s in signals if s.readiness}

    conflict = bool(hard_deny and authoritative_allow)
    if len({v for v in liveness if v not in {"UNKNOWN", "N/A"}}) > 1:
        conflict = True
    if len({v for v in readiness if v not in {"UNKNOWN", "N/A"}}) > 1:
        conflict = True

    if hard_deny:
        state = WorkerState.DEAD if "DEAD" in liveness else WorkerState.DEGRADED
        return NormalizedHealth(state, False, failures, conflict, "DISPATCH_DENIED_BY_SOURCE")

    # Liveness alone is never an allow signal.
    if authoritative_allow:
        state = WorkerState.READY if "READY" in readiness else WorkerState.BUSY
        return NormalizedHealth(state, True, failures, conflict, "AUTHORITATIVE_DISPATCH_ALLOW")

    if "DEAD" in liveness:
        return NormalizedHealth(WorkerState.DEAD, False, failures, conflict, "LIVENESS_DEAD")

    if "READY" in readiness:
        # Ready is useful state but still not dispatch authority unless the deployment
        # explicitly maps that readiness source to dispatch_allowed=True.
        return NormalizedHealth(WorkerState.READY, False, failures, conflict, "READY_BUT_DISPATCH_NOT_AUTHORIZED")

    if "ALIVE" in liveness:
        return NormalizedHealth(WorkerState.BUSY, False, failures, conflict, "ALIVE_BUT_READINESS_NOT_PROVEN")

    return NormalizedHealth(WorkerState.UNKNOWN, False, failures, conflict, "DISPATCH_NOT_PROVEN")
