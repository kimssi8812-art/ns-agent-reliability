from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from pathlib import PurePosixPath


class CommandClass(str, Enum):
    PYTHON = "PYTHON"
    PYTEST = "PYTEST"
    SAFE_SHELL = "SAFE_SHELL"
    HASH = "HASH"
    GIT = "GIT"
    GITHUB = "GITHUB"
    FILESYSTEM = "FILESYSTEM"
    POLL = "POLL"


@dataclass(frozen=True)
class ExecutorPolicy:
    allowed_roots: tuple[str, ...]
    allowed_classes: frozenset[CommandClass]
    allow_writes: bool = False
    max_timeout_sec: int = 120
    max_output_bytes: int = 64 * 1024
    allow_sudo: bool = False
    allow_ssot_mutation: bool = False


@dataclass(frozen=True)
class ExecutorRequest:
    run_id: str
    goal_id: str
    checkpoint_id: str
    command_class: CommandClass
    cwd: str
    timeout_sec: int
    expected_output_limit: int
    write_requested: bool = False
    sudo_requested: bool = False
    ssot_mutation_requested: bool = False


@dataclass(frozen=True)
class ExecutorDecision:
    allowed: bool
    reason: str


def _within_roots(path: str, roots: tuple[str, ...]) -> bool:
    candidate = PurePosixPath(path)
    for root in roots:
        base = PurePosixPath(root)
        if candidate == base or base in candidate.parents:
            return True
    return False


def validate_executor_request(request: ExecutorRequest, policy: ExecutorPolicy) -> ExecutorDecision:
    if request.command_class not in policy.allowed_classes:
        return ExecutorDecision(False, "COMMAND_CLASS_NOT_ALLOWED")
    if not _within_roots(request.cwd, policy.allowed_roots):
        return ExecutorDecision(False, "CWD_OUTSIDE_ALLOWED_ROOTS")
    if request.timeout_sec <= 0 or request.timeout_sec > policy.max_timeout_sec:
        return ExecutorDecision(False, "TIMEOUT_OUT_OF_POLICY")
    if request.expected_output_limit <= 0 or request.expected_output_limit > policy.max_output_bytes:
        return ExecutorDecision(False, "OUTPUT_LIMIT_OUT_OF_POLICY")
    if request.write_requested and not policy.allow_writes:
        return ExecutorDecision(False, "WRITE_NOT_ALLOWED")
    if request.sudo_requested and not policy.allow_sudo:
        return ExecutorDecision(False, "SUDO_NOT_ALLOWED")
    if request.ssot_mutation_requested and not policy.allow_ssot_mutation:
        return ExecutorDecision(False, "SSOT_MUTATION_NOT_ALLOWED")
    return ExecutorDecision(True, "BOUNDED_EXECUTION_ALLOWED")
