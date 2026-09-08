# NS Control Hub

> Historical-context note: words such as “current”, “live”, “healthy”, “blocked” or “verified” in dated sections describe the historical snapshot of that section, not the 2026-09-08 public release candidate or current private runtime. Current publication status is defined by the root README, manifest and publication checklist.


The Control Hub is the non-AI gravity/control layer between GPT/N and the execution layer. In V3 the execution layer includes both provider Worker Managers and a bounded Deterministic Executor.

## Responsibilities

The Hub owns normalized system state, not provider CLI mechanics or unrestricted shell authority. Expected modules include:

- System/Worker/Executor Registry;
- Goal Registry and Goal DAG;
- scheduler/critical path;
- Taskboard lifecycle;
- Evidence/Truth Registry;
- Context/DNA index;
- Progress Engine;
- resource/session/executor telemetry;
- capability router;
- model/runtime/version registry;
- Atomic Machine Event Ledger/reducers;
- Gate/approval state;
- failure/retry/learning ledger;
- external human-facing mirrors/projections.

## Execution choice

The first routing question is no longer only "Which provider?"

```text
checkpoint
 -> authority/security boundary
 -> deterministic or model-reasoning work?
      -> deterministic: bounded executor
      -> semantic/code/analysis: Worker Manager
 -> warm Goal/session affinity
 -> resource/context/quota/reliability
 -> runtime/model/profile compatibility
```

This prevents deterministic checks such as tests, hashes, polling and metadata inspection from consuming provider allocation unnecessarily.

## Goal DAG

Each Goal is represented as dependency nodes with fixed acceptance weights. A node carries at least:

```text
node_id
parents/depends_on
required capability
assigned executor or worker/session
acceptance criteria
fixed weight
state
evidence requirement/evidence status
blocker/failure class
resource references
```

Allowed states can include `QUEUED`, `READY`, `RUNNING`, `BLOCKED`, `VERIFIED`, `FAILED`, and `CANCELLED`.

## Progress

Progress is not "tasks completed / tasks total". The canonical measure is:

```text
Goal Progress = sum(weight of evidence-backed VERIFIED nodes)
                / sum(weight of all acceptance nodes)
```

`RUNNING` contributes no verified completion by itself.

Separate views include:
- Evidence Coverage;
- Critical Path Progress;
- Blocked Weight;
- worker/session/executor state;
- resource/context trends.

## Lifecycle

The desired automated lifecycle is:

```text
request
 -> Goal/DAG
 -> select checkpoint
 -> route executor or worker/profile
 -> execute or create/reuse session
 -> result
 -> verify evidence
 -> emit/consume normalized state transitions
 -> ACKNOWLEDGED/CONSUMED
 -> update DAG/progress
 -> choose next eligible checkpoint
```

The human should not relay worker output between these steps.

## Atomic event truth

V3 promotes execution observability into a control-plane contract:

```text
collectors/adapters
 -> FlowEvent
 -> bounded/durable Event Ledger
 -> reducers/materialized machine state
      -> Machine Flowboard
      -> Human Cockpit
```

The Human Cockpit must not collect an independent truth stream. It is a simplified projection of the same machine state used for orchestration and diagnosis.

## Ports and adapters

Existing capabilities should be connected through ports/adapters rather than rewritten:

- Direct Channel — external chat transport, safe reads, sandbox writes, bounded dispatch and future bounded executor exposure;
- Deterministic Executor — Python/pytest/safe-shell/hash/Git/GitHub/polling within policy;
- Collab — legacy/local worker orchestration and state sources;
- Context/DNA — continuity references and bounded inheritance;
- Taskboard — shared work state;
- Evidence Registry — verifiable result lineage;
- Event Ledger — causal execution lineage/projection source;
- Gate/RPB — operational promotion;
- Git/GitHub — code/history/publication integration;
- Chat Export — canonical conversation intake;
- Linear — optional non-SSOT human mirror.

## Unknown-safe design

A Hub field is not considered known because a model guessed it. If provider quota, context capacity, readiness or resource state cannot be directly verified, the normalized value remains `UNKNOWN` and the router uses the remaining evidence.

## Failure learning

Repeated failures should become durable guards/runbooks/tests rather than chat-only lessons. The system should record failure class, source, evidence, retry result, and the condition that permits a retry. Identical blind retry is prohibited.

## Progressive reduction of GPT/N direct work

During construction, GPT/N may use the bounded executor directly to keep the implementation/test loop continuous. Once a deterministic sequence repeats reliably, it should become a Hub job/adapter. Mature operation therefore reduces routine GPT/N direct execution while retaining diagnostic and exception-handling access.
