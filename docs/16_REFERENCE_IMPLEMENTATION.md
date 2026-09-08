# Reference Implementation Guide

> Historical-context note: words such as “current”, “live”, “healthy”, “blocked” or “verified” in dated sections describe the historical snapshot of that section, not the 2026-09-08 public release candidate or current private runtime. Current publication status is defined by the root README, manifest and publication checklist.


The `src/ns_agent_reliability` package is intentionally provider-neutral. It is a design/reference layer, not the private runtime copied into public source.

## Modules

- `contracts.py` — Goal, Session, resource and WorkerManager contracts.
- `health.py` — normalized multi-source health semantics; liveness alone cannot authorize dispatch.
- `context.py` — reference keep/externalize/compact/rollover decision policy.
- `sessions.py` — one-active-session-per-Goal registry and controlled generation rollover.
- `progress.py` — evidence-weighted progress and dependency-ready nodes.
- `routing.py` — warm Goal affinity + capability/readiness/load routing.
- `model_governance.py` — execution profile registry/selection and canary-promotion guard.
- `lifecycle.py` — result verification/acknowledgement/consumption state machine.
- `ports.py` — deployment adapters for evidence, Goal/session storage, Taskboard, Gate, runtime inventory and mirrors.
- `telemetry.py` — normalized non-SSOT telemetry event format.
- `executor.py` — bounded deterministic-executor policy/request validation; deliberately not an unrestricted shell implementation.
- `dna.py` — deterministic Chat-share intent classification and bounded inheritance-packet reference logic.
- `observability.py` — FlowEvent ledger, MachineFlowboardSnapshot, HumanCockpitSnapshot and projection/causality invariants.
- `hub.py` — minimal assembly example.

## What a real deployment must provide

A deployment should implement adapters for its own:
- MCP/transport layer;
- durable databases/files/queues;
- bounded deterministic process executor;
- provider CLI/API runtimes;
- auth/readiness/quota signals;
- context/token estimators;
- DNA/transcript store and explicit target registry;
- evidence storage;
- Atomic Event Ledger persistence/reducers;
- Machine/Human view APIs or UI adapters;
- operational Gate;
- process/service telemetry.

## Bounded executor note

The public reference only validates executor requests against policy. It intentionally does not publish a generic arbitrary-command runner as the architecture itself. A deployment must decide its command allow classes, root/write policy, time/output caps, secret boundary and privileged Gate integration.

The important contract is:

```text
deterministic bounded work -> executor
model reasoning required -> Worker Manager
privileged/operational mutation -> Gate
```

## DNA note

The public reference treats ordinary Chat-share ingestion/inheritance as deterministic control-plane work by default. Full transcript/full DNA remain external artifacts; active context uses explicit bounded references/packets. A deployment may add semantic enrichment, but that is optional and independently budgeted.

## Observability note

The reference dual-view model follows:

```text
FlowEvent / normalized state
 -> MachineFlowboardSnapshot
 -> HumanCockpitSnapshot projection
```

A real Human Cockpit should never establish a competing truth store. Detailed machine state may be reduced/summarized for the human view, but it must retain lineage to the same underlying evidence/events.

## No provider assumptions

The public reference does not encode private model IDs, installed CLI flags, account plans, or context-window claims. Provider adapters discover and verify those facts in the target environment.

## Test philosophy

The included tests focus on invariants discovered during private development:
- alive is not dispatchable by itself;
- running work does not add verified progress;
- warm Goal Session affinity is preserved;
- valid execution profile remains pinned;
- unknown context capacity remains unknown;
- only one active session is bound to a Goal;
- rollover preserves Goal lineage and increments generation;
- a result cannot become `RESULT_VERIFIED` without evidence metadata;
- deterministic DNA intents do not require a provider by default;
- bounded executor policy blocks sudo/SSOT authority escalation;
- inheritance packets remain bounded and do not default to full history;
- Human Cockpit state is projected from machine state;
- event sequence/causality invariants are enforceable.

A real implementation should add integration tests for its own transport, executor, provider sessions, DNA pipeline, event persistence, Gate and UI layers.
