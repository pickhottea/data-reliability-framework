# Clause 6 — Planning (Risk Assessment & Control Selection)

## Clause Intent (Plain Language)

ISO/IEC 27001 Clause 6 asks:

> What are the risks, and which controls are we using to treat them?

Controls are not added randomly.

Clause 6 requires:

- identifying information security risks  
- selecting controls that reduce those risks  
- documenting why each control exists  
- ensuring governance decisions are risk-based  

---

## Risk-Based Governance in Project F

Project F treats **data reliability failures** as governance risks.

The core risk question:

> Can business-critical data remain trustworthy across transformations, incidents, and environment boundaries?

Project F addresses this through reliability control planning:

- quality enforcement  
- monitoring evidence  
- escalation workflows  
- audit-ready traceability  

---

## Primary Risk Categories

Project F identifies key governance risk classes:

---

### Risk 1 — Data Quality Failure (Incorrect Decisions)

**Scenario:**  
Schema drift or invalid records enter downstream analytics.

**Impact:**  
Finance reporting errors, incorrect business decisions.

**Controls:**

- F2 Data Quality Rules Catalog  
- Contract enforcement (F5)

---

### Risk 2 — Loss of Freshness / Operational Delay

**Scenario:**  
Data pipelines succeed technically but violate SLA expectations.

**Impact:**  
Stale dashboards, delayed operational response.

**Controls:**

- F3 Monitoring & Alert Spec  
- Freshness thresholds and escalation routing

---

### Risk 3 — Unowned Failures (No Accountability)

**Scenario:**  
Alerts fire but no owner exists to respond.

**Impact:**  
Governance breakdown: failures become invisible.

**Controls:**

- Ownership requirements in alert payloads (F3)  
- Incident routing + runbook enforcement (F4)

---

### Risk 4 — Evidence Gaps (Audit Failure)

**Scenario:**  
A dataset cannot be traced back to its origin during review.

**Impact:**  
Compliance risk, inability to prove governance continuity.

**Controls:**

- Metadata + Lineage Evidence (F6)  
- OpenLineage + Marquez traceability

---

### Risk 5 — Cross-Environment Governance Drift

**Scenario:**  
Data is exported or consumed outside the governed platform.

**Impact:**  
Loss of contract versioning, unclear responsibility boundary.

**Controls:**

- Clause4 scope boundary enforcement  
- Project 3 extension: intent preservation validation

---

## Risk Treatment Strategy

Project F applies the ISO risk treatment model:

1. Identify governance risk  
2. Select reliability controls  
3. Monitor control effectiveness  
4. Produce evidence for audit  
5. Improve controls continuously  

Controls are chosen because they reduce specific operational risks.

---

## Control Inventory Mapping (Project F)

Clause 6 requires explicit control selection.

Project F control inventory:

- Preventive Controls  
  - Data Quality Rules (F2)  
  - Data Contracts (F5)

- Detective Controls  
  - Monitoring & Alerts (F3)  
  - Observability evidence loop (Project 2 extension)

- Corrective Controls  
  - Incident Response Playbook (F4)  
  - Corrective action and improvement workflow

- Traceability Controls  
  - Metadata + Lineage Evidence (F6)

---

## Governance Planning Outcome

Clause 6 is satisfied when:

- controls are risk-justified  
- ownership exists  
- evidence is operational, not theoretical  
- monitoring proves controls are active  

Project F demonstrates a complete planning loop:

> Risk → Control → Evidence → Review → Improvement

---

## Key Clause 6 Takeaway

> Controls are not checklists.  
> Controls are selected because they reduce real governance risk.

Project F demonstrates Clause 6 through reliability-first control planning aligned with audit evidence.

---
