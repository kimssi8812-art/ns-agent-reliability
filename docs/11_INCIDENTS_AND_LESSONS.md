# Incidents and Engineering Lessons

> Historical-context note: words such as “current”, “live”, “healthy”, “blocked” or “verified” in dated sections describe the historical snapshot of that section, not the 2026-09-08 public release candidate or current private runtime. Current publication status is defined by the root README, manifest and publication checklist.


This catalogue exists because the connection project was shaped as much by failures as by successful implementation.

## Incident: internal test reported as external E2E

**Symptom:** General Chat UAT was labelled PASS before an actual ordinary ChatGPT room exercised the connector.

**Correction:** PASS was formally revoked.

**Lesson:** evidence must match the claimed boundary. Internal unit/integration tests cannot prove external chat E2E.

---

## Incident: client path hallucination

**Symptom:** GPT supplied a relative path and a misspelled server root.

**Server behavior:** correctly denied both.

**Correction:** status response exposed allowed read roots; tool descriptions instructed clients to query status first and use exact absolute paths.

**Lesson:** do not require a model to memorize deployment paths; expose discoverable capability metadata.

---

## Incident: connector tool metadata cache drift

**Symptom:** UI displayed an older tool count even though the server had a newer surface.

**Lesson:** distinguish connector metadata cache from live MCP server behavior. Version/tool discovery must have an explicit freshness source.

---

## Incident: provider allocation leakage from cold task sessions

**Symptom:** repeated bounded tasks consumed provider allocation rapidly.

**Root architectural issue:** each task could start a fresh provider process and rehydrate context.

**Correction:** introduce Worker Manager + one Goal/one session + baseline once/delta thereafter. Hard budgets become guardrails after structural waste is removed.

---

## Incident: provider allocation leakage during deterministic DNA ingestion

**Symptom:** conversation/DNA ingestion succeeded at the infrastructure level, but a provider worker was used to create/check intake state and then retried after report-schema failures. Large DNA/history content was also reread to reconstruct continuity.

**Root architectural issue:** deterministic infrastructure responsibilities were coupled to general-purpose provider workers because GPT/N lacked a direct bounded executor/intake path.

**Correction:** V3 introduces:
- deterministic-first routing;
- bounded Direct Executor capability;
- provider-forbidden `CHAT_SHARE`/`DNA_HYDRATION` infrastructure paths by default;
- explicit DNA target selection;
- bounded inheritance packets/references instead of default full-DNA/history replay;
- direct infrastructure verification before any recovery provider call.

**Lesson:** the target is not "zero model usage at all costs." The target is **zero unnecessary model usage for deterministic work**. Models remain appropriate when semantic reasoning is actually required.

---

## Incident: report-format failure triggered unnecessary recovery

**Symptom:** a provider task's final report violated a strict schema even though the requested external/deterministic side effect may already have occurred.

**Lesson:** separate execution truth from report formatting. Before retrying a provider, inspect deterministic state/evidence directly. A malformed report must not automatically imply the underlying operation failed.

---

## Incident: Codex SESSION_DEAD circular deadlock

**Symptom:** Direct Channel reported Codex unavailable and work silently fell back toward Claude.

**Cause:** Direct Channel health depended on a legacy tmux lifecycle while legacy auto-sleep could kill the same session after a different inbox went idle. Direct Channel could not reach the wake path because pre-dispatch health already blocked it.

**Lesson:** a transport must not depend exclusively on another transport's session lifecycle as its own readiness authority.

---

## Incident: stale quota latch vs current human evidence

**Symptom:** persisted server state continued to report quota exhaustion after the human reported allocation was available again.

**Lesson:** quota, auth, liveness, readiness, provider-reported usage and persisted latches are separate signals. A stale latch should trigger verification, not become permanent truth.

---

## Incident: health collector self-test false confidence

**Symptom:** an implementation reported a large self-test PASS count while using the wrong persisted JSON shape and stale timestamp field.

Further review found neutral signals returning `True`, a session identity mismatch, schema incompatibility, and a deeper liveness/readiness conflation.

**Lesson:** test count is not semantic coverage. Reference-contract and live-fixture tests must be present.

Durable invariant:

```text
LIVENESS != READINESS != DISPATCH_ALLOWED
```

---

## Incident: false runner SHA mismatch diagnosis

**Symptom:** a worker compared a configuration digest to the runner script digest and proposed a configuration change.

**Countercheck:** the configured digest actually pinned a different artifact and it matched.

**Lesson:** before repairing a digest mismatch, prove which artifact the digest is contractually bound to.

---

## Incident: current-state claim from wrong freshness domain

**Symptom:** repository Git freshness was used to make a claim about the latest GitHub Issue.

**Lesson:** Git repository state and GitHub Issue metadata are separate freshness domains. If direct issue evidence is unavailable, the result is UNKNOWN rather than an inferred latest issue.

---

## Incident: conflicting "alive/dead" worker claims

**Symptom:** a manual CLI could be alive while the Direct Channel path for the same provider was dead, creating apparently contradictory status statements.

**Correction:** observability must preserve explicit session scope such as `MANUAL_CLI`, `DIRECT_CHANNEL`, `COLLAB`, and `GOAL_SESSION`.

**Lesson:** provider identity alone is not a health key. Scope/session generation/source/freshness are part of the identity of a health claim.

---

## Engineering pattern that emerged

The project adopted a repeated review loop:

```text
N reference scaffold
 -> deterministic direct checks when appropriate
 -> worker implementation/review when model reasoning is needed
 -> N semantic/evidence check
 -> regression test added
 -> repeated deterministic loop promoted into Hub automation
 -> next checkpoint
```

This pattern catches errors that provider-local self-tests and conversational PASS reports can miss while also reducing unnecessary provider hops as the system matures.
