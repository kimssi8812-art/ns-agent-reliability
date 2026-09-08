from __future__ import annotations

from dataclasses import dataclass

from .contracts import GoalDefinition, GoalNodeState


@dataclass(frozen=True)
class ProgressSnapshot:
    goal_id: str
    progress_percent: float
    evidence_coverage_percent: float
    blocked_weight_percent: float
    verified_weight: float
    total_weight: float


def calculate_progress(goal: GoalDefinition) -> ProgressSnapshot:
    total = sum(max(0.0, n.weight) for n in goal.nodes)
    verified = sum(
        max(0.0, n.weight)
        for n in goal.nodes
        if n.state == GoalNodeState.VERIFIED
        and (not n.evidence_required or n.evidence_verified)
    )
    blocked = sum(max(0.0, n.weight) for n in goal.nodes if n.state == GoalNodeState.BLOCKED)
    required = [n for n in goal.nodes if n.evidence_required]
    covered = [n for n in required if n.evidence_verified]

    return ProgressSnapshot(
        goal_id=goal.goal_id,
        progress_percent=0.0 if total <= 0 else round(verified / total * 100.0, 2),
        evidence_coverage_percent=100.0 if not required else round(len(covered) / len(required) * 100.0, 2),
        blocked_weight_percent=0.0 if total <= 0 else round(blocked / total * 100.0, 2),
        verified_weight=verified,
        total_weight=total,
    )


def ready_nodes(goal: GoalDefinition) -> list[str]:
    by_id = {node.node_id: node for node in goal.nodes}
    result: list[str] = []
    for node in goal.nodes:
        if node.state not in {GoalNodeState.QUEUED, GoalNodeState.READY}:
            continue
        if all(by_id[parent].state == GoalNodeState.VERIFIED for parent in node.depends_on):
            result.append(node.node_id)
    return result
