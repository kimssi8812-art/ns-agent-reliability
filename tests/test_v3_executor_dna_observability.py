import hashlib
import json

from ns_agent_reliability.dna import build_inheritance_packet, parse_share_url, provider_required_for_intent
from ns_agent_reliability.executor import (
    CommandClass,
    ExecutorPolicy,
    ExecutorRequest,
    validate_executor_request,
)
from ns_agent_reliability.observability import (
    EventLedger,
    FlowEvent,
    MachineFlowboardSnapshot,
    project_human,
)


def test_deterministic_dna_intents_do_not_require_provider():
    assert provider_required_for_intent("CHAT_SHARE") is False
    assert provider_required_for_intent("chat_share") is False
    assert provider_required_for_intent("DNA_HYDRATION") is False
    assert provider_required_for_intent("analysis") is True


def test_share_url_is_canonical_and_idempotent():
    spec = parse_share_url("https://chatgpt.com/share/00000000-0000-0000-0000-000000000000")
    assert spec.slug == "00000000-0000-0000-0000-000000000000"
    assert spec.idempotency_key == "chat-export:00000000-0000-0000-0000-000000000000"


def test_inheritance_packet_is_bounded_and_does_not_default_to_full_history():
    dna = {
        "title": "example",
        "conversation_type": "WORK",
        "completeness": "VERIFIED_COMPLETE",
        "current_state": "IN_PROGRESS",
        "core_purpose": "x" * 1000,
        "summary": "y" * 2000,
        "last_context": {"user_intent": "continue", "unfinished_point": "next"},
        "next_actions": [{"message_ref": str(i), "text": "z" * 500} for i in range(20)],
    }
    digest = hashlib.sha256(json.dumps(dna, sort_keys=True).encode()).hexdigest()
    packet = build_inheritance_packet(dna, slug="s", source_digest=digest, max_bytes=4096)
    encoded = json.dumps(packet, ensure_ascii=False, separators=(",", ":")).encode("utf-8")
    assert len(encoded) <= 4096
    assert packet["packet_bytes"] == len(encoded)
    assert packet["provider_calls_required"] == 0
    assert packet["full_history_default_read"] is False


def test_executor_allows_bounded_pytest_and_blocks_sudo_ssot():
    policy = ExecutorPolicy(
        allowed_roots=("/sandbox",),
        allowed_classes=frozenset({CommandClass.PYTEST, CommandClass.HASH}),
        allow_writes=False,
        allow_sudo=False,
        allow_ssot_mutation=False,
    )
    safe = ExecutorRequest(
        run_id="r1",
        goal_id="g",
        checkpoint_id="c",
        command_class=CommandClass.PYTEST,
        cwd="/sandbox/project",
        timeout_sec=60,
        expected_output_limit=8192,
    )
    assert validate_executor_request(safe, policy).allowed is True

    unsafe = ExecutorRequest(
        run_id="r2",
        goal_id="g",
        checkpoint_id="c",
        command_class=CommandClass.PYTEST,
        cwd="/sandbox/project",
        timeout_sec=60,
        expected_output_limit=8192,
        sudo_requested=True,
        ssot_mutation_requested=True,
    )
    decision = validate_executor_request(unsafe, policy)
    assert decision.allowed is False
    assert decision.reason in {"SUDO_NOT_ALLOWED", "SSOT_MUTATION_NOT_ALLOWED"}


def test_human_snapshot_is_projection_of_machine_state():
    event = FlowEvent(
        event_id="e1",
        sequence=1,
        event_type="SESSION_RUNNING",
        observed_at="now",
        source="test",
        authority="TEST",
        project_id="p",
        state_before="READY",
        state_after="RUNNING",
        goal_id="g",
    )
    ledger = EventLedger()
    ledger.append(event)
    machine = MachineFlowboardSnapshot(
        snapshot_id="s1",
        observed_at="now",
        cursor=1,
        goals=({"goal_id": "g", "state": "RUNNING"},),
        workers=(),
        sessions=({
            "provider": "codex",
            "session_scope": "GOAL_SESSION",
            "goal_id": "g",
            "checkpoint_id": "c1",
            "model_id": "model",
            "state": "RUNNING",
        },),
        executor_runs=(),
        events=ledger.all(),
    )
    human = project_human(machine)
    assert human.snapshot_id == machine.snapshot_id
    assert human.active_work[0]["actor"] == "codex"
    assert human.active_work[0]["goal_id"] == "g"
