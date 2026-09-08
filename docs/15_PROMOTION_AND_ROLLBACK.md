# Promotion and Rollback

> Historical-context note: words such as “current”, “live”, “healthy”, “blocked” or “verified” in dated sections describe the historical snapshot of that section, not the 2026-09-08 public release candidate or current private runtime. Current publication status is defined by the root README, manifest and publication checklist.


## Problem

A conversational control plane can safely draft code and prepare change candidates without being allowed to modify operational state directly. The system therefore needs a deterministic bridge from reviewed sandbox artifacts to the deployment-specific Gate.

## Promotion pattern

```text
sandbox candidate
 -> full-original/baseline verification
 -> dependency/execution-path check
 -> bounded change manifest
 -> human/Gate approval where required
 -> atomic promotion
 -> service/canary verification
 -> evidence
 -> rollback automatically if acceptance fails
```

## Runtime Promotion Bridge concept

The private project developed a Runtime Promotion Bridge pattern so one human approval can authorize a narrowly scoped, evidence-producing promotion instead of requiring many manual terminal commands.

The public architecture does not embed the private implementation. Instead it exposes a deployment adapter contract.

## Required inputs

A promotion request should identify:

- target artifact/path class;
- expected current digest;
- candidate digest;
- exact bounded operation;
- required service/reload action if any;
- acceptance/canary checks;
- rollback source/digest;
- approval reference when the environment requires one.

## Required outputs

The bridge should return evidence sufficient to distinguish:

- request prepared;
- approval validated;
- candidate promoted;
- restart/reload performed;
- canary passed/failed;
- rollback performed/not required;
- final digest/state.

## Atomicity and rollback

A robust implementation should stage alongside the target where possible, validate before replacement, perform a bounded atomic replacement, run a canary, and restore the known rollback artifact automatically on failure.

## Authority rule

A chat-side function that only creates the request is not the apply function. Documentation and UI should use explicit authority/status labels so `PREPARED` can never be confused with `APPLIED`.
