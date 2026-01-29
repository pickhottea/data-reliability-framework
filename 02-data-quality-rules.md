# F2 — Data Quality Rules Catalog (Project F)

## Purpose

Data quality is not a vague concept.

In governed data systems, quality must be translated into:

- explicit rules
- measurable checks
- severity levels
- ownership
- audit evidence

This document defines the **Data Quality Rules Catalog** for Project F.

---

## Rule Template

Every rule must include:

| Field | Meaning |
|------|---------|
| Rule ID | Unique identifier |
| Dimension | Completeness / Validity / Timeliness / Consistency |
| Description | Human-readable intent |
| Severity | Sev1–Sev3 |
| Check Logic | What is being tested |
| Evidence Output | What is logged or stored |
| Owner | Who is accountable |

Rule:

> A rule without evidence is not a control.

---

## Core Data Quality Dimensions

| Dimension | Question |
|----------|----------|
| Completeness | Are required fields present? |
| Validity | Are values within allowed ranges? |
| Uniqueness | Are keys duplicated? |
| Consistency | Do fields agree across systems? |
| Timeliness | Is the data fresh enough? |
| Integrity | Are relationships preserved? |

---

## Example Rules (Yield Monitoring Dataset)

### Completeness Rules

| Rule ID | Description | Severity | Evidence |
|--------|-------------|----------|----------|
| DQ-C-01 | `wafer_id` must not be NULL | Sev1 | missing_id_count |
| DQ-C-02 | `measurement_time` must exist | Sev1 | null_timestamp_count |

Business impact:

- missing identifiers break traceability

---

### Validity Rules

| Rule ID | Description | Severity | Evidence |
|--------|-------------|----------|----------|
| DQ-V-01 | `yield_rate` must be within [0,1] | Sev1 | invalid_value_count |
| DQ-V-02 | `process_step` must be in approved list | Sev2 | invalid_category_count |

Business impact:

- invalid values destroy decision readiness

---

### Uniqueness Rules

| Rule ID | Description | Severity | Evidence |
|--------|-------------|----------|----------|
| DQ-U-01 | `(wafer_id, measurement_time)` must be unique | Sev2 | duplicate_row_count |

Business impact:

- duplicates inflate KPIs

---

### Consistency Rules

| Rule ID | Description | Severity | Evidence |
|--------|-------------|----------|----------|
| DQ-S-01 | `lot_id` must map to correct product family | Sev3 | mismatch_count |
| DQ-S-02 | Region definitions must remain stable across exports | Sev3 | dimension_drift_flag |

Business impact:

- inconsistent definitions cause governance conflict

---

### Timeliness Rules

| Rule ID | Description | Severity | Evidence |
|--------|-------------|----------|----------|
| DQ-T-01 | Dataset freshness lag must be < 24h | Sev2 | freshness_lag_hours |
| DQ-T-02 | Daily partition must arrive before 09:00 | Sev2 | late_arrival_flag |

Business impact:

- stale data becomes outdated enterprise truth

---

## Severity Policy

| Severity | Meaning | Action |
|---------|---------|--------|
| Sev1 | Data cannot be trusted | Stop serving + incident ticket |
| Sev2 | Degraded quality | Investigate within SLA |
| Sev3 | Improvement opportunity | Track and review weekly |

Linked artifact:

- Sev1/Sev2 triggers **F4 Incident Response Playbook**

---

## Evidence & Auditability

Each rule must produce evidence that can be stored in:

- monitoring logs (F3)
- ELK evidence dashboards (Project 2)
- metadata lineage records (F6)

Evidence must include:

- rule ID
- run ID
- timestamp
- failure counts
- owner notified

---

## Review & Continuous Improvement

Rules are not static.

Required lifecycle:

- weekly quality review
- post-incident rule refinement
- quarterly governance audit alignment

Rule:

> Data quality is a living control system, not a one-time checklist.

---

## Key Principle

> Data becomes an enterprise asset only when quality expectations are explicit, owned, and auditable.

This catalog is the control foundation connecting:

- Monitoring & Alerts (F3)
- Incident Response (F4)
- Data Contracts (F5)
- Metadata & Lineage Evidence (F6)

