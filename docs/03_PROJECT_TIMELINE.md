# Project Timeline — GPT ↔ NS Connection

This timeline records the connection project as an engineering history, including invalidated claims and architecture changes. Dates are KST unless otherwise noted.

## 2026-07-05 — GPT/Claude collaboration contract

An early role document made the limitation explicit: GPT was strong at high-level context, methodology and prioritization but could not directly inspect the server; Claude CLI could inspect and execute but depended on the human/GPT loop for broader interpretation.

This was the starting problem: GPT needed direct, verifiable server awareness without turning the human into a permanent relay.

## 2026-07-08 — first server-side Claude ↔ ChatGPT direct conversation

A Playwright bridge successfully let Claude running on the server send a message to ChatGPT and receive a response without the human copying each turn.

This proved the target interaction pattern — AI workers and GPT could communicate directly — but the transport depended on browser UI automation and authenticated browser-session state.

## 2026-07-10 — shared bridge runtime

The GPT browser bridge became a reusable runtime shared by server worker roles, moving from one-off automation toward infrastructure.

## 2026-07-28 — Playwright bridge hardening and Collab integration

The bridge gained a more persistent browser execution path and a unified launch flow. By this point the project had demonstrated autonomous AI-to-AI exchange, but browser/UI fragility, session state, selector drift and ambiguous authority remained architectural limitations.

These limitations motivated an explicit tool protocol rather than further expanding browser automation.

## 2026-08-03 — objective hardens from tooling to control plane

The objective was reframed from "give GPT some server APIs" to a simple surface experience: the human speaks naturally to GPT, GPT sees current non-secret server state, delegates implementation/review to server workers, verifies results, and stops only at real approval boundaries.

Key consequence: the human is not the routine terminal operator or AI-to-AI relay.

## 2026-08-04 to 2026-08-07 — GitHub/Chat Export/Work integration groundwork

- Chat Exporter work established canonical intake, completeness judgement, human package, and AI DNA package patterns.
- GitHub and server sandboxes were separated from operational SSOT.
- Work connector UAT and Direct Channel dispatch were exercised.
- P8.x work introduced private runtime configuration handling, consumer/tunnel service operation, restart recovery, and bounded worker dispatch.
- The surface interface was explicitly simplified to ordinary General/Work chat rather than special command syntax.

## 2026-08-08 — Direct Channel V2 canonical plan

The canonical V2 plan was written after GPT Work review, Claude objections, human direction, and Gemini review.

The authority stack was fixed conceptually as:

```text
Human Owner
  -> GPT Control Plane
  -> Claude / Codex / Gemini workers
  -> NS Gate / Runtime
```

The plan required modularization, full-baseline inspection before change, safe read roots, secret redaction, sandbox-only GPT writes, bounded task dispatch, and preservation of the existing Gate.

A Context/DNA layer was inserted before orchestration so workers would not start every task without context.

## 2026-08-08 — PHASE 0 architecture freeze

A no-change inventory captured Direct Channel runtime/source structure, tunnel→MCP execution, consumer→runner→provider execution, read/write roots, secret-path denials, worker-health dependencies, Gate/apply chain, Git/PR lineage, and responsibility split between GPT and the server.

The initial runtime had a thin FastMCP server, policy core, bounded consumer, agent bridge, pinned runners, a GPT sandbox write root, and separate worker work areas.

## 2026-08-08 — PHASE 2 through PHASE 11 implementation/test growth

The server-side capability surface grew from 7 tools to 20 across the recorded phases. The PHASE 11 report recorded 8/8 security-negative tests and 14 functional checks.

Negative tests included traversal-write denial, secret-path denial, non-allowed service denial, journal metacharacter rejection, safe process exposure, Git-root restriction, and compare-and-swap mismatch denial.

## 2026-08-08 — P12 General Chat PASS is revoked

An early P12-B document claimed 5/5 General Chat E2E PASS. That judgement was formally retracted because the execution was server-internal rather than an actual ordinary ChatGPT-room E2E.

The human then ran the real path. Findings:

- connection itself worked;
- connector metadata was stale (7 tools displayed while the server served 20);
- GPT generated a relative path and an incorrectly spelled root;
- server policy correctly rejected both bad calls.

This produced a durable rule: a lower-layer test must never be represented as evidence for a higher external boundary.

The client contract was improved so GPT calls control-plane status first, learns current read roots, and uses exact absolute paths.

## 2026-08-09 — Multi-agent and Control Hub expansion

