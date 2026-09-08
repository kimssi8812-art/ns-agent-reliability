from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Iterable


@dataclass(frozen=True)
class FlowEvent:
    event_id: str
    sequence: int
    event_type: str
    observed_at: str
    source: str
    authority: str
    project_id: str
    state_before: str | None
    state_after: str | None
    goal_id: str | None = None
    checkpoint_id: str | None = None
    task_id: str | None = None
    executor_run_id: str | None = None
    provider: str | None = None
    session_scope: str | None = None
    session_id: str | None = None
    session_generation: int | None = None
    runtime_version: str | None = None
    model_id: str | None = None
    baseline_digest: str | None = None
    delta_digest: str | None = None
    failure_class: str | None = None
    retry_index: int | None = None
    evidence_refs: tuple[str, ...] = ()
    artifact_refs: tuple[str, ...] = ()
    correlation_id: str | None = None
    causation_id: str | None = None
    metadata: dict[str, Any] = field(default_factory=dict)


class EventLedger:
    def __init__(self) -> None:
        self._events: list[FlowEvent] = []

    def append(self, event: FlowEvent) -> None:
        if self._events and event.sequence <= self._events[-1].sequence:
            raise ValueError("FLOW_EVENT_SEQUENCE_NOT_MONOTONIC")
        if any(existing.event_id == event.event_id for existing in self._events):
            raise ValueError("DUPLICATE_FLOW_EVENT_ID")
        if event.causation_id and not any(existing.event_id == event.causation_id for existing in self._events):
            raise ValueError("UNKNOWN_CAUSATION_EVENT")
        self._events.append(event)

    def after(self, cursor: int) -> tuple[FlowEvent, ...]:
        return tuple(event for event in self._events if event.sequence > cursor)

    def all(self) -> tuple[FlowEvent, ...]:
        return tuple(self._events)


@dataclass(frozen=True)
class MachineFlowboardSnapshot:
    snapshot_id: str
    observed_at: str
    cursor: int
    goals: tuple[dict[str, Any], ...]
    workers: tuple[dict[str, Any], ...]
    sessions: tuple[dict[str, Any], ...]
    executor_runs: tuple[dict[str, Any], ...]
    events: tuple[FlowEvent, ...]
    resources: dict[str, Any] = field(default_factory=dict)
    dna_objects: tuple[dict[str, Any], ...] = ()
    evidence: tuple[dict[str, Any], ...] = ()
    gates: tuple[dict[str, Any], ...] = ()
    system_health: dict[str, Any] = field(default_factory=dict)


@dataclass(frozen=True)
class HumanCockpitSnapshot:
    snapshot_id: str
    observed_at: str
    roadmap: dict[str, Any]
    progress: dict[str, Any]
    active_work: tuple[dict[str, Any], ...]
    blockers: tuple[dict[str, Any], ...]
    approvals: tuple[dict[str, Any], ...]
    resource_summary: dict[str, Any]
    dna_summary: dict[str, Any]
    system_health: dict[str, Any]
    next_critical_action: dict[str, Any] | None = None


def project_human(machine: MachineFlowboardSnapshot) -> HumanCockpitSnapshot:
    blocked = tuple(goal for goal in machine.goals if goal.get("state") == "BLOCKED")
    active_sessions = [
        {
            "actor": session.get("provider"),
            "scope": session.get("session_scope"),
            "goal_id": session.get("goal_id"),
            "checkpoint_id": session.get("checkpoint_id"),
            "model_id": session.get("model_id"),
            "state": session.get("state"),
        }
        for session in machine.sessions
        if session.get("state") not in {"CLOSED", "IDLE"}
    ]
    active_executor = [
        {
            "actor": "deterministic-executor",
            "scope": run.get("command_class"),
            "goal_id": run.get("goal_id"),
            "checkpoint_id": run.get("checkpoint_id"),
            "model_id": None,
            "state": run.get("state"),
        }
        for run in machine.executor_runs
        if run.get("state") not in {"DONE", "FAILED", "CANCELLED"}
    ]
    return HumanCockpitSnapshot(
        snapshot_id=machine.snapshot_id,
        observed_at=machine.observed_at,
        roadmap={"goal_count": len(machine.goals)},
        progress={},
        active_work=tuple(active_sessions + active_executor),
        blockers=blocked,
        approvals=tuple(machine.gates),
        resource_summary=machine.resources,
        dna_summary={"active_objects": len(machine.dna_objects)},
        system_health=machine.system_health,
        next_critical_action=None,
    )


def validate_causality(events: Iterable[FlowEvent]) -> None:
    seen: set[str] = set()
    last_sequence = -1
    for event in events:
        if event.event_id in seen:
            raise ValueError("DUPLICATE_FLOW_EVENT_ID")
        if event.sequence <= last_sequence:
            raise ValueError("FLOW_EVENT_SEQUENCE_NOT_MONOTONIC")
        if event.causation_id and event.causation_id not in seen:
            raise ValueError("UNKNOWN_CAUSATION_EVENT")
        seen.add(event.event_id)
        last_sequence = event.sequence
