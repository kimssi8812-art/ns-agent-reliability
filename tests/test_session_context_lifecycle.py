from ns_agent_reliability.context import ContextAction, decide_context_action
from ns_agent_reliability.contracts import ContextEnvelope, SessionRecord, SessionState
from ns_agent_reliability.lifecycle import LifecycleState, transition
from ns_agent_reliability.sessions import SessionRegistry


def test_context_unknown_capacity_stays_unknown():
    decision = decide_context_action(ContextEnvelope(), projected_next_units=100)
    assert decision.action == ContextAction.CAPACITY_UNKNOWN


def test_context_uses_reserved_headroom():
    context = ContextEnvelope(
        capacity_units=1000,
        used_units=700,
        reserve_output_units=100,
        reserve_tool_units=50,
        reserve_safety_units=50,
        baseline_units=200,
        delta_units=50,
    )
    assert decide_context_action(context, 50).action == ContextAction.KEEP
    assert decide_context_action(context, 150).action in {ContextAction.COMPACT, ContextAction.ROLLOVER}


def test_only_one_active_session_per_goal():
    registry = SessionRegistry()
    registry.bind(SessionRecord(session_id="s1", goal_id="g1", provider="codex"))
    try:
        registry.bind(SessionRecord(session_id="s2", goal_id="g1", provider="codex"))
    except ValueError as exc:
        assert str(exc) == "ACTIVE_GOAL_SESSION_ALREADY_EXISTS"
    else:
        raise AssertionError("second active Goal session must be rejected")


def test_rollover_preserves_goal_and_increments_generation():
    registry = SessionRegistry()
    registry.bind(SessionRecord(session_id="s1", goal_id="g1", provider="codex", generation=1))
    rolled = registry.rollover("g1", "s2")
    assert rolled.goal_id == "g1"
    assert rolled.generation == 2
    assert rolled.state == SessionState.CREATED


def test_verified_lifecycle_requires_evidence_digest():
    try:
        transition("g", "c", LifecycleState.RESULT_RECEIVED, LifecycleState.RESULT_VERIFIED)
    except ValueError as exc:
        assert str(exc) == "VERIFIED_RESULT_REQUIRES_EVIDENCE_DIGEST"
    else:
        raise AssertionError("verification without evidence digest must fail")