- Multi-Agent Consumer isolation/concurrency work continued.
- Gemini adapter/runtime work established an additional provider path.
- The NS Control Hub was formalized as a non-AI gravity layer with registry, capability routing, context, evidence, Taskboard/lifecycle, Gate state, and resource hooks.
- The human explicitly rejected being the message relay among AIs.

## 2026-08-10 — Context Gravity and centralized control

The project shifted from independent tools toward one gravity/control plane.

Key ideas:

- fresh GPT rooms bootstrap from server state;
- Context Gravity injects bounded task-relevant context;
- Taskboard/evidence/registry state are shared references;
- Direct Channel and Collab are transports/execution mechanisms, not truth authorities;
- GitHub/Linear are external views/integration surfaces, not operational SSOT.

A fail-open path in Context Gravity was identified as incompatible with the desired `CONTEXT_NOT_VERIFIED` fail-closed invariant for core context.

## 2026-08-10 to 2026-08-11 — Runtime Promotion Bridge

A Runtime Promotion Bridge design and sandbox implementation were developed so one human approval could map to a bounded, evidence-producing promotion/rollback operation rather than repeated manual terminal commands.

Negative and E2E sandbox tests passed, while GPT-side tooling continued to distinguish request preparation from actual operational apply authority.

## 2026-08-11 — M3.1 and final architecture correction

Direct Channel source/runtime corrections were promoted and canaried through the controlled path. Context Gravity acceptance evidence existed for the Claude path.

A deeper structural problem then became clear: each Direct Channel worker task could still launch a fresh provider process. Context bundles were cached, but provider conversational/session state was not reused.

This produced the final V2 hierarchy:

```text
Human -> GPT/N -> Control Hub -> Worker Manager -> Goal Session -> checkpoint/evidence
```

## 2026-08-11 — Structural allocation/context leakage diagnosis

Repeated cold provider-process starts and repeated baseline hydration were identified as more important than arbitrary quota ceilings.

Canonical response:

- one Goal = one reusable worker session;
- hydrate baseline once;
- send delta thereafter;
- persist large evidence externally;
- controlled rollover only after checkpoint persistence;
- hard budgets only after structural waste is removed.

## 2026-08-11 — Codex SESSION_DEAD root cause

Direct Channel Codex readiness was coupled to legacy `codex_collab` tmux health, while legacy auto-sleep could kill that session after a different Collab inbox became idle. Direct Channel requests did not wake through that inbox path before preflight, creating a circular deadlock:

```text
idle -> auto-sleep + tmux stop
-> Direct Channel health reports SESSION_DEAD
-> dispatch blocked
-> Direct Channel cannot create the activity that wakes the legacy path
-> fallback pressure moves toward Claude
```

A persisted quota latch was a separate signal and had to be treated independently from liveness/readiness.

## 2026-08-11 — Plan-wide scaffold

GPT/N became not only the orchestration layer but the Lead Architect + Reference Implementation Owner.

A non-SSOT scaffold was generated for Goal/DAG, WorkerManager, GoalSession, context policy/store, progress/critical path, evidence/taskboard/Gate bridges, resource telemetry, provider adapters, health normalization, recovery/watchdog, model/runtime/version governance, and UAT/acceptance.

Workers are expected to compare, adapt, implement, test and challenge this common contract rather than redesigning the architecture from scratch.

## 2026-08-11 — Stage 0 health collector R1/R2/R3 review

A worker-produced health collector initially self-tested successfully but contained semantic mismatches. GPT/N review caught, over successive rounds:

- wrong persisted JSON shape assumption;
- wrong stale timestamp field;
- neutral signals incorrectly returning allow;
- tmux socket UID mismatch;
- false scaffold-schema compatibility;
- liveness incorrectly capable of implying dispatch readiness.

By R3, the key invariant was explicit:

```text
LIVENESS != READINESS != DISPATCH_ALLOWED
```

The worker saved an R3-corrected source before its provider allocation limit interrupted final closure testing/reporting.

## Historical endpoint snapshot — 2026-08-12

At the end of the 2026-08-12 historical snapshot below (not current runtime status):

- Direct Channel transport/services are healthy;
- Claude path is live;
- Codex Direct Channel dispatch remains blocked by session/readiness state despite newer human evidence that provider allocation is available;
- Gemini is not yet a verified normal Direct Channel path;
- Worker Manager/Goal Session is scaffolded but not operationally complete;
- model/runtime/version governance is scaffolded;
- final multi-agent acceptance and public GitHub publication are still pending.
