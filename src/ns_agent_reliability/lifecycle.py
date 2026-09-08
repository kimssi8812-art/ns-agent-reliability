from __future__ import annotations

from dataclasses import dataclass
from enum import Enum


class LifecycleState(str, Enum):
    REQUESTED = "REQUESTED"
    ASSIGNED = "ASSIGNED"
    RUNNING = "RUNNING"
    RESULT_RECEIVED = "RESULT_RECEIVED"
    RESULT_VERIFIED = "RESULT_VERIFIED"
    ACKNOWLEDGED = "ACKNOWLEDGED"
    CONSUMED = "CONSUMED"
    BLOCKED = "BLOCKED"
    FAILED = "FAILED"


_ALLOWED: dict[LifecycleState, set[LifecycleState]] = {
    LifecycleState.REQUESTED: {LifecycleState.ASSIGNED, LifecycleState.BLOCKED, LifecycleState.FAILED},
    LifecycleState.ASSIGNED: {LifecycleState.RUNNING, LifecycleState.BLOCKED, LifecycleState.FAILED},
    LifecycleState.RUNNING: {LifecycleState.RESULT_RECEIVED, LifecycleState.BLOCKED, LifecycleState.FAILED},
    LifecycleState.RESULT_RECEIVED: {LifecycleState.RESULT_VERIFIED, LifecycleState.FAILED},
    LifecycleState.RESULT_VERIFIED: {LifecycleState.ACKNOWLEDGED},
    LifecycleState.ACKNOWLEDGED: {LifecycleState.CONSUMED},
    LifecycleState.CONSUMED: set(),
    LifecycleState.BLOCKED: {LifecycleState.ASSIGNED, LifecycleState.FAILED},
    LifecycleState.FAILED: set(),
}


@dataclass(frozen=True)
class LifecycleEvent:
    goal_id: str
    checkpoint_id: str
    previous: LifecycleState
    current: LifecycleState
    evidence_digest: str | None = None
    failure_class: str | None = None


def transition(
    goal_id: str,
    checkpoint_id: str,
    previous: LifecycleState,
    current: LifecycleState,
    *,
    evidence_digest: str | None = None,
    failure_class: str | None = None,
) -> LifecycleEvent:
    if current not in _ALLOWED[previous]:
        raise ValueError(f"INVALID_LIFECYCLE_TRANSITION:{previous}->{current}")
    if current == LifecycleState.RESULT_VERIFIED and not evidence_digest:
        raise ValueError("VERIFIED_RESULT_REQUIRES_EVIDENCE_DIGEST")
    return LifecycleEvent(goal_id, checkpoint_id, previous, current, evidence_digest, failure_class)
