# Genesis and Objective

> Historical-context note: words such as “current”, “live”, “healthy”, “blocked” or “verified” in dated sections describe the historical snapshot of that section, not the 2026-09-08 public release candidate or current private runtime. Current publication status is defined by the root README, manifest and publication checklist.


## Problem statement

Private server automation becomes fragile when a human must manually relay context among ChatGPT, terminal sessions, Claude/Codex/Gemini CLIs, GitHub, and an operational Gate. It also becomes expensive when every worker task starts as a cold process and rereads the same history.

This project therefore treats the conversational AI as a top-level intent/control surface rather than a thin chat client.

## Target surface experience

A normal interaction should look like:

```text
Human: "Check why the service is failing, fix it, verify it, and prepare deployment."

GPT/N:
  1. verifies live control-plane connectivity;
  2. reconstructs current server context;
  3. creates or recovers the Goal;
  4. selects an eligible worker/runtime/model;
  5. creates or reuses the Goal Session;
  6. delegates bounded checkpoints;
  7. verifies evidence;
  8. updates Goal/Taskboard/progress;
  9. stops only if an operational approval is required.
```

The human should not be required to:

- know MCP tool names;
- invent task IDs;
- launch provider CLI sessions;
- copy worker output back to GPT;
- repeatedly paste project history;
- execute routine shell commands;
- manage context window sizes or provider model menus manually.

## Authority model

```text
Human Owner
  -> GPT/N Control Plane
  -> NS Control Hub
  -> Worker Managers
  -> Goal Sessions (Claude/Codex/Gemini)
  -> evidence/results

Operational mutation:
  verified candidate -> Gate -> runtime/SSOT
```

GPT/N is an evidence integrator and orchestration authority, not a bypass around the server's operational controls.

## Design philosophy

The project evolved around five principles:

1. **Evidence over conversational confidence.** A PASS requires direct evidence appropriate to the claim.
2. **State outside the model.** Taskboard, evidence, Goal state, source digests, and Gate state live on the server so a fresh chat can recover them.
3. **Continuity over cold starts.** One Goal should reuse one worker session and send deltas instead of replaying the full baseline.
4. **Resource-aware routing.** Provider, model, version, reasoning profile, context capacity, and quota pressure are scheduling inputs.
5. **Explicit authority boundaries.** Read/observe/sandbox work can be autonomous; operational change remains separately gated.

## Non-goals

The open-source core is not intended to:

- expose arbitrary shell execution to ChatGPT;
- publish credentials or private server topology;
- make a model the production SSOT;
- silently turn a sandbox write into a production apply;
- guarantee provider quota values that cannot be directly observed;
- force one provider or model for all workloads.
