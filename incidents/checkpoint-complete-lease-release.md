# Incident: Completed Workflow Kept a Write Lease Until TTL Expiry

## Failure class

A workflow mutation finished successfully, but the write lease remained active because the explicit release/finish call did not complete. The work was already checkpoint-safe, yet the next legitimate writer had to wait for TTL expiry.

This is not a reason to weaken fencing or permit lease theft. It is a lifecycle-finalization gap: **completed mutation ownership should be explicitly finished at the completion boundary**.

## Minimal reproduction

```text
Client A acquires lease(epoch=40, ttl=900s)
Client A completes and checkpoints the mutation
release/finish delivery fails before the lease registry is updated
Client B needs the same workflow

EXPECTED: checkpoint-safe finish releases A immediately; B can acquire epoch=41
BROKEN: B waits for the remaining TTL despite the completed mutation
```

## Corrected model

```text
active mutation
  -> keep lease + fencing

checkpoint-safe completion
  -> finish(existing release primitive)
  -> released = true immediately
  -> next acquire gets newer epoch

not checkpoint-safe
  -> finish denied

foreign holder / wrong epoch
  -> finish denied
```

## Invariants

- `CHECKPOINT_COMPLETE_MUST_RELEASE_WRITE_OWNERSHIP`.
- Completion finalization reuses the existing release primitive; it does not create another lease store, manager, scheduler, or lifecycle authority.
- `finish` requires an explicit checkpoint-safe assertion.
- A foreign holder cannot finish or steal another holder's active lease.
- A failed or missing finish call never authorizes unsafe takeover; ordinary TTL expiry remains the fallback.
- After successful finish, the next acquire receives a strictly newer fencing epoch immediately rather than waiting for TTL expiry.

## Portable implementation

See `src/ns_agent_reliability/leases.py` and `tests/test_lease_session_independence.py`.

The portable reference adds `LeaseRegistry.finish(..., checkpoint_safe=True)` as a thin semantic wrapper over the existing `release` operation. The goal is to make the completion boundary explicit without adding orchestration layers.

Focused regression for the new finish contract: **3/3 PASS** in the bounded executor workspace.

## Doctor rule seed

Flag a reliability smell when all of the following are true:

1. a mutation is terminal/checkpoint-safe;
2. its write ownership remains active solely until TTL expiry;
3. a later writer is blocked by that stale completion ownership.

Suggested remediation: expose one idempotent checkpoint-safe finish/release path and verify immediate newer-epoch reacquisition. Do not solve it with lease stealing or a second recovery manager.

## License partition

- portable code/tests/Doctor rule: Apache-2.0 candidate;
- sanitized incident/postmortem/tutorial text: CC BY 4.0 candidate;
- brand/trademark excluded from the open-license grant;
- third-party material remains governed by original provenance/licenses.
