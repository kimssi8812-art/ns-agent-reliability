# Project Timeline — V3 Addendum

> Historical-context note: words such as “current”, “live”, “healthy”, “blocked” or “verified” in dated sections describe the historical snapshot of that section, not the 2026-09-08 public release candidate or current private runtime. Current publication status is defined by the root README, manifest and publication checklist.


This addendum extends `03_PROJECT_TIMELINE.md` from the V2 endpoint into the 2026-08-12 V3 architecture correction without rewriting the earlier historical record.

## 2026-08-11 — Dual-view Control Cockpit design

Observability was separated into two projections over one underlying truth model:

```text
Atomic Machine Event Ledger
  -> Machine Flowboard
  -> Human Cockpit
```

The Machine Flowboard was defined as an atomic operational trace for GPT/N, the Hub and Worker Managers. The Human Cockpit was intentionally constrained to roadmap, verified progress, active actor/model/resource/DNA state, blockers, approvals and next critical action.

A key invariant was established: the Human Cockpit must not maintain a competing truth collector.

## 2026-08-11 — conversation/DNA provider-leakage incident

A conversation ingestion/inheritance workflow exposed a second structural provider-allocation problem beyond cold Goal sessions.

Deterministic infrastructure work such as intake creation, workflow checking, artifact discovery and report verification was routed through a provider worker. Report-schema failures then created retry pressure even after deterministic side effects had already succeeded. Large DNA/history content was also reread to reconstruct continuity.

This incident changed the design target from "reduce provider usage" to a more precise invariant:

> deterministic work should not consume a provider session when a bounded executor/control-plane path can perform it.

## 2026-08-12 — Final Connection Plan V3

V3 preserved the V2 Worker Manager/Goal Session/DAG/resource/model architecture and added four first-class layers:

1. **Bounded Deterministic Executor** for Python/pytest/safe-shell/hash/Git/GitHub/polling work under explicit policy.
2. **Zero-unnecessary-AI DNA** with deterministic intake/registration, explicit target resolution and bounded inheritance packets.
3. **Atomic FlowEvent/Event Ledger** as execution truth for causality, retries, context/resource cost, evidence and Gate lineage.
4. **Machine Flowboard + Human Cockpit** as two projections from one normalized state/event source.

V3 also clarified GPT/N role transition:

```text
construction: architect + integrator + bounded executor user
stabilized:   architect + orchestrator + reviewer + exception handler
mature:       Goal/architecture/judgment layer
```

Repeated GPT/N direct deterministic sequences should be promoted into Hub jobs/adapters as the system stabilizes.

## V3 endpoint

At this addendum's cutoff, the architecture/reference package includes portable contracts for the bounded executor, deterministic DNA inheritance, FlowEvent ledger and dual-view projection, while live deployment acceptance of those features remains a separate implementation/UAT concern.
