# Prehistory — From Manual Relay to Direct Channel

> Historical-context note: words such as “current”, “live”, “healthy”, “blocked” or “verified” in dated sections describe the historical snapshot of that section, not the 2026-09-08 public release candidate or current private runtime. Current publication status is defined by the root README, manifest and publication checklist.


The GPT↔server connection project predates Direct Channel. Its engineering lineage begins with the problem that GPT could reason about the project but could not directly inspect or operate the server.

## 2026-07-05 — explicit GPT/Claude division of labor

An early collaboration contract defined:

```text
Human -> direction
GPT -> high-level context, methodology, prioritization
Claude CLI -> direct server inspection, execution and verification
```

At this stage GPT depended on Claude to summarize server state. The document explicitly recorded GPT's major limitations: no direct system visibility and weak cross-session continuity.

This is the architectural problem that the later Control Plane solves.

## 2026-07-08 — first server-side Claude -> ChatGPT direct conversation

A Playwright-based bridge achieved the first recorded direct conversation where Claude on the server sent a message to the ChatGPT UI and received the response without the human relaying each message.

The bridge used browser automation, an authenticated browser session, message insertion, response-completion detection, and multi-round discussion loops.

Historical significance:

```text
Before:
Human -> Claude -> Human -> GPT -> Human -> Claude

After Playwright bridge:
Claude server process <-> ChatGPT UI
Human -> observes/approves
```

This proved the value of removing the human relay, but it was still browser/UI automation rather than a stable control-plane protocol.

## 2026-07-10 — common bridge runtime

The Playwright bridge evolved into a shared runtime usable by server worker roles. This made GPT connectivity a reusable infrastructure component rather than a one-off browser script.

## 2026-07-28 — bridge operational hardening

The historical manual records show further hardening around persistent browser execution and a unified entry path. The exact browser-auth details are deliberately excluded from this public package because they are deployment-specific and can involve sensitive session material.

## Why the Playwright approach was not the final architecture

Browser automation proved the concept but has structural weaknesses:

- UI selectors and application layout can change;
- browser authentication/session state is brittle;
- Cloudflare/bot-detection behavior adds operational coupling;
- tool capability/authority is implicit in UI actions;
- server state and worker results are harder to normalize as typed evidence;
- a fresh chat cannot easily discover a deterministic server capability surface.

These limitations motivated the next architecture: an MCP-based Direct Channel with explicit tools, read/write boundaries, health, worker dispatch, and Gate separation.

## Architectural lineage

```text
GPT advisory role (human relay)
  -> Playwright GPT bridge
  -> automated Claude <-> GPT discussion
  -> shared Collab/runtime integration
  -> Direct Channel MCP
  -> Context/DNA + Context Gravity
  -> NS Control Hub
  -> Worker Manager + reusable Goal Session
  -> resource/model/version governance
```

The open-source project should preserve this lineage because it explains why the final architecture separates transport, truth, worker lifecycle, context, and operational authority instead of relying on a browser automation script alone.
