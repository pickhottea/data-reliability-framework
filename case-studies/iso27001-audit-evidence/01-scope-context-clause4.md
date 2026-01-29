# Clause 4 — Context of the Organization (Scope & Governance Boundary)

## Clause Intent (Plain Language)

ISO/IEC 27001 Clause 4 asks one foundational question:

> What exactly is the system we are securing and governing?

Before any controls, audits, or monitoring can exist, the organization must define:

- scope boundaries  
- business context  
- stakeholders  
- governance assumptions  

Without scope clarity, security controls cannot be evaluated.

---

## Project Scope Definition (Project F)

This portfolio defines an ISMS-relevant governance scope focused on:

- reliability-critical data assets  
- observability evidence  
- operational governance controls  

The scope includes the lifecycle from:

- ingestion  
- validation  
- monitoring  
- incident response  
- audit evidence preservation  

---

## In-Scope Assets

Project F governs the following data reliability assets:

- structured transactional datasets (e.g., yield or sales-like data)
- metadata records and ownership definitions
- monitoring outputs and alert evidence
- lineage continuity across transformations

Key governed artifacts:

- Data Quality Rules (F2)
- Monitoring & Alert Spec (F3)
- Incident Response Playbook (F4)
- Data Contracts (F5)
- Metadata & Lineage Evidence (F6)

---

## Out-of-Scope Boundaries

This portfolio intentionally excludes:

- full production infrastructure hardening  
- identity provider configuration  
- enterprise-wide SOC operations  
- AI/ML model governance  

Project F is scoped as a **data reliability governance control system**, not a complete corporate ISMS deployment.

---

## Interested Parties (Stakeholders)

Clause 4 requires identifying parties who depend on the governed system.

In Project F, key stakeholders include:

- **Data Producers**  
  Responsible for upstream correctness and schema stability

- **Data Consumers**  
  Depend on reliable, decision-ready datasets

- **Governance / Compliance Functions**  
  Require audit evidence, traceability, and accountability

- **Security / Risk Owners**  
  Need classification, retention, and incident response proof

---

## Business Need Alignment

The business purpose of this scope is:

> Ensuring that enterprise data remains trustworthy and auditable across environments, transformations, and operational failures.

This directly supports:

- decision readiness  
- governance continuity  
- compliance evidence generation  
- risk-based operational control

---

## Governance Boundary Principle

Clause 4 establishes the core rule:

> Controls only exist where scope is defined.

Project F enforces this by requiring:

- explicit dataset ownership  
- contract boundaries  
- monitoring evidence  
- traceable lineage context  

Reliability governance is only valid inside an accountable boundary.

---

## Evidence Produced (Audit Readiness)

Clause 4 evidence in this repository includes:

- lifecycle definition (F1)
- scoped governance artifacts (F2–F6)
- defined ownership + accountability model
- documented boundary of what is governed vs excluded

---

## Key Clause 4 Takeaway

> Scope comes before controls.  
> Context comes before compliance.  
> Governance begins with defining what is inside the boundary.

Project F demonstrates Clause 4 through a practical, audit-oriented data reliability governance scope.

---
