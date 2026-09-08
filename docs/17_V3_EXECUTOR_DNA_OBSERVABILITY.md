# V3: Deterministic Executor, DNA Continuity, and Dual-View Observability

> Historical-context note: words such as “current”, “live”, “healthy”, “blocked” or “verified” in dated sections describe the historical snapshot of that section, not the 2026-09-08 public release candidate or current private runtime. Current publication status is defined by the root README, manifest and publication checklist.


Status: publication-candidate design/reference contract. These concepts may exist at different implementation maturities in a private deployment; this document does not claim production acceptance.

## Why V3 was needed

The V2 architecture already addressed repeated cold provider sessions, baseline replay, Worker Manager/session continuity, Goal DAG progress, and resource-aware routing. A later failure pattern exposed a deeper gap: some deterministic infrastructure work still reached a provider simply because GPT/N had no direct bounded executor path.

Examples include:
- running pytest;
- computing/checking hashes;
- locating known artifacts;
- polling workflow state;
- creating an idempotent conversation-intake record;
- registering a generated DNA artifact;
- checking deterministic report state.

If these jobs wake a model, provider allocation can be consumed without any semantic reasoning benefit. Worse, a report-format failure may trigger another provider call even though the underlying infrastructure side effect already succeeded.

V3 therefore distinguishes **deterministic execution** from **provider reasoning** before worker selection.

## Bounded Deterministic Executor

The executor is a capability below the Control Hub, alongside provider Worker Managers.

```text
Control Hub
  +--> Deterministic Executor
  |      +-- Python
  |      +-- pytest/test runner
  |      +-- bounded shell
  |      +-- hash/stat
  |      +-- Git/GitHub metadata
  |      +-- polling/filesystem operations
  |
  +--> Claude Worker Manager
  +--> Codex Worker Manager
  +--> Gemini Worker Manager
```

A safe executor request should carry:
- run identifier;
- Goal/checkpoint correlation;
- command class;
- approved working root;
- write scope;
- timeout;
- maximum captured output;
- authority;
- expected evidence/result contract.

It is explicitly **not** an unrestricted root shell. Secret reads, arbitrary sudo, direct SSOT/production mutation, authority bypass and unbounded output remain forbidden.

Operational changes still cross the Gate.

## Routing rule

The Hub should decide in this order:

1. authority/security boundary;
2. deterministic vs model-reasoning requirement;
3. deterministic bounded work -> executor;
4. semantic/code/analysis work -> eligible provider Worker Manager;
5. warm Goal Session affinity;
6. capability/resource/context/quota/reliability state;
7. runtime/model/profile compatibility and switch cost.

This prevents `pytest` or `sha256` from becoming accidental Claude/Codex/Gemini workloads.

## Zero-unnecessary-AI DNA

Conversation DNA is durable context, not an excuse to replay entire history into every new model session.

Canonical path:

```text
share URL
 -> deterministic intake
 -> transcript extraction
 -> completeness verification
 -> deterministic compiler/package
 -> DNA registry/index
 -> bounded inheritance packet/reference
 -> Goal/new-room baseline
 -> later deltas
```

Infrastructure-only steps should not require a provider session:
- intake creation;
- workflow polling;
- artifact discovery;
- hash verification;
- completeness metadata reads;
- DNA registration;
- ordinary inheritance.

A model may still be used for optional semantic enrichment, but enrichment is explicit, budgeted, and non-authoritative relative to extraction/completeness truth.

## Explicit DNA target

Selecting "the newest DNA directory" is unsafe when multiple conversations exist. Inherited context should be tied to an explicit conversation identifier, Goal relation, or verified registry reference. Ambiguity should fail closed rather than silently hydrating unrelated history.

## Bounded inheritance packet

Full transcript and full DNA remain external artifacts. The active baseline normally receives only a compact package such as:
- title/type/completeness;
- core purpose/current state;
- last user intent/unfinished point;
- selected unresolved work and decisions;
- source digest and authority.

Later lookups retrieve only the specific referenced fragment needed for the current Goal.

## Atomic Machine Event Ledger

V3 also promotes observability from a dashboard concern to a control-plane invariant.

Every meaningful transition should emit a normalized `FlowEvent` with enough identity and causality to reconstruct execution:
- project/Goal/node/checkpoint/task/run/session;
- provider or deterministic executor identity;
- runtime/model/profile where applicable;
- previous/next state;
- trigger/failure/retry;
- context baseline/delta lineage;
- resource/usage provenance when observable;
- evidence/artifact references;
- Gate/source digest lineage;
- correlation and causation identifiers.

A state transition without a corresponding event becomes an observability defect once that subsystem is instrumented.

## One truth, two projections

```text
normalized FlowEvents + durable state
        |
        v
   reducers/snapshots
      /          \
     v            v
Machine          Human
Flowboard        Cockpit
```

### Machine Flowboard

Designed for GPT/N, the Hub, Worker Managers and engineering diagnosis. It exposes:
- actual Goal/DAG/checkpoint execution graph;
- executor vs provider routing decision;
- queue/claim/lease/heartbeat/retry details;
- manual/direct-channel/collab/Goal-session scopes separately;
- session reuse/rollover/context lineage;
- routing exclusions and selected runtime/model/profile;
- evidence verification and Taskboard consumption;
- Gate/promotion/rollback lineage;
- event cursor replay for incident reconstruction.

### Human Cockpit

Designed for fast human understanding and approval:
- current objective/roadmap;
- verified progress and critical path;
- active actor/Goal/checkpoint/model;
- resource/token/context summary with provenance;
- DNA/session generation summary;
- blocker and next critical action;
- evidence/approval status;
- system health/degraded state.

The Human Cockpit must not collect separate operational truth. It is a simplified projection of machine state.

## Progressive GPT/N role reduction

Direct executor access is most valuable during construction and stabilization because it keeps the design-test-fix loop continuous without unnecessary provider hops.

The mature architecture should gradually move repeated deterministic procedures into Hub jobs/adapters:

```text
construction:
GPT/N = architect + integrator + bounded executor user

stabilized:
GPT/N = architect + orchestrator + reviewer + exception handler

mature:
GPT/N = Goal/architecture/judgment layer
Hub = routine orchestration
Executor = deterministic automation
Workers = specialized model reasoning/execution
Human = intent/approval boundary
```

The goal is not to remove GPT/N's ability to intervene; it is to reduce routine direct execution as proven automation grows.
