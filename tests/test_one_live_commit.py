from pathlib import Path
import pytest

from ns_agent_reliability.deployment import (
    DeploymentError,
    ReadyArtifact,
    commit_once,
    sha256_file,
)


def setup_case(tmp_path: Path):
    target = tmp_path / "live.txt"
    candidate = tmp_path / "candidate.txt"
    evidence = tmp_path / "validation.json"
    target.write_text("stable\n", encoding="utf-8")
    candidate.write_text("new\n", encoding="utf-8")
    evidence.write_text('{"tests":"PASS"}\n', encoding="utf-8")
    ready = ReadyArtifact(sha256_file(candidate), sha256_file(evidence))
    return target, candidate, evidence, ready


def test_success_is_one_atomic_commit(tmp_path):
    target, candidate, evidence, ready = setup_case(tmp_path)
    receipt = commit_once(
        target=target, candidate=candidate, validation_evidence=evidence,
        ready=ready, expected_live_sha256=sha256_file(target), smoke=lambda _: True,
    )
    assert receipt.status == "APPLIED_VERIFIED"
    assert receipt.rollback_triggered is False
    assert target.read_text() == "new\n"


def test_live_cas_mismatch_has_zero_mutation(tmp_path):
    target, candidate, evidence, ready = setup_case(tmp_path)
    before = target.read_bytes()
    with pytest.raises(DeploymentError, match="LIVE_CAS_MISMATCH"):
        commit_once(target=target, candidate=candidate, validation_evidence=evidence,
                    ready=ready, expected_live_sha256="0" * 64, smoke=lambda _: True)
    assert target.read_bytes() == before


def test_candidate_sha_mismatch_has_zero_mutation(tmp_path):
    target, candidate, evidence, ready = setup_case(tmp_path)
    before = target.read_bytes()
    bad = ReadyArtifact("1" * 64, ready.validation_evidence_sha256)
    with pytest.raises(DeploymentError, match="CANDIDATE_SHA_MISMATCH"):
        commit_once(target=target, candidate=candidate, validation_evidence=evidence,
                    ready=bad, expected_live_sha256=sha256_file(target), smoke=lambda _: True)
    assert target.read_bytes() == before


def test_evidence_sha_mismatch_has_zero_mutation(tmp_path):
    target, candidate, evidence, ready = setup_case(tmp_path)
    before = target.read_bytes()
    bad = ReadyArtifact(ready.candidate_sha256, "2" * 64)
    with pytest.raises(DeploymentError, match="VALIDATION_EVIDENCE_SHA_MISMATCH"):
        commit_once(target=target, candidate=candidate, validation_evidence=evidence,
                    ready=bad, expected_live_sha256=sha256_file(target), smoke=lambda _: True)
    assert target.read_bytes() == before


def test_symlink_evidence_is_denied(tmp_path):
    target, candidate, evidence, ready = setup_case(tmp_path)
    link = tmp_path / "evidence-link.json"
    link.symlink_to(evidence)
    before = target.read_bytes()
    with pytest.raises(DeploymentError, match="REGULAR_FILE_REQUIRED"):
        commit_once(target=target, candidate=candidate, validation_evidence=link,
                    ready=ready, expected_live_sha256=sha256_file(target), smoke=lambda _: True)
    assert target.read_bytes() == before


def test_smoke_failure_rolls_back_once(tmp_path):
    target, candidate, evidence, ready = setup_case(tmp_path)
    stable_sha = sha256_file(target)
    receipt = commit_once(
        target=target, candidate=candidate, validation_evidence=evidence,
        ready=ready, expected_live_sha256=stable_sha, smoke=lambda _: False,
    )
    assert receipt.status == "FAILED"
    assert receipt.rollback_triggered is True
    assert sha256_file(target) == stable_sha


def test_same_failed_candidate_sha_is_not_repromoted(tmp_path):
    target, candidate, evidence, ready = setup_case(tmp_path)
    stable_sha = sha256_file(target)
    failed = commit_once(
        target=target, candidate=candidate, validation_evidence=evidence,
        ready=ready, expected_live_sha256=stable_sha, smoke=lambda _: False,
    )
    with pytest.raises(DeploymentError, match="FAILED_CANDIDATE_SHA_RETRY_DENIED"):
        commit_once(target=target, candidate=candidate, validation_evidence=evidence,
                    ready=ready, expected_live_sha256=stable_sha, smoke=lambda _: True,
                    previous_receipts=[failed.__dict__])
