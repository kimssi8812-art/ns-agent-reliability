from __future__ import annotations

from typing import Any, Protocol

from .contracts import EvidenceRef, GoalDefinition, SessionRecord


class EvidencePort(Protocol):
    def persist(self, payload: bytes, summary: str) -> EvidenceRef: ...
    def verify(self, evidence: EvidenceRef) -> bool: ...


class GoalStorePort(Protocol):
    def get_goal(self, goal_id: str) -> GoalDefinition | None: ...
    def put_goal(self, goal: GoalDefinition) -> None: ...


class SessionStorePort(Protocol):
    def get_session(self, goal_id: str) -> SessionRecord | None: ...
    def put_session(self, session: SessionRecord) -> None: ...


class TaskboardPort(Protocol):
    def acknowledge(self, goal_id: str, checkpoint_id: str, evidence: EvidenceRef) -> None: ...
    def consume(self, goal_id: str, checkpoint_id: str) -> None: ...


class GatePort(Protocol):
    def prepare(self, change: dict[str, Any]) -> dict[str, Any]: ...
    def verify_approval(self, approval_ref: str) -> bool: ...


class RuntimeInventoryPort(Protocol):
    def discover_provider_profiles(self, provider: str) -> list[dict[str, Any]]: ...


class MirrorPort(Protocol):
    """Optional human-facing non-SSOT mirror."""

    def publish_goal_view(self, payload: dict[str, Any]) -> None: ...
