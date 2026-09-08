# Incident: Released Lease Blocked by a Still-Live Client Session

## Failure class

A workflow mutation lease was released or expired, but a different client could not acquire the workflow because the previous client session was still alive.

That couples two independent facts:

- **client-session liveness** — whether a client/operator connection still exists;
- **mutation ownership** — whether that client currently holds the workflow lease.

A live client session is not proof of current workflow ownership.

## Minimal reproduction

```text
Client A acquires lease(epoch=16)
Client A releases the lease
Client A session remains alive
current holder = none
Client B acquires the same workflow

EXPECTED: Client B receives epoch=17
BROKEN: acquire is rejected because Client A is still alive
```

## Root cause

Lease recovery/reacquisition treated session liveness as ownership authority. The ownership boundary therefore survived after the ownership record itself had expired or been released.

## Corrected model

```text
client session lifecycle ─────────────── independent

workflow lease:
  holder + expiry/release + fencing epoch
       │
       ├─ active foreign lease -> deny takeover
       ├─ released lease       -> reacquire allowed
       ├─ expired lease        -> reacquire allowed
       └─ every acquire        -> strictly newer epoch

execution boundary:
  command epoch must equal current lease epoch
  stale epoch -> reject
```

## Invariants

- Session liveness does not imply lease ownership.
- An unexpired foreign lease cannot be stolen.
- A released or expired lease can be reacquired without closing the previous client session.
- Every successful acquire advances a monotonic fencing epoch.
- Commands from the previous holder are rejected after a newer epoch is issued.
- Recovery does not create a second lease store, scheduler, manager, or mutation authority.

## Portable implementation

See `src/ns_agent_reliability/leases.py` and `tests/test_lease_session_independence.py`.

The publication-candidate reference implementation intentionally keeps session state outside the lease registry so the failure cannot be reintroduced by consulting session liveness during acquisition.

## Production lesson

Long-running agent systems often need clients to remain connected after a specific ownership window ends. Treating connection/session lifetime and mutation ownership as one lifecycle creates deadlocks and stale-owner behavior. Separate them and fence mutations with an explicit monotonic epoch.
