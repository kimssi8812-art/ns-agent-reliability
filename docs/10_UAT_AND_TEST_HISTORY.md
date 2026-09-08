# UAT and Test History

> Historical-context note: words such as “current”, “live”, “healthy”, “blocked” or “verified” in dated sections describe the historical snapshot of that section, not the 2026-09-08 public release candidate or current private runtime. Current publication status is defined by the root README, manifest and publication checklist.


## Why this history is preserved

A multi-layer control plane can produce false confidence if internal unit tests are confused with external end-to-end evidence. This project therefore preserves both successful tests and invalidated PASS judgements.

## PHASE 11 recorded security-negative tests

The 2026-08-08 PHASE 11 report recorded 8/8 PASS for negative cases covering:

- traversal write rejection;
- secret path denial;
- `/etc`/outside-root denial;
- non-NS service denial;
- journal metacharacter rejection;
- bounded safe process status;
- Git path outside allowed roots;
- compare-and-swap SHA mismatch.

The same report recorded functional PASS for safe service/journal/process/Git observation, sandbox writes, worker health/pre-dispatch checks, baseline/immutable/path-policy checks, security audit, and aggregate control-plane status.

## Tool-surface progression

The historical PHASE 11 report recorded a server-side progression from 7 initial tools to 20 by PHASE 9.

This number is historical evidence, not a permanent compatibility requirement.

## The revoked P12-B PASS

An initial P12-B document labelled five scenarios as General Chat E2E PASS. It was later formally revoked because the execution context was server-internal rather than an actual ordinary ChatGPT room.

The real external test showed:

- connection: PASS;
- connector UI metadata freshness: FAIL/stale;
- path argument generation: FAIL on two calls;
- server path-policy enforcement: PASS.

This distinction is important: a client generated invalid paths, while the server correctly refused them.

## Lessons from the retraction

A valid external UAT must record the actual boundary being tested. Examples:

```text
ChatGPT ordinary room -> connector -> tunnel -> MCP server -> tool -> response
ChatGPT Work -> connector -> Direct Channel -> worker -> report -> GPT
Hub -> Worker Manager -> reusable Goal Session -> checkpoint 1 -> checkpoint 2
Gate approval -> bounded promotion -> canary -> evidence
```

A lower-layer test cannot substitute for a higher-layer acceptance.

## Required final acceptance families

The target system should eventually prove:

1. fresh ordinary-chat bootstrap from server state;
2. fresh Work-room bootstrap;
3. safe broad non-secret observation;
4. same Goal, same verified worker session, multiple checkpoints;
5. baseline once and delta thereafter;
6. Claude plus at least one non-Claude normal path;
7. result -> evidence -> Taskboard/DAG consume without human relay;
8. evidence-weighted progress and resource telemetry;
9. provider failure/recovery without blind retries;
10. Gate/secret/authority negative regressions;
11. model/runtime canary and rollback;
12. tunnel/service recovery.

## Evidence labels

Recommended test-result labels:

- `PASS_VERIFIED` — correct boundary and evidence verified;
- `FAIL_VERIFIED` — failure directly reproduced;
- `REVOKED` — prior judgement invalidated by stronger evidence;
- `PARTIAL` — some layers proven, final boundary incomplete;
- `NOT_RUN` — no execution evidence;
- `UNKNOWN` — evidence unavailable or stale.

A historical `REVOKED` result should remain visible instead of being rewritten as though it never happened.
