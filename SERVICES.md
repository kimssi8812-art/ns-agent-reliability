# Commercial reliability services

The open-source Doctor is free to use under its published license. Commercial services are optional and review the stack you already run; they do **not** require migration to an NS runtime.

> Launch-stage offers: the technical capability and package definitions are ready, but NS does not claim external customer validation or customer case studies yet.

## Delivery assurance

Paid reliability services are **AI-assisted, evidence-reviewed and human-reviewed**. `CRITICAL` and `HIGH` customer findings require human sign-off before delivery. Audit work is read-only by default, missing evidence remains `UNKNOWN`, and NS does not guarantee discovery of every defect or elimination of all future incidents.

See [Professional service assurance & responsibility boundary](docs/SERVICE_ASSURANCE.md).

Prices below are **fixed regional launch pricing**, not daily FX conversions. USD is the primary global display; KRW is the Korea price.

## MCP Surface & Contract Quick Audit — $750

Korea: **₩990,000**

**Best for:** teams whose MCP/tool surface has grown faster than its contract and authority model.

**2–3 business days / one bounded MCP or tool surface**

You receive:
- current surface inventory;
- duplicate/legacy/authority findings;
- target simplification map;
- stale-schema and rollback-risk checklist;
- one findings walkthrough.

Not a penetration test, application rewrite or full reliability audit.

## AI Agent Reliability Audit — Founding $1,100 / Standard $2,200

Korea: **Founding ₩1,490,000 / Standard ₩2,900,000**

**Best for:** production or late-staging action-capable agents with repeated execution, recovery or deployment failures.

**3–5 business days / one bounded agent stack**

You receive:
- reliability scorecard;
- evidence-ranked critical findings;
- failure scenarios and root causes;
- priority hardening plan;
- scope-simplification recommendations;
- one findings walkthrough.

Founding pricing is limited to early bounded engagements and will be retired after reference cases are established.

## Safe Deployment Hardening Sprint — from $5,000

Korea: **₩6,900,000** for the current bounded launch scope

**Best for:** teams that already know their deploy/rollback path can drift, replay stale behavior or confuse candidate success with live success.

**5–10 business days / one bounded deployment path**

You receive:
- deployment-path risk map;
- one-live-commit / CAS / evidence design;
- bounded implementation in the agreed target;
- rollback/replay regression checks;
- handover checklist.

## Start with a fit check

**Public / no-secret intake:** [Open the Reliability Audit Fit Check](https://github.com/kimssi8812-art/ns-agent-reliability/issues/new?template=audit-fit-check.yml)

GitHub sign-in is required to submit the fit-check issue. The issue is public. Do **not** include credentials, private repositories, customer data, private endpoints, proprietary logs or other confidential material. If the situation is sensitive, submit only a high-level symptom and request a private follow-up path.

Before any audit accepts customer material, the evidence boundary and processing route must be agreed explicitly.

## What happens next

1. Fit check: production/late-staging status, action surface, observed failure pattern.
2. Scope: one bounded stack/surface and read-only evidence boundary.
3. Audit: evidence-backed findings; UNKNOWN remains UNKNOWN.
4. Readout: NOW / NEXT / LATER remediation order.
5. Optional implementation: only selected findings become a separately scoped Hardening Sprint.

See the [illustrative sample report](docs/SAMPLE_AUDIT_REPORT.md) and [integration/evidence guide](docs/INTEGRATIONS.md).
