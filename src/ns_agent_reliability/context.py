from __future__ import annotations

from dataclasses import dataclass
from enum import Enum

from .contracts import ContextEnvelope


class ContextAction(str, Enum):
    KEEP = "KEEP"
    EXTERNALIZE = "EXTERNALIZE"
    COMPACT = "COMPACT"
    ROLLOVER = "ROLLOVER"
    CAPACITY_UNKNOWN = "CAPACITY_UNKNOWN"


@dataclass(frozen=True)
class ContextDecision:
    action: ContextAction
    reason: str


def decide_context_action(
    context: ContextEnvelope,
    projected_next_units: int,
    large_inline_artifact: bool = False,
) -> ContextDecision:
    """Reference policy; deployment-specific token estimators live behind adapters."""
    if large_inline_artifact:
        return ContextDecision(ContextAction.EXTERNALIZE, "LARGE_ARTIFACT_SHOULD_BE_REFERENCED")

    can_accept = context.can_accept(projected_next_units)
    if can_accept is None:
        return ContextDecision(ContextAction.CAPACITY_UNKNOWN, "PROVIDER_CAPACITY_NOT_VERIFIED")
    if can_accept:
        return ContextDecision(ContextAction.KEEP, "ENOUGH_RESERVED_HEADROOM")

    # Production policy may distinguish compact vs rollover using measured
    # compaction yield and information-loss evidence.
    if context.delta_units > context.baseline_units:
        return ContextDecision(ContextAction.COMPACT, "DELTA_GROWTH_EXCEEDS_BASELINE")
    return ContextDecision(ContextAction.ROLLOVER, "NEXT_CHECKPOINT_CANNOT_FIT_WITH_RESERVES")
