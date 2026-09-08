from __future__ import annotations

from dataclasses import dataclass

from .contracts import ResourceSnapshot, WorkerState


@dataclass(frozen=True)
class RouteDecision:
    provider: str | None
    mode: str
    reason: str


def choose_worker(
    capability: str,
    snapshots: list[ResourceSnapshot],
    warm_goal_providers: set[str] | None = None,
) -> RouteDecision:
    warm_goal_providers = warm_goal_providers or set()
    eligible = [
        s for s in snapshots
        if s.dispatch_allowed and s.worker_state in {WorkerState.READY, WorkerState.BUSY}
    ]
    if not eligible:
        return RouteDecision(None, "BLOCKED", "NO_DISPATCHABLE_WORKER")

    warm = [s for s in eligible if s.provider in warm_goal_providers]
    if warm:
        selected = sorted(warm, key=lambda s: (s.active_sessions, s.recent_failure, -s.recent_success))[0]
        mode = "DEGRADED_SINGLE_AGENT" if len(eligible) == 1 else "NORMAL"
        return RouteDecision(selected.provider, mode, "WARM_GOAL_SESSION")

    preferences = {
        "code": ("codex", "claude", "gemini"),
        "test": ("codex", "claude", "gemini"),
        "analysis": ("gemini", "claude", "codex"),
        "counterexample": ("gemini", "claude", "codex"),
        "architecture": ("claude", "gemini", "codex"),
    }
    order = preferences.get(capability, ("codex", "gemini", "claude"))

    ranked = sorted(
        eligible,
        key=lambda s: (
            order.index(s.provider) if s.provider in order else len(order),
            s.active_sessions,
            s.recent_failure,
            -s.recent_success,
        ),
    )
    selected = ranked[0]
    mode = "DEGRADED_SINGLE_AGENT" if len(eligible) == 1 else "NORMAL"
    return RouteDecision(selected.provider, mode, "CAPABILITY_READINESS_LOAD")
