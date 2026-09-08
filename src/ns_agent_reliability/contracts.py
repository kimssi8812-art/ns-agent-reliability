from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Protocol


class WorkerState(str, Enum):
    READY = "READY"
    BUSY = "BUSY"
    DEGRADED = "DEGRADED"
    DEAD = "DEAD"
    UNKNOWN = "UNKNOWN"


class GoalNodeState(str, Enum):
    QUEUED = "QUEUED"
    READY = "READY"
    RUNNING = "RUNNING"
    BLOCKED = "BLOCKED"
    VERIFIED = "VERIFIED"
    FAILED = "FAILED"
    CANCELLED = "CANCELLED"


class SessionState(str, Enum):
    CREATED = "CREATED"
    BASELINE_HYDRATED = "BASELINE_HYDRATED"
    RUNNING = "RUNNING"
    BLOCKED = "BLOCKED"
    ROLLOVER_REQUIRED = "ROLLOVER_REQUIRED"
    CLOSED = "CLOSED"


@dataclass(frozen=True)
class EvidenceRef:
    uri: str
    digest: str
    summary: str = ""


@dataclass
class ContextEnvelope:
    capacity_units: int | None = None
    used_units: int | None = None
    reserve_output_units: int = 0
    reserve_tool_units: int = 0
    reserve_safety_units: int = 0
    baseline_units: int = 0
    delta_units: int = 0

    @property
    def free_units(self) -> int | None:
        if self.capacity_units is None or self.used_units is None:
            return None
        return max(0, self.capacity_units - self.used_units)

    def can_accept(self, projected_next_units: int) -> bool | None:
        free = self.free_units
        if free is None:
            return None
        reserved = self.reserve_output_units + self.reserve_tool_units + self.reserve_safety_units
        return free >= projected_next_units + reserved


@dataclass
class GoalNode:
    node_id: str
    weight: float
    state: GoalNodeState = GoalNodeState.QUEUED
    depends_on: tuple[str, ...] = ()
    acceptance: str = ""
    evidence_required: bool = True
    evidence_verified: bool = False
    owner_worker: str | None = None
    session_id: str | None = None
    blocker: str | None = None


@dataclass
class GoalDefinition:
    goal_id: str
    nodes: list[GoalNode]
    priority: int = 0


@dataclass
class SessionRecord:
    session_id: str
    goal_id: str
    provider: str
    generation: int = 1
    state: SessionState = SessionState.CREATED
    baseline_digest: str | None = None
    baseline_hydrated_count: int = 0
    checkpoint_count: int = 0
    context: ContextEnvelope = field(default_factory=ContextEnvelope)
    execution_profile_id: str | None = None
    last_failure_class: str | None = None


@dataclass
class ResourceSnapshot:
    provider: str
    observed_at: str
    worker_state: WorkerState = WorkerState.UNKNOWN
    dispatch_allowed: bool = False
    quota_state: str = "UNKNOWN"
    active_sessions: int = 0
    warm_sessions: int = 0
    memory_bytes: int | None = None
    cpu_percent: float | None = None
    recent_success: int = 0
    recent_failure: int = 0
    metadata: dict[str, Any] = field(default_factory=dict)


@dataclass(frozen=True)
class CheckpointRequest:
    goal_id: str
    checkpoint_id: str
    instructions: str
    baseline_digest: str | None = None
    delta: dict[str, Any] | None = None


@dataclass(frozen=True)
class CheckpointResult:
    checkpoint_id: str
    state: str
    summary: str
    evidence: tuple[EvidenceRef, ...] = ()
    failure_class: str | None = None


class WorkerManager(Protocol):
    provider: str

    def probe(self) -> ResourceSnapshot: ...
    def create_session(self, goal_id: str, baseline: dict[str, Any]) -> SessionRecord: ...
    def get_session(self, goal_id: str) -> SessionRecord | None: ...
    def run_checkpoint(self, session: SessionRecord, request: CheckpointRequest) -> CheckpointResult: ...
    def compact(self, session: SessionRecord) -> SessionRecord: ...
    def rollover(self, session: SessionRecord, compact_baseline: dict[str, Any]) -> SessionRecord: ...
    def close_session(self, session: SessionRecord, reason: str) -> None: ...
