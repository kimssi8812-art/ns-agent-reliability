import json
from pathlib import Path
from ns_agent_reliability.doctor import inspect_snapshot, report_dict


def test_broken_example_detects_expected_rule_families():
    root = Path(__file__).resolve().parents[1]
    snapshot = json.loads((root / "examples" / "doctor_broken_system.json").read_text())
    findings = inspect_snapshot(snapshot)
    rules = {f.rule_id for f in findings}
    expected = {
        "STALE_OWNERSHIP", "DUPLICATE_AUTHORITY", "UNBOUNDED_RETRY",
        "RETRY_LINEAGE_CORRUPTION", "CONTEXT_RESUME_DEFECT",
        "EXCESSIVE_PUBLIC_TOOL_SURFACE", "STALE_CLIENT_SERVER_SCHEMA",
        "AUTHORITY_LEAKAGE", "EVIDENCE_GAP", "DUPLICATE_REDISPATCH",
        "STALE_DEPENDENCY_PIN", "SELF_LOCKING_DEPLOY_BOUNDARY",
        "ROLLBACK_RESURRECTS_DEPRECATED_SURFACE",
        "OBSERVABILITY_COUPLED_TO_EXECUTION", "HISTORICAL_STATE_CURRENT_AUTHORITY",
    }
    assert rules == expected
    assert report_dict(snapshot)["finding_count"] == len(expected)


def test_missing_fields_are_unknown_not_failures():
    assert inspect_snapshot({}) == []


def test_healthy_minimal_snapshot_is_clean():
    snapshot = {
        "ownership": {"released_or_expired": True, "session_alive": True, "reacquire_blocked": False},
        "authorities": [{"name": "canonical", "writes": True, "target": "run_state"}],
        "retry": {"enabled": True, "max_attempts": 3, "lineage_nested": False},
        "resume": {"long_running": True, "durable_resume": True, "requires_raw_chat_history": False},
        "public_tools": ["read", "execute", "change", "provider", "phone", "workrun", "status"],
        "mutation": {"enabled": True}, "verification": {"result_evidence_required": True},
        "observability": {"required_for_execution": False},
        "history": {"rebound_as_current_authority": False},
    }
    assert inspect_snapshot(snapshot) == []
