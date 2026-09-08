"""Portable build-once / verify-once / one atomic production commit primitive.

This module intentionally contains no NS paths, credentials, provider bindings,
or privileged-runtime assumptions. Validation happens before commit. The commit
boundary performs only immutable input checks, live CAS, rollback-point creation,
atomic replacement, one smoke callback, and a durable receipt returned to caller.
"""
from __future__ import annotations

import hashlib
import json
import os
import shutil
import tempfile
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Callable, Iterable, Mapping


class DeploymentError(RuntimeError):
    pass


@dataclass(frozen=True)
class ReadyArtifact:
    candidate_sha256: str
    validation_evidence_sha256: str


@dataclass(frozen=True)
class DeploymentReceipt:
    status: str
    target: str
    candidate_sha256: str
    live_before_sha256: str
    live_after_sha256: str
    rollback_triggered: bool
    reason: str | None = None


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as fh:
        for chunk in iter(lambda: fh.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def _fsync_dir(path: Path) -> None:
    fd = os.open(path, os.O_RDONLY)
    try:
        os.fsync(fd)
    finally:
        os.close(fd)


def failed_candidate_sha256(receipts: Iterable[Mapping[str, object]]) -> set[str]:
    """Return candidate hashes that mutated LIVE, failed, and rolled back."""
    out: set[str] = set()
    for receipt in receipts:
        if receipt.get("status") == "FAILED" and receipt.get("rollback_triggered") is True:
            value = receipt.get("candidate_sha256")
            if isinstance(value, str) and len(value) == 64:
                out.add(value)
    return out


def commit_once(
    *,
    target: Path,
    candidate: Path,
    validation_evidence: Path,
    ready: ReadyArtifact,
    expected_live_sha256: str,
    smoke: Callable[[Path], bool],
    previous_receipts: Iterable[Mapping[str, object]] = (),
) -> DeploymentReceipt:
    """Promote one already-validated candidate exactly once.

    Preconditions fail before mutation. A post-replace smoke failure restores the
    byte-exact rollback point once and permanently marks the failed candidate in
    the returned receipt so callers can deny replay of the same SHA.
    """
    for path in (target, candidate, validation_evidence):
        if path.is_symlink() or not path.is_file():
            raise DeploymentError(f"REGULAR_FILE_REQUIRED:{path}")

    live_before = sha256_file(target)
    if live_before != expected_live_sha256:
        raise DeploymentError("LIVE_CAS_MISMATCH")

    candidate_sha = sha256_file(candidate)
    if candidate_sha != ready.candidate_sha256:
        raise DeploymentError("CANDIDATE_SHA_MISMATCH")
    if candidate_sha in failed_candidate_sha256(previous_receipts):
        raise DeploymentError("FAILED_CANDIDATE_SHA_RETRY_DENIED")

    evidence_sha = sha256_file(validation_evidence)
    if evidence_sha != ready.validation_evidence_sha256:
        raise DeploymentError("VALIDATION_EVIDENCE_SHA_MISMATCH")

    backup_fd, backup_name = tempfile.mkstemp(prefix=f".{target.name}.rollback.", dir=target.parent)
    os.close(backup_fd)
    backup = Path(backup_name)
    stage: Path | None = None
    try:
        shutil.copy2(target, backup)
        if sha256_file(backup) != live_before:
            raise DeploymentError("ROLLBACK_POINT_MISMATCH")

        stage_fd, stage_name = tempfile.mkstemp(prefix=f".{target.name}.candidate.", dir=target.parent)
        os.close(stage_fd)
        stage = Path(stage_name)
        shutil.copy2(candidate, stage)
        if sha256_file(stage) != candidate_sha:
            raise DeploymentError("STAGED_CANDIDATE_SHA_MISMATCH")

        os.replace(stage, target)
        stage = None
        _fsync_dir(target.parent)
        live_after = sha256_file(target)
        if live_after != candidate_sha:
            raise DeploymentError("POST_COMMIT_SHA_MISMATCH")

        if smoke(target):
            return DeploymentReceipt(
                status="APPLIED_VERIFIED",
                target=str(target),
                candidate_sha256=candidate_sha,
                live_before_sha256=live_before,
                live_after_sha256=live_after,
                rollback_triggered=False,
            )

        # One rollback. No recursive rollback/retry loop.
        os.replace(backup, target)
        _fsync_dir(target.parent)
        restored = sha256_file(target)
        if restored != live_before:
            raise DeploymentError("ROLLBACK_SHA_MISMATCH")
        return DeploymentReceipt(
            status="FAILED",
            target=str(target),
            candidate_sha256=candidate_sha,
            live_before_sha256=live_before,
            live_after_sha256=restored,
            rollback_triggered=True,
            reason="SMOKE_FAILED",
        )
    finally:
        if stage is not None and stage.exists():
            stage.unlink()
        if backup.exists():
            backup.unlink()


def receipt_json(receipt: DeploymentReceipt) -> str:
    return json.dumps(asdict(receipt), sort_keys=True, separators=(",", ":"))
