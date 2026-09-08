# Current Status and Roadmap

> Historical-context note: words such as “current”, “live”, “healthy”, “blocked” or “verified” in dated sections describe the historical snapshot of that section, not the 2026-09-08 public release candidate or current private runtime. Current publication status is defined by the root README, manifest and publication checklist.


Historical cutoff: 2026-08-12.

## Verified/strong evidence from the private project history

- Direct Channel consumer/tunnel supervision exists and safe server observation works through the boundary.
- GPT sandbox writes can be isolated from operational SSOT.
- Secret/path policies have negative-test coverage.
- Context/DNA continuity, Goal/Session and resource/model governance have plan-wide reference scaffolding.
- a bounded promotion/rollback path exists in the private project history.
- a dual-view observability design and portable FlowEvent projection skeleton exist.
- deterministic DNA-ingestion/inheritance candidate code and regression tests exist in sandbox/reference form.

These statements do not imply every item is live in a production runtime.

## Partial/scaffolded

- bounded Deterministic Executor policy/reference exists, but final chat-accessible executor integration is not yet accepted.
- zero-unnecessary-AI DNA candidate logic exists, but the full runtime share -> export -> sync -> bounded inheritance route requires UAT.
- Worker Manager/Goal Session contract is scaffolded but not yet the universal live execution authority.
- Goal DAG/progress/resource modules are scaffolded rather than fully operational.
- model/runtime/version governance is scaffolded but not fully wired to live provider inventory.
- Atomic Event Ledger and Machine/Human snapshot contracts exist, but the complete durable ledger/reducers/dashboard are not final live features.
- result -> evidence -> Taskboard/DAG consume lifecycle is not fully closed.

## Known degraded/blocked themes at the cutoff

- at least one provider Direct Channel path has historically been unavailable because health/session semantics were coupled to a legacy session lifecycle;
- normal multi-provider routing is not at final acceptance;
- deterministic work can still be forced through provider paths until a bounded Direct Executor is exposed end-to-end;
- provider quota/resource signals may remain UNKNOWN unless directly observable.

## V3 priority roadmap

### P0 — bounded Direct Executor + DNA leakage closure

Expose a constrained execution capability for Python/pytest/safe-shell/hash/Git/GitHub/polling. Enforce roots, timeout/output caps, write authority, secret denial and Gate separation. Then run the deterministic DNA regression suite and prove ordinary chat-share ingestion/inheritance completes without provider calls when semantic enrichment is not requested.

Acceptance also requires explicit DNA targeting and no default full-transcript/full-DNA replay.

### P1 — Worker Manager + Goal Session

Implement/finish the common manager contract and durable Goal Session registry. Prove two checkpoints in the same Goal reuse the same verified provider session with baseline-once/delta-only semantics where the provider runtime supports reuse.

### P2 — multi-provider readiness and routing

Normalize liveness/readiness/auth/quota/session scope independently. Prove at least two provider paths for semantic work and avoid silent single-provider normal mode. Route deterministic checkpoints to the executor and semantic checkpoints to eligible providers.

### P3 — Goal DAG + evidence lifecycle

Operationalize fixed acceptance weights, evidence verification, Taskboard/DAG consumption, progress/coverage/critical-path/blocked-weight calculation and automatic next-checkpoint selection.

### P4 — resource/context/model governance

Feed executor/worker/session context and resource telemetry into routing. Track repeated reads, cold-start/switch costs, quota provenance and model/runtime/profile identity. Govern new execution profiles through compatibility checks and canary/promotion/rollback.

### P5 — Atomic Event Ledger + Machine Flowboard

Instrument execution transitions into normalized FlowEvents. Persist a bounded/durable ledger and reducers, preserve causality/correlation, distinguish session scopes, and support incident replay without broad log rereads. Build the detailed machine operational projection.

### P6 — Human Cockpit

Derive a mobile-first human snapshot from the exact same machine truth. Show roadmap, verified progress, active work, model/resource/DNA summary, blocker, next critical action, evidence/approval status and system health. Do not create a second collector.

### P7 — external mirrors and full UAT

Keep systems such as Linear optional/non-authoritative. Prove fresh ordinary-chat and Work bootstrap, private Git path, zero-unnecessary-AI Chat Export/DNA path, multi-provider semantic execution, security/Gate regressions, recovery and event-based incident reconstruction.

### P8 — final acceptance and progressive GPT/N direct-work reduction

Final acceptance requires:
- deterministic work does not unnecessarily consume provider sessions;
- reusable Goal Sessions and delta context;
- evidence-driven lifecycle and progress;
- multi-provider semantic routing without silent monopoly;
- one event truth feeding both machine and human projections;
- fresh-room continuity;
- correct secret/Gate behavior;
- zero routine human relay.

After acceptance, repeated direct GPT/N executor sequences should be promoted into Hub jobs/adapters and direct-run frequency should decline, while diagnostic/exception access remains available.

## Definition of done

The system is complete when a human can open a fresh ordinary ChatGPT/Work conversation, state a Goal naturally, and the control plane can recover live state, select deterministic execution or an appropriate worker/runtime/model, create or reuse Goal Sessions, use bounded context, verify evidence, update progress, emit causal execution events, project detailed and simplified views from one truth model, recover from failures, and stop only at a real human/Gate boundary.
