from ns_agent_reliability.contracts import (
    GoalDefinition,
    GoalNode,
    GoalNodeState,
    ResourceSnapshot,
    WorkerState,
)
from ns_agent_reliability.health import HealthSignal, normalize_health
from ns_agent_reliability.model_governance import (
    CandidateState,
    ExecutionProfile,
    select_profile,
)
from ns_agent_reliability.progress import calculate_progress
from ns_agent_reliability.routing import choose_worker


def test_liveness_does_not_imply_dispatch():
    result = normalize_health([
        HealthSignal(source="tmux", liveness="ALIVE", readiness="UNKNOWN", dispatch_allowed=None)
    ])
    assert result.dispatch_allowed is False


def test_authoritative_ready_allow_dispatches():
    result = normalize_health([
        HealthSignal(source="readiness", liveness="ALIVE", readiness="READY", dispatch_allowed=True)
    ])
    assert result.dispatch_allowed is True
    assert result.worker_state == WorkerState.READY


def test_running_node_does_not_add_progress():
    goal = GoalDefinition(
        goal_id="g",
        nodes=[
            GoalNode("verified", 25, GoalNodeState.VERIFIED, evidence_verified=True),
            GoalNode("running", 75, GoalNodeState.RUNNING),
        ],
    )
    assert calculate_progress(goal).progress_percent == 25.0


def test_warm_goal_session_has_routing_affinity():
    workers = [
        ResourceSnapshot("claude", "now", WorkerState.READY, True, active_sessions=0),
        ResourceSnapshot("codex", "now", WorkerState.READY, True, active_sessions=0),
    ]
    decision = choose_worker("code", workers, warm_goal_providers={"claude"})
    assert decision.provider == "claude"
    assert decision.reason == "WARM_GOAL_SESSION"


def test_execution_profile_stays_pinned_when_valid():
    profiles = [
        ExecutionProfile(
            profile_id="pinned",
            provider="codex",
            runtime_version="1",
            adapter_version="1",
            model_id="model-a",
            reasoning_profile="medium",
            capabilities=("code",),
            supports_session_reuse=True,
            context_capacity_units=1000,
            quality_score=0.8,
            efficiency_score=0.9,
            state=CandidateState.ACCEPTED,
        ),
        ExecutionProfile(
            profile_id="newer",
            provider="codex",
            runtime_version="2",
            adapter_version="2",
            model_id="model-b",
            reasoning_profile="high",
            capabilities=("code",),
            supports_session_reuse=True,
            context_capacity_units=2000,
            quality_score=0.99,
            efficiency_score=0.7,
            state=CandidateState.PROMOTED,
        ),
    ]
    decision = select_profile(profiles, "code", pinned_profile_id="pinned")
    assert decision.profile_id == "pinned"
