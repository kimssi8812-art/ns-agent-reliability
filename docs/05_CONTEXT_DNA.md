# Context and DNA Continuity

> Historical-context note: words such as “current”, “live”, “healthy”, “blocked” or “verified” in dated sections describe the historical snapshot of that section, not the 2026-09-08 public release candidate or current private runtime. Current publication status is defined by the root README, manifest and publication checklist.


## The cold-start problem

A multi-agent system wastes time and provider allocation if every bounded task receives the full conversation history, rereads the same files, or starts a worker with no retained Goal context.

The project separates durable truth from active model context and, in V3, separates deterministic DNA infrastructure from provider reasoning.

## Context hierarchy

```text
GLOBAL DNA REFERENCE
  -> WORKER PROFILE
  -> GOAL BASELINE
  -> SESSION DELTA
```

### Global DNA reference

Contains stable architecture identity and invariant references. It should be referenced by digest/summary rather than replayed in full.

### Worker profile

Contains provider capabilities, tool boundaries, current runtime/model profile, and resource/readiness metadata.

### Goal baseline

Contains only what the Goal needs:
- Goal and DAG slice;
- authority/scope;
- relevant registry/Taskboard state;
- required source baselines;
- evidence references + digests;
- blockers/approval state.

### Session delta

Contains only changes since the previous checkpoint: new evidence, changed source digest, new blocker, changed authority, new acceptance state, or new instructions.

## Baseline-once invariant

A verified Goal Session hydrates its baseline once. Ordinary checkpoint continuation should not trigger a full rehydrate.

Full rehydration is justified by:
- new Goal;
- worker session death/restart;
- source baseline drift;
- authority/scope change;
- `CONTEXT_NOT_VERIFIED`;
- controlled rollover after checkpoint persistence.

## Zero-unnecessary-AI DNA

Conversation ingestion and ordinary inheritance are control-plane responsibilities by default.

```text
share reference
 -> deterministic intake
 -> transcript extraction
 -> completeness verification
 -> deterministic package/compiler
 -> DNA registry/index
 -> bounded inheritance packet/reference
 -> Goal/new-room baseline
```

A provider model is not required merely to:
- create/poll an intake record;
- locate generated artifacts;
- verify a digest;
- inspect completeness metadata;
- register DNA;
- pass DNA from one AI to another.

A model may perform optional semantic enrichment, but enrichment is separately budgeted and must not become a prerequisite for canonical extraction/completeness truth.

## Explicit DNA targeting

A production implementation must not silently choose the newest conversation directory when inherited work refers to a particular conversation or Goal. DNA selection should be tied to an explicit conversation identifier, Goal relationship, or verified registry reference. Ambiguity fails closed rather than hydrating unrelated history.

## Bounded inheritance packet

Full transcripts and full DNA remain durable artifacts. A normal fresh-room or Goal baseline receives a compact deterministic package containing only selected state, unresolved work and source digest metadata.

A typical packet may include:
- conversation title/type/completeness;
- current state/core purpose;
- last user intent and unfinished point;
- selected open tasks/next actions/decisions/constraints;
- source digest and authority;
- a marker that full history is not read by default.

Later retrieval loads only the referenced fragment required by the current Goal.

## Externalize large artifacts

Large reports, code snapshots, raw transcripts and evidence should be stored once and later referenced as:

```text
artifact reference + digest + bounded summary
```

They should not be repeatedly injected into active model context.

## Context capacity

Active model context should be governed in provider-native units where possible, not by a universal MB constant. Byte limits can still be used for transport/storage safety.

A Worker Manager should track or estimate:
- physical context capacity if verified;
- current active context usage;
- projected next-checkpoint input;
- reserved output/tool/safety headroom;
- baseline size;
- accumulated delta size;
- externalized artifact size.

When provider capacity is not verifiable, the field remains UNKNOWN rather than being fabricated.

## Rollover

A rollover preserves the same Goal lineage while replacing the worker session. It must persist a checkpoint before creating the next session generation.

```text
goal_id remains constant
session_generation += 1
compact baseline -> hydrate once -> continue deltas
```

Acceptance criteria, source digests, unresolved blockers, Gate state, evidence references, and DAG state must survive compaction.

## DNA contamination controls

Historical context can be wrong or obsolete. A production-quality DNA store should support:
- source attribution;
- explicit target identity;
- timestamps/TTL where appropriate;
- verification status;
- conflict detection against higher-authority state;
- relevance scoring;
- invalidation/supersession;
- bounded injection budgets;
- hydration lineage visible to observability/event tooling.

A worker's own conversational memory is always subordinate to current server/Gate/evidence truth.
