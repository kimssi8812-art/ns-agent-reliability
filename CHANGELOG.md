# Changelog

## Main — public packaging enhancement — 2026-09-08

Repository is public and remotely verified. Added the first conversion/discovery layer without changing the Doctor core:

- visual terminal demo based on actual Doctor output;
- symptom-first “Use this if…” triage near the top of README;
- LangGraph, CrewAI, OpenAI Agents SDK and MCP evidence-mapping guide;
- neutral normalized snapshot template;
- illustrative/sanitized audit report clearly labeled as **not** an external customer case;
- commercial service scope/pricing sourced from NS Package Factory;
- public no-secret Audit Fit Check issue form;
- lightweight GitHub Pages sales surface;
- tracked public scope expanded from 77 to 86 files; clean install, 32/32 tests, Doctor 15 findings, snapshot-template 0 findings, public scrub and package-license boundary all reverified.

## 0.1.0rc1-prepublication — 2026-09-08

Doctor-first release candidate prepared for external publication.

Added/changed:

- installed `ns-reliability` CLI and 60-second first-value README path;
- Agent Reliability Doctor source, broken fixture and tests included in the tracked public scope;
- clean Python 3.11 wheel build/install + installed CLI smoke verified;
- full candidate regression suite: **32/32 PASS**;
- Doctor-inclusive tracked-tree scrub and manifest verification;
- Apache-2.0 software license, CC BY 4.0 narrative-documentation scope, NOTICE, trademark policy, third-party provenance note and SPDX SBOM;
- historical/live wording corrected so historical provider states are not presented as current runtime truth.

Still not public:

- target GitHub owner/repository and authenticated write path are not yet bound;
- no public push or remote install verification has occurred.

## 0.0.2-publication-candidate — 2026-09-02

Harvested two verified reliability patterns from real operational incidents without creating a second runtime or publication system.

Added:

- build-once / verify-once / one-atomic-production-commit reference primitive with live-SHA CAS, validation-evidence binding, rollback-once and failed-candidate-SHA replay denial;
- portable lease/fencing primitive that separates client-session lifetime from workflow mutation ownership;
- monotonic fencing epoch on every successful lease acquisition;
- regression coverage for released/expired lease reacquisition, active foreign-lease takeover denial and stale-holder rejection;
- sanitized incident notes for deployment-Gate expansion and released-lease/live-session coupling;
- prepared license recommendation: Apache-2.0 target for software, CC BY 4.0 target for eligible narrative documentation, separate trademark treatment, and original third-party provenance controls.

Verified in the publication candidate:

- one-live-commit focused regression: 7 cases;
- lease/session independence focused regression: 5 cases;
- full current publication-candidate test suite: 27 passed in the independent read-only verification run;
- bounded scan of the newly harvested lease incident files found no flagged private server paths, credentials, private endpoints/account IDs or Trading content.

Still a publication candidate:

- final canonical LICENSE/NOTICE/SPDX metadata have not been applied;
- dependency/SBOM/provenance and clean-room release verification remain release-gate work;
- public repository exposure remains a human release boundary.

## 0.0.1-publication-candidate — 2026-08-12

V3 architecture update layered on the existing V2 Control Hub/Worker Manager design.

Added:

- bounded Deterministic Executor policy/reference module;
- deterministic-first routing principle;
- zero-unnecessary-AI Chat-share/DNA continuity design;
- explicit DNA target and bounded inheritance-packet reference logic;
- Atomic `FlowEvent` / Event Ledger reference model;
- Machine Flowboard + Human Cockpit dual projection contracts;
- V3 executor/DNA/observability schemas and tests;
- incident lessons for deterministic-work provider leakage and report-format retry coupling;
- progressive GPT/N direct-execution reduction model;
- updated roadmap and architecture diagrams.

Clarified:

- the objective is not zero model usage; it is zero **unnecessary** model usage for deterministic work;
- a bounded executor is not unrestricted root shell and never bypasses secret/SSOT/Gate boundaries;
- Human Cockpit must derive from machine truth rather than maintain a competing collector;
- scaffold/reference code is not production acceptance evidence.

Still not claimed as production-complete:

- live bounded Direct Executor integration;
- end-to-end zero-unnecessary-AI DNA UAT;
- live universal Worker Manager/Goal Session authority;
- normal multi-provider routing acceptance;
- durable live Atomic Event Ledger and dashboard projections;
- final reproducible public UAT;
- public repository push;
- final open-source license selection.

## 0.0.0-publication-candidate — 2026-08-11

Initial reconstructed open-source package covering the private project's connection work through the V2 Control Hub/Worker Manager architecture.

Included:

- Direct Channel architecture and security boundary;
- historical test/UAT evidence summary and preservation of revoked claims;
- Context/DNA and baseline/delta continuity design;
- Control Hub architecture;
- Worker Manager + Goal Session architecture;
- evidence-weighted Goal DAG/progress;
- resource/context/session governance;
- provider model/runtime/version governance;
- security/Gate authority model;
- incident/lesson catalogue;
- portable reference Python contracts and JSON schemas;
- current status and roadmap.
