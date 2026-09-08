# Architecture Evolution

> Historical-context note: words such as “current”, “live”, “healthy”, “blocked” or “verified” in dated sections describe the historical snapshot of that section, not the 2026-09-08 public release candidate or current private runtime. Current publication status is defined by the root README, manifest and publication checklist.


## Generation 0 — chat + manual relay

The human coordinated separate tools and worker sessions manually. Context lived primarily in conversations and terminal sessions. This was hard to resume and encouraged duplicated work.

## Generation 1 — Direct Channel as a safe MCP bridge

A server-side MCP service exposed capability-oriented tools rather than unrestricted remote control.

Core boundary:

```text
ChatGPT/Work
  -> secure MCP tunnel
  -> Direct Channel server
     -> safe read tools
     -> GPT sandbox writes
     -> bounded agent dispatch
     -> Gate request preparation
```

The server enforced read roots, secret-path denial, NS-service filtering, bounded journal/process views, sandbox-only writes, and pinned worker runner contracts.

## Generation 2 — Multi-agent dispatch

Claude and Codex runners were added behind a bounded consumer. Gemini support followed through separate adapter work.

This solved transport and isolation, but worker lifecycle was still largely provider-specific and cold per task.

## Generation 3 — Context/DNA and Context Gravity

Repeated context replay became a measurable cost. The system introduced structured Context/DNA references and a bounded Context Gravity bundle.

Important hierarchy:

```text
Human/current instruction
  > operational/Gate truth
  > Taskboard/Goal state
  > verified evidence
  > relevant DNA/context
  > worker-local conversational memory
```

Raw terminal capture was rejected as a default memory mechanism because it mixes UI/log noise with useful state.

## Generation 4 — NS Control Hub

The system was re-centered around a non-AI Hub rather than direct GPT-to-runner branching.

Hub responsibilities:
- system/worker registry;
- Goal/DAG state;
- Taskboard lifecycle;
- evidence/truth references;
- capability routing;
- resource telemetry;
- context index;
- Gate state;
- failure/learning ledger;
- external mirrors.

Direct Channel became a transport/inspection/dispatch port of the Hub rather than the whole architecture.

## Generation 5 — Worker Manager + Goal Session

A structural token leak was identified: Direct Channel runner tasks could launch fresh provider processes even when the logical Goal had not changed.

The architecture inserted an explicit Worker Manager tier:

```text
Control Hub
  -> Claude Manager
  -> Codex Manager
  -> Gemini Manager
       -> Goal Session
          -> checkpoint 1
          -> checkpoint 2
          -> checkpoint N
```

The Worker Manager owns provider-specific auth/readiness, session create/reuse/rollover, context accounting, runtime health, and recovery.

## Generation 6 — Goal DAG, progress and resource control

Task count was rejected as a progress metric because unequal tasks make percentages misleading.

Canonical progress:

```text
verified acceptance weight / total acceptance weight
```

Separate views track evidence coverage, critical-path progress, blocked weight, worker load, session/context growth, retries, and resource signals.

## Generation 7 — Provider model/runtime/version governance

Worker selection alone is insufficient because each provider can expose multiple models, CLI versions, reasoning profiles, context capacities, tool capabilities, and usage states.

The routing hierarchy therefore becomes:

```text
Goal/Checkpoint
  -> Provider
  -> Runtime/CLI version
  -> Model
  -> reasoning/tool profile
  -> Goal Session
```

A running Goal Session should remain pinned to a verified execution profile unless a controlled rollover is required. New versions/models are discovered and canaried before promotion.

## Generation 8 — bounded Deterministic Executor

A later failure pattern showed that deterministic work could still consume provider allocation simply because GPT/N had no direct bounded execution path.

The Hub execution domain expanded:

```text
Control Hub
  -> Deterministic Executor
       -> Python / pytest / bounded shell / hash / Git / polling
  -> Provider Worker Managers
```

The executor is policy-bounded and does not imply root/SSOT authority. Privileged operational mutation remains behind the Gate.

## Generation 9 — zero-unnecessary-AI DNA continuity

Conversation ingestion and ordinary inheritance were reclassified as deterministic control-plane responsibilities by default.

```text
share reference
 -> deterministic intake/extraction/completeness/package
 -> DNA registry
 -> explicit bounded inheritance packet/reference
 -> Goal/new-room baseline
```

Full transcript/full DNA remain durable artifacts rather than default active context. Provider reasoning is optional enrichment, not infrastructure glue.

## Generation 10 — Atomic Event Ledger + dual projection

Observability moved from a dashboard feature to a control-plane invariant.

```text
Hub / Executor / WorkerManagers / Evidence / Gate
  -> normalized FlowEvent
  -> bounded Event Ledger
  -> reducers
      -> Machine Flowboard
      -> Human Cockpit
```

The Machine Flowboard preserves atomic operational detail for GPT/N and engineering diagnosis. The Human Cockpit is a smaller decision/approval projection for the human owner. It may not maintain a separate truth collector.

## Generation 11 — progressive GPT/N execution reduction

During construction, GPT/N can use the bounded executor directly to keep design/test/fix loops continuous. Repeated deterministic sequences are then promoted into Hub jobs/adapters.

The long-term role transition is:

```text
build:       GPT/N = architect + integrator + bounded executor user
stabilized:  GPT/N = architect + orchestrator + reviewer + exception handler
mature:      GPT/N = Goal/architecture/judgment layer
             Hub = routine orchestration
             Executor = deterministic automation
             Workers = specialized model reasoning
```

## Target architecture

```text
Human
  |
  v
GPT/N Architecture + Judgment
  |
  v
NS Control Hub
  |-- Goal Registry / DAG / Scheduler
  |-- Evidence / Taskboard / Progress
  |-- Context/DNA index
  |-- Resource & Model Registry
  |-- Atomic Event Ledger / reducers
  |-- Gate state / Authority Router
  |
  +--> Bounded Deterministic Executor
  +--> Worker Manager: Claude -> Goal Session(s)
  +--> Worker Manager: Codex  -> Goal Session(s)
  +--> Worker Manager: Gemini -> Goal Session(s)
  |
  +--> Machine Flowboard
  +--> Human Cockpit projection

Ports:
  Direct Channel / Collab / Git / Chat Export / Linear mirror / Gate
```
