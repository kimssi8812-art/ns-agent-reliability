# Worker Manager and Goal Session

## Why a Worker Manager exists

Directly mapping every checkpoint to a new provider CLI process creates cold-start overhead, duplicate context hydration, fragmented state, and poor resource observability.

The Worker Manager is a provider-neutral lifecycle contract. Private NS history includes provider-specific adapter implementations, while this public candidate exposes only reference/scaffold portions and does not claim a production-complete universal Worker Manager.

## Common responsibilities

Each manager should own:

- provider/runtime discovery;
- auth/readiness/quota/resource normalization;
- Goal Session create/reuse/checkpoint/compact/rollover/close;
- session watchdog;
- context baseline/delta lineage;
- runtime/model/reasoning profile selection and pinning;
- session resource telemetry;
- crash recovery;
- idle cleanup.

The Hub consumes normalized manager state rather than branching on provider-specific CLI details.

## Goal Session invariant

```text
one Goal -> one active verified session
```

Multiple checkpoints under the same Goal should reuse that session unless a controlled rollover is required.

## Lifecycle

```text
GOAL_ASSIGNED
 -> SESSION_CREATE
 -> BASELINE_HYDRATED
 -> RUNNING
 -> CHECKPOINT*
 -> GOAL_RESULT
 -> STATE_PERSISTED
 -> SESSION_CLOSE
```

A controlled rollover inserts:

```text
CHECKPOINT_PERSISTED
 -> SESSION_CLOSE generation N
 -> SESSION_CREATE generation N+1
 -> compact baseline hydrate once
 -> continue
```

## Health semantics

A key invariant discovered during implementation review is:

```text
LIVENESS != READINESS != DISPATCH_ALLOWED
```

Examples:

- a tmux session may be alive while the provider is out of quota;
- a process may be alive but waiting for authentication;
- a stale health file may say blocked while a fresh authoritative readiness probe says ready;
- absence of an auto-sleep flag is neutral, not proof of readiness.

A liveness-only source must never grant dispatch permission.

## Codex legacy deadlock case study

A legacy auto-sleep mechanism could stop a `codex_collab` tmux session after Collab inbox idle. Direct Channel health depended on that tmux session, but Direct Channel tasks did not wake through the Collab inbox path before preflight. This caused a circular `SESSION_DEAD` state and forced Claude fallback.

The permanent architectural fix is to make Direct Channel-native Worker Manager/session state the Direct Channel readiness authority. Legacy tmux state may remain an input, but it cannot be the sole gate for a different transport.

## Recovery policy

Recovery should distinguish failure classes such as:

- session/process dead;
- auth expired;
- quota/rate limit;
- stale health;
- malformed IPC;
- context capacity/rollover;
- provider/tool incompatibility.

A retry is permitted only when new evidence indicates the previous blocker may have changed.
