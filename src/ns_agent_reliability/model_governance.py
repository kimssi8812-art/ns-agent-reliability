from __future__ import annotations

from dataclasses import dataclass
from enum import Enum


class CandidateState(str, Enum):
    DISCOVERED = "DISCOVERED"
    COMPATIBLE = "COMPATIBLE"
    CANARY = "CANARY"
    ACCEPTED = "ACCEPTED"
    PROMOTED = "PROMOTED"
    QUARANTINED = "QUARANTINED"


@dataclass(frozen=True)
class ExecutionProfile:
    profile_id: str
    provider: str
    runtime_version: str
    adapter_version: str
    model_id: str
    reasoning_profile: str
    capabilities: tuple[str, ...]
    supports_session_reuse: bool | None
    context_capacity_units: int | None
    quality_score: float | None = None
    latency_score: float | None = None
    efficiency_score: float | None = None
    recent_failure_rate: float | None = None
    quota_state: str = "UNKNOWN"
    state: CandidateState = CandidateState.DISCOVERED


@dataclass(frozen=True)
class ProfileDecision:
    profile_id: str | None
    reason: str


def select_profile(
    profiles: list[ExecutionProfile],
    required_capability: str,
    pinned_profile_id: str | None = None,
) -> ProfileDecision:
    """Reference policy: preserve a valid pinned session profile, otherwise rank accepted evidence."""
    by_id = {p.profile_id: p for p in profiles}
    if pinned_profile_id:
        pinned = by_id.get(pinned_profile_id)
        if pinned and pinned.state in {CandidateState.ACCEPTED, CandidateState.PROMOTED}:
            if required_capability in pinned.capabilities and pinned.quota_state not in {"EXHAUSTED", "BLOCKED"}:
                return ProfileDecision(pinned.profile_id, "PINNED_GOAL_SESSION_PROFILE")

    eligible = [
        p for p in profiles
        if required_capability in p.capabilities
        and p.state in {CandidateState.ACCEPTED, CandidateState.PROMOTED}
        and p.quota_state not in {"EXHAUSTED", "BLOCKED"}
    ]
    if not eligible:
        return ProfileDecision(None, "NO_VERIFIED_EXECUTION_PROFILE")

    def score(p: ExecutionProfile) -> tuple[float, float, float, float]:
        quality = -1.0 if p.quality_score is None else p.quality_score
        efficiency = -1.0 if p.efficiency_score is None else p.efficiency_score
        latency = -1.0 if p.latency_score is None else p.latency_score
        failure = 1.0 if p.recent_failure_rate is None else p.recent_failure_rate
        return (quality, efficiency, latency, -failure)

    selected = max(eligible, key=score)
    return ProfileDecision(selected.profile_id, "BEST_VERIFIED_CAPABILITY_RESOURCE_PROFILE")


def can_promote(
    current: ExecutionProfile,
    candidate: ExecutionProfile,
    compatibility_pass: bool,
    canary_pass: bool,
) -> bool:
    if not compatibility_pass or not canary_pass:
        return False
    if candidate.state not in {CandidateState.CANARY, CandidateState.ACCEPTED}:
        return False
    if current.provider != candidate.provider:
        return False
    return True
