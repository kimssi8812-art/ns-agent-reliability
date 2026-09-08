from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from .contracts import GoalDefinition, ResourceSnapshot, WorkerManager
from .progress import ProgressSnapshot, calculate_progress, ready_nodes
from .routing import RouteDecision, choose_worker


@dataclass(frozen=True)
class HubSnapshot:
    goal: ProgressSnapshot
    ready_nodes: tuple[str, ...]
    workers: tuple[ResourceSnapshot, ...]


class ControlHub:
    """Reference assembly only. Production ports/storage/Gate remain deployment-specific."""

    def __init__(self, managers: dict[str, WorkerManager]) -> None:
        self.managers = managers

    def observe(self, goal: GoalDefinition) -> HubSnapshot:
        workers = tuple(manager.probe() for manager in self.managers.values())
        return HubSnapshot(
            goal=calculate_progress(goal),
            ready_nodes=tuple(ready_nodes(goal)),
            workers=workers,
        )

    def route(self, capability: str, goal_id: str, workers: list[ResourceSnapshot]) -> RouteDecision:
        warm = {
            provider
            for provider, manager in self.managers.items()
            if manager.get_session(goal_id) is not None
        }
        return choose_worker(capability, workers, warm_goal_providers=warm)

    def ensure_goal_session(self, provider: str, goal_id: str, baseline: dict[str, Any]):
        manager = self.managers[provider]
        current = manager.get_session(goal_id)
        return current if current is not None else manager.create_session(goal_id, baseline)
