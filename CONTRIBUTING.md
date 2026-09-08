# Contributing

This project uses evidence-first engineering. A contribution is not complete because a worker or model says it is complete.

## Contribution flow

```text
issue/goal
 -> acceptance criteria + fixed scope
 -> reference-contract check
 -> sandbox implementation
 -> tests
 -> evidence artifact/digest
 -> independent review where appropriate
 -> merge candidate
```

## Design rules

- Prefer adapting an existing port/module before creating a parallel subsystem.
- Keep provider-specific CLI mechanics behind provider adapters/Worker Managers.
- Preserve `LIVENESS != READINESS != DISPATCH_ALLOWED`.
- Keep Goal/session state durable outside the model.
- Do not make model context the source of truth.
- Do not invent provider quota/context values.
- Do not increase progress for `RUNNING`; progress is evidence-weighted.
- Do not change a running Goal Session's execution profile casually; use controlled rollover.
- Do not add unrestricted shell capabilities to the chat-facing layer.

## Tests expected

Changes should include semantic tests, not only structural tests. When fixing a production-discovered bug, add a regression case that would have caught the original error.

## Evidence labels

Use `PASS_VERIFIED`, `FAIL_VERIFIED`, `REVOKED`, `PARTIAL`, `NOT_RUN`, or `UNKNOWN` in engineering reports where the distinction matters.

## Provider adapters

Before encoding a CLI flag, model identifier, context capacity, or session-resume capability, verify it against the installed runtime or authoritative provider documentation. Unsupported assumptions should remain explicit adapter TODOs rather than fabricated compatibility.
