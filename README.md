# NS Agent Reliability Doctor

Find reliability and control-plane failure patterns in agent/MCP systems before they become repeated production incidents.

> Status: 0.1.0rc1 RELEASE CANDIDATE  
> First public wedge: Agent Reliability Doctor  
> Runtime/reference scope: portable diagnostics, regressions and reliability/control-plane contracts; not a production-ready full agent framework.

## 60-second first value

Python 3.11+ is required.

```bash
git clone https://github.com/kimssi8812-art/ns-agent-reliability.git
cd ns-agent-reliability
python -m pip install .
ns-reliability examples/doctor_broken_system.json
```

Expected shape of the result:

```text
Agent Reliability Doctor: 15 finding(s)
[HIGH] STALE_OWNERSHIP
[CRITICAL] DUPLICATE_AUTHORITY
[HIGH] UNBOUNDED_RETRY
[HIGH] RETRY_LINEAGE_CORRUPTION
[HIGH] CONTEXT_RESUME_DEFECT
[MEDIUM] EXCESSIVE_PUBLIC_TOOL_SURFACE
[HIGH] STALE_CLIENT_SERVER_SCHEMA
[CRITICAL] AUTHORITY_LEAKAGE
[HIGH] EVIDENCE_GAP
[HIGH] DUPLICATE_REDISPATCH
[HIGH] STALE_DEPENDENCY_PIN
[CRITICAL] SELF_LOCKING_DEPLOY_BOUNDARY
[CRITICAL] ROLLBACK_RESURRECTS_DEPRECATED_SURFACE
[MEDIUM] OBSERVABILITY_COUPLED_TO_EXECUTION
[HIGH] HISTORICAL_STATE_CURRENT_AUTHORITY
```

JSON output:

```bash
ns-reliability examples/doctor_broken_system.json --json
```

The Doctor only fires a rule when the supplied snapshot contains matching evidence. Missing fields remain unknown rather than being silently treated as healthy.

## What the Doctor checks

The current rule set is derived from real reliability incidents and regression work in a long-running multi-agent system. It includes:

- stale ownership and fencing defects;
- duplicate mutation authority;
- unbounded retry and corrupted retry lineage;
- broken durable-resume assumptions;
- excessive MCP/tool-surface growth;
- stale client/server schemas;
- read/write authority leakage;
- mutation without result evidence;
- redispatch of already-completed work;
- stale dependency pins and self-locking deploy boundaries;
- rollback that resurrects deprecated surfaces;
- observability coupled to execution;
- historical state accidentally regaining current authority.

The goal is not to replace LangGraph, CrewAI, AutoGen, MCP runtimes, observability platforms or security scanners. The Doctor is a reliability/control diagnostic layer that can be used alongside existing stacks.

## Why this exists

The project grew out of repeated operational failures in a real multi-agent control system. Several failures generalized into portable invariants:

```text
client session lifecycle != mutation lease lifecycle

released/expired lease -> reacquire with a newer fencing epoch
stale holder/epoch      -> reject
```

```text
build once
-> verify once
-> candidate + evidence binding
-> expected-live CAS
-> one atomic commit
-> smoke
-> PASS or rollback once
```

```text
capability-per-tool surface
83 public tools
-> 26
-> 7 stable authority-class primitives
-> future capability growth through bounded action/payload contracts
```

The public value is the failure class, diagnostic, reproduction, regression and remediation pattern—not private production infrastructure.

## Current portable evidence

### Lease/session independence

`src/ns_agent_reliability/leases.py` models lease ownership independently from client-session liveness and advances a monotonic fencing epoch on every successful reacquire.

Regression coverage includes:

- released lease can be reacquired while the old client session remains alive;
- active foreign lease cannot be stolen;
- expired lease can be reacquired;
- stale holders are rejected after a newer epoch is acquired;
- checkpoint-safe completion releases ownership without waiting for TTL expiry.

See `tests/test_lease_session_independence.py` and `incidents/released-lease-live-session.md`.

### One live commit

`src/ns_agent_reliability/deployment.py` contains a portable deployment primitive covering:

