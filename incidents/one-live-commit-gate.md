# Incident: Deployment Gate Became the Deployment Workflow

## Failure class

A production change boundary gradually accumulated build checks, repeated policy scans, readiness hooks, registrars, post-registrars, and retry logic. The result was a deployment path that could reject a correct candidate because an older guard still encoded obsolete semantics.

## Root cause

Validation and commit authority were conflated. The Gate re-ran or reinterpreted work that should have been completed before the production boundary.

## Corrected model

```text
build once
→ test / security / regression once
→ READY artifact + validation-evidence digest
→ ONE LIVE COMMIT
   1. compare expected live SHA (CAS)
   2. verify candidate SHA
   3. verify evidence SHA
   4. create rollback point
   5. atomic replace
→ one bounded smoke
   PASS → receipt
   FAIL → rollback once + candidate SHA retired
```

## Invariants

- Precondition failure causes zero production mutation.
- Validation evidence is content-bound, not a decorative string.
- A candidate that failed after production mutation is never promoted again under the same SHA.
- A fix creates a new candidate SHA.
- Rollback happens once; rollback failure does not start another retry/rollback loop.
- The Gate is a commit boundary, not a second test pipeline, scheduler, workflow engine, or state store.

## Portable implementation

See `src/ns_agent_reliability/deployment.py` and `tests/test_one_live_commit.py`.

The reference implementation intentionally contains no private deployment paths, credentials, provider-specific bindings, or product-specific business logic.
