# Resource, Model and Version Governance

> Historical-context note: words such as “current”, “live”, “healthy”, “blocked” or “verified” in dated sections describe the historical snapshot of that section, not the 2026-09-08 public release candidate or current private runtime. Current publication status is defined by the root README, manifest and publication checklist.


## Resource control principle

The project treats provider allocation, active context, model choice, session continuity, host resources, and retry cost as scheduling inputs.

Structural waste is addressed before arbitrary hard limits:

```text
session reuse
 -> baseline once
 -> delta context
 -> externalize large evidence
 -> restore multi-agent routing
 -> then add budgets/thresholds
```

A hard budget should not hide the cause of repeated cold starts or duplicate file/history reads.

## Resource hierarchy

### Hub ledger

Aggregates worker readiness, active/warm sessions, context estimates, usage signals, quota/rate-limit state, memory/CPU/runtime where observable, and retry/failure cost.

### Worker Manager ledger

Tracks provider-specific session load, auth/readiness, runtime/model inventory, usage signal source, recent success/failure, and capacity state.

### Goal Session ledger

Tracks baseline input estimate, deltas, tool/output size, session runtime, context growth, checkpoint count, failure/retry events, and provider-reported usage when available.

## Provider execution profile

The scheduler should select more than a provider name. A complete execution profile may include:

```text
provider
runtime/CLI identity + version
adapter version
model identifier
reasoning/effort profile
supported tools/capabilities
verified context capacity
session-resume compatibility
resource/quota state
```

## Selection rule

The best model is not always the newest or largest. Selection should use verified measurements and workload requirements such as:

- capability fit;
- acceptance-quality history;
- latency;
- context headroom;
- provider allocation pressure;
- recent failure/retry cost;
- tool/session compatibility;
- warm Goal Session affinity;
- switch/rehydration cost.

Unknown values remain unknown and must not be replaced by invented scores.

## Session pinning

Once a Goal Session starts with a verified execution profile, the profile should normally remain pinned for that session generation. Mid-session model/runtime changes can alter behavior and invalidate context continuity assumptions.

If a change is required:

```text
checkpoint -> persist state/evidence -> controlled rollover -> new pinned profile
```

## Version governor

New runtime/model/adapter combinations move through a lifecycle similar to:

```text
DISCOVERED
 -> COMPATIBLE
 -> SHADOW/CANARY
 -> ACCEPTED
 -> PROMOTED
```

Failures can produce `QUARANTINED` or rollback to a previous accepted profile.

Promotion evidence should include compatibility, task success, regression tests, resource behavior, and session/context semantics. A version string alone is not evidence of superiority.

## Adaptive optimization

Over time the Hub can build workload-specific empirical priors. For example, a smaller/faster model may dominate routine deterministic edits while a stronger model may be reserved for architecture review or high-risk Gate preparation.

The human should not have to manually select models during normal operation; the Hub should explain the selected profile when needed and request human involvement only for paid-plan/account boundaries.
