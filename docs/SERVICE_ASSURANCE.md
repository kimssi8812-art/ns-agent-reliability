# Professional service assurance & responsibility boundary

The open-source Doctor is an automated diagnostic tool. Paid NS reliability services add an **AI-assisted, evidence-reviewed, human-reviewed** professional-service layer around the agreed customer scope.

This page describes the delivery standard. It is not jurisdiction-specific legal advice and does not replace a customer-specific signed agreement.

## 1. Evidence truth states

Material customer findings use one of three states:

- **OBSERVED** — directly visible in supplied evidence or a bounded reproduction.
- **SUPPORTED** — supported by multiple artifacts or a strong causal chain, but not directly reproduced in the customer environment.
- **UNKNOWN** — evidence is missing, ambiguous, stale or outside the agreed scope.

`UNKNOWN` is not silently converted to PASS.

## 2. Human review

Before a paid Audit report is delivered, all `CRITICAL` and `HIGH` findings require human review of:

- the evidence supporting the claim;
- evidence freshness/environment;
- severity and plausible blast radius;
- alternative explanations where material;
- the proposed remediation;
- the acceptance test;
- sensitive-data minimization.

If a reviewer cannot explain why an AI-generated material finding is supported by the supplied evidence, it is not delivered as fact. It is removed, downgraded to a hypothesis, or marked UNKNOWN.

## 3. Audit is read-only by default

MCP Surface & Contract Quick Audit and AI Agent Reliability Audit do not include production mutation, credential acquisition, unrestricted remote administration or deployment changes.

Implementation is a separately scoped Hardening engagement.

## 4. No-guarantee boundary

A bounded audit does not promise:

- discovery of every defect, vulnerability or failure mode;
- zero future incidents, downtime or data loss;
- guaranteed performance, security, cost or revenue improvement;
- correctness of evidence that was not supplied or cannot be verified;
- future compatibility with third-party systems that change after delivery.

The service delivers a bounded assessment based on the written scope and evidence available during the engagement.

## 5. Hardening change control

When a separately contracted Hardening Sprint includes production change, the expected minimum path is:

`scope lock → current-state capture → staging/test → rollback point/plan → explicit customer approval → bounded production mutation → live-result verification → acceptance or rollback`

Production mutation is not inferred from an Audit purchase.

## 6. Customer data boundary

Default posture:

- minimum necessary evidence;
- read-only evidence collection where possible;
- credentials/secrets excluded by default;
- unrelated PII/customer data excluded;
- processing/storage/retention route agreed before sensitive evidence is accepted;
- no customer material enters OSS or a public case study without explicit permission.

## 7. Case studies

A paid engagement does not automatically become marketing material. Customer outcome publication requires explicit written permission for one of:

- no public case study;
- anonymous/sanitized case study;
- named case study with specifically approved facts/results.

The final public draft should be customer-approved before publication.

## 8. Contract boundary

Before signature, the customer-specific agreement should address the applicable scope/exclusions, payment, confidentiality, data processing, IP, acceptance/change control, warranty/no-guarantee wording, liability allocation, termination and governing-law/dispute terms.
