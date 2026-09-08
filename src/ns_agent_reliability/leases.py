from __future__ import annotations

from dataclasses import dataclass, replace


class LeaseError(RuntimeError):
    """A lease invariant was violated."""


@dataclass(frozen=True)
class Lease:
    workflow_id: str
    holder_session_id: str
    epoch: int
    acquired_at: float
    expires_at: float
    released: bool = False

    def is_active(self, now: float) -> bool:
        return not self.released and now < self.expires_at


class LeaseRegistry:
    """Reference lease/fencing registry independent from client-session liveness.

    The registry deliberately knows nothing about whether a client/operator
    session is alive. Ownership is defined only by the current lease record.
    Every successful acquire creates a strictly newer fencing epoch.
    """

    def __init__(self) -> None:
        self._leases: dict[str, Lease] = {}
        self._epochs: dict[str, int] = {}

    def get(self, workflow_id: str) -> Lease | None:
        return self._leases.get(workflow_id)

    def acquire(
        self,
        workflow_id: str,
        holder_session_id: str,
        *,
        now: float,
        ttl_seconds: float,
    ) -> Lease:
        if not workflow_id or not holder_session_id:
            raise LeaseError("LEASE_IDENTITY_REQUIRED")
        if ttl_seconds <= 0:
            raise LeaseError("LEASE_TTL_MUST_BE_POSITIVE")

        current = self._leases.get(workflow_id)
        if current is not None and current.is_active(now):
            if current.holder_session_id == holder_session_id:
                raise LeaseError("ACTIVE_LEASE_ALREADY_HELD")
            raise LeaseError("ACTIVE_LEASE_HELD_BY_OTHER_SESSION")

        epoch = self._epochs.get(workflow_id, 0) + 1
        lease = Lease(
            workflow_id=workflow_id,
            holder_session_id=holder_session_id,
            epoch=epoch,
            acquired_at=now,
            expires_at=now + ttl_seconds,
        )
        self._epochs[workflow_id] = epoch
        self._leases[workflow_id] = lease
        return lease

    def release(
        self,
        workflow_id: str,
        holder_session_id: str,
        epoch: int,
    ) -> Lease:
        current = self._require(workflow_id)
        self._require_identity(current, holder_session_id, epoch)
        if current.released:
            return current
        released = replace(current, released=True)
        self._leases[workflow_id] = released
        return released

    def finish(
        self,
        workflow_id: str,
        holder_session_id: str,
        epoch: int,
        *,
        checkpoint_safe: bool,
    ) -> Lease:
        """Finish completed mutation ownership without waiting for TTL expiry.

        This is deliberately only a checkpoint-safe alias of the existing
        release primitive. It creates no second lifecycle/state authority and
        never permits takeover of another holder's active lease.
        """
        if not checkpoint_safe:
            raise LeaseError("WORKFLOW_FINISH_REQUIRES_CHECKPOINT_SAFE")
        return self.release(workflow_id, holder_session_id, epoch)

    def authorize(
        self,
        workflow_id: str,
        holder_session_id: str,
        epoch: int,
        *,
        now: float,
    ) -> Lease:
        current = self._require(workflow_id)
        self._require_identity(current, holder_session_id, epoch)
        if current.released:
            raise LeaseError("LEASE_RELEASED")
        if now >= current.expires_at:
            raise LeaseError("LEASE_EXPIRED")
        return current

    def _require(self, workflow_id: str) -> Lease:
        try:
            return self._leases[workflow_id]
        except KeyError as exc:
            raise LeaseError("LEASE_NOT_FOUND") from exc

    @staticmethod
    def _require_identity(current: Lease, holder_session_id: str, epoch: int) -> None:
        if current.holder_session_id != holder_session_id:
            raise LeaseError("LEASE_HOLDER_MISMATCH")
        if current.epoch != epoch:
            raise LeaseError("STALE_FENCING_EPOCH")
