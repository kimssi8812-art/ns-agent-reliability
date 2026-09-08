# Git, GitHub and Chat Export Integration

> Historical-context note: words such as “current”, “live”, “healthy”, “blocked” or “verified” in dated sections describe the historical snapshot of that section, not the 2026-09-08 public release candidate or current private runtime. Current publication status is defined by the root README, manifest and publication checklist.


## Git repository state vs GitHub metadata

The project learned to treat local/remote Git repository freshness and GitHub Issue freshness as separate domains.

A Git fetch/branch comparison can establish facts about commits and tracking refs. It cannot prove which GitHub Issue is newest. When direct GitHub metadata is unavailable, the correct answer for issue freshness is `UNKNOWN_UNVERIFIED`.

## Private Git observation

Direct Channel's safe Git status interface is intended to expose bounded metadata such as:

- current branch;
- local HEAD identifier;
- tracking branch;
- ahead/behind counts;
- remote names without credential-bearing URLs;
- clean/changed-file summary.

It should not expose embedded remote credentials.

## GitHub intake / snapshot pattern

The private project used GitHub-generated or GitHub-received snapshots as bounded artifacts for review. A public implementation can use a similar pattern:

```text
GitHub change/PR
 -> snapshot artifact
 -> sandbox review
 -> evidence/test
 -> controlled promotion
```

The GitHub repository is a collaboration/versioning surface, not production runtime authority by itself.

## Chat Export

A parallel Chat Exporter project established an important continuity pattern:

```text
share link
 -> canonical extraction
 -> completeness judgement
 -> raw structured transcript
 -> human summary package
 -> AI conversation DNA
```

The connection project reuses the conceptual lesson: conversation history should be normalized into durable structured context rather than requiring a human to relay messages manually.

## Completeness and truth labels

Useful export/result states include:

- `VERIFIED_COMPLETE`;
- `BEST_EFFORT`;
- `FAILED`.

A context package should record provenance, completeness, and digest metadata so the Control Hub can decide how strongly to rely on it.

## Publication note

The open-source tree intentionally excludes raw private chat exports and private Git remotes. The architecture and schemas may be public while the user's historical conversations remain private evidence.
