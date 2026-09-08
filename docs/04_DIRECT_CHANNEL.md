# Direct Channel

> Historical-context note: words such as “current”, “live”, “healthy”, “blocked” or “verified” in dated sections describe the historical snapshot of that section, not the 2026-09-08 public release candidate or current private runtime. Current publication status is defined by the root README, manifest and publication checklist.


## Purpose

Direct Channel is the safe server bridge between ChatGPT/Work and the private NS environment. It is designed around capabilities, not arbitrary remote shell access.

## Core request path

```text
ChatGPT/Work
  -> secure MCP tunnel
  -> FastMCP server
  -> policy/core module
  -> capability tool
```

For worker execution:

```text
dispatch request
  -> task bridge
  -> bounded task queue
  -> consumer
  -> pinned runner contract
  -> provider CLI
  -> report/evidence verification
  -> result artifact
```

## Security boundary

A portable deployment should configure:

- one or more absolute read roots;
- one isolated GPT sandbox write root;
- secret-path deny patterns;
- an allowlist for observable services/process fields;
- capability-specific subprocess execution with `shell=False` or equivalent;
- bounded output sizes and timeouts;
- compare-and-swap for edits;
- a separate operational Gate for production mutation.

Direct Channel should never turn chat input into unrestricted shell text.

## Why status comes first

A real external-chat UAT exposed GPT path hallucination: the model sent a relative path and a misspelled root. The server correctly rejected both.

The durable interaction contract is therefore:

```text
1. call control-plane status
2. learn current read roots/capabilities
3. call path-sensitive tools using exact absolute paths
```

A client should not guess deployment paths.

## Tool maturity history

The initial connector exposed a small tool surface. During V2 phases the server-side tool count grew from 7 to 20. The categories included:

- control-plane status;
- safe file/directory read;
- path policy preflight;
- bounded systemd/journal/process inspection;
- safe Git status;
- atomic GPT-sandbox write/move/delete;
- worker health/pre-dispatch/task/result functions;
- baseline and immutable-flag checks;
- security audit;
- bounded Gate request preparation.

The exact public implementation may expose a smaller or larger set, but the capability boundary is more important than raw tool count.

## Truth/authority labels

Read tools should attach authority labels such as:

- `NON_SSOT_OBSERVATION` for live observations;
- `GPT_SANDBOX_WRITE` for non-operational drafts;
- `PREPARED_NOT_APPLIED` for a Gate request that was only prepared.

This prevents the control plane from turning a safe observation or draft into a false production claim.

## Tunnel recovery

Operational testing included tunnel/service recovery scenarios. A resilient deployment should supervise both the consumer and tunnel, expose health/ready state, and prove reconnection after a bounded failure injection.

## Connector metadata freshness

A connector UI can cache an older tool schema even when the server has been upgraded. External UAT must distinguish:

- server tool surface;
- connector metadata cache;
- actual callable path.

A cached UI count is not authoritative evidence of the live MCP server's internal version.