- expected-live SHA/CAS protection;
- candidate/evidence digest binding;
- zero mutation on failed preconditions;
- byte-exact rollback point;
- one rollback after smoke failure;
- failed-candidate replay denial.

See `tests/test_one_live_commit.py` and `incidents/one-live-commit-gate.md`.

### Reliability Doctor

`src/ns_agent_reliability/doctor.py` currently diagnoses 15 reliability/control failure classes from normalized evidence JSON.

See `examples/doctor_broken_system.json` and `tests/test_doctor.py`.

## Important maturity boundary

This repository contains both portable code and historical/reference architecture material. They are not all at the same maturity level.

**Proven portable components in the current candidate:**

- Reliability Doctor rules over normalized evidence;
- lease/session independence and fencing reference behavior;
- one-live-commit deployment primitive and regressions.

**Reference/scaffold or partially portable areas:**

- broader Worker/Run orchestration;
- event-ledger and dashboard projections;
- provider governance;
- context/DNA continuity architecture;
- full durable runtime persistence.

For example, the current public `LeaseRegistry` is an in-memory reference implementation of ownership/fencing semantics. It must not be described as a complete durable persistent workflow runtime.

## Repository map

```text
ns-agent-reliability/
├── README.md
├── pyproject.toml
├── examples/
│   ├── doctor_broken_system.json
│   └── config.example.json
├── src/ns_agent_reliability/
│   ├── doctor.py
│   ├── leases.py
│   ├── deployment.py
│   ├── observability.py
│   └── ...
├── tests/
│   ├── test_doctor.py
│   ├── test_lease_session_independence.py
│   ├── test_one_live_commit.py
│   └── ...
├── incidents/
│   ├── released-lease-live-session.md
│   ├── one-live-commit-gate.md
│   └── checkpoint-complete-lease-release.md
├── docs/
├── schemas/
├── SECURITY.md
├── CONTRIBUTING.md
└── PUBLICATION_CHECKLIST.md
```

## Design principles

1. Unknown is not PASS.
2. Worker self-report is not completion evidence.
3. Read authority and mutation authority stay distinct.
4. Historical state is searchable evidence, not automatic current authority.
5. Retry is bounded and terminal states are explicit.
6. A stale fencing epoch cannot mutate current state.
7. Observability should be fail-soft unless it is itself a required safety input.
8. Rollback must not resurrect an obsolete public surface.
9. Existing capabilities are collapsed/reused before new control layers are added.
10. Reliability controls should protect actual mutation boundaries without becoming universal work-start dependencies.

## Historical architecture material

The repository also preserves the evolution from human-relayed AI work through Direct Channel, bounded deterministic execution, reusable sessions, context continuity, evidence-weighted progress and control-plane simplification. That material is retained as case-study/reference context under `docs/` and `architecture/`.

It should not be mistaken for a claim that every historical subsystem is part of the first public product surface.

## Security and publication boundary

Public release must not contain:

- credentials, tokens, cookies or private keys;
- private remote URLs or account identifiers;
- raw private conversation exports;
- private deployment paths;
- production Trading/financial logic or state;
- unredacted production logs.

Run the publication scrub before release:

```bash
python tools/prepublish_check.py
```

This repository remains a publication candidate until the Doctor-inclusive tracked tree passes clean install/smoke and scrub checks, the final open-source license/provenance metadata is applied, and the target public repository is explicitly selected and verified.

## Commercial boundary

The Apache-2.0-licensed Doctor candidate and regressions are intended to remain useful without paid services. Separate commercial services may include bounded MCP/control-surface audits, agent reliability audits and implementation hardening. Paid work is not required to use the public diagnostic core.


## Licensing

- Software, tests, schemas and executable examples: **Apache-2.0**.
- Original narrative documentation and incident write-ups: **CC BY 4.0**.
- NS names/logos/distinctive brand assets: not granted under those licenses.
- Third-party names remain the property of their respective owners.

See `LICENSE`, `LICENSE_POLICY.md`, `NOTICE`, `THIRD_PARTY_NOTICES.md` and `TRADEMARKS.md`. The repository is still a prepublication release candidate until a public GitHub remote is pushed and verified.
