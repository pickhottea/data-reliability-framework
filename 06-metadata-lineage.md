# F6 — Metadata & Lineage Evidence (Audit Trail)

## Purpose

Data governance is only credible if data remains **traceable**.

Project F treats metadata and lineage as **governance evidence**, not optional documentation.

This deliverable answers:

- Where did this dataset come from?
- What transformations happened?
- Who owns the job?
- Can we reproduce the output?
- Can auditors verify continuity across environments?

Without lineage, reliability controls cannot be proven.

---

## Metadata vs Lineage (Governance Meaning)

### Metadata answers: “What is this asset?”

Examples:

- dataset name
- business purpose
- owner
- classification (PII / sensitive)
- contract version
- retention policy

Metadata enables:

- accountability
- compliance scope
- control ownership

---

### Lineage answers: “How did this asset happen?”

Lineage provides:

- upstream sources
- transformation jobs
- downstream consumers
- execution evidence

Lineage enables:

- auditability
- root cause analysis
- governance continuity across layers

---

## Evidence Requirements (Audit-Ready)

A governed dataset must carry:

### Dataset Metadata Fields

| Field | Required |
|------|----------|
| dataset_name | ✅ |
| business_owner | ✅ |
| technical_owner | ✅ |
| business_intent | ✅ |
| sensitivity_classification | ✅ |
| contract_version (F5) | ✅ |
| retention_policy | ✅ |

---

### Lineage Evidence Fields

| Field | Required |
|------|----------|
| input_dataset(s) | ✅ |
| transformation_job_id | ✅ |
| execution_timestamp | ✅ |
| output_dataset(s) | ✅ |
| environment (Linux / Windows) | ✅ |
| monitoring_reference (F3) | ✅ |

---

## Tooling Alignment (Project Context)

Project F uses modern open standards for lineage evidence:

- **OpenLineage** — lineage event specification  
- **Marquez** — metadata + lineage UI catalog  
- **PostgreSQL** — governed relational asset layer  
- **ELK (Project 2 extension)** — evidence storage + observability search  

These tools are positioned as:

> Evidence generators, not engineering complexity.

---

## Lineage as Governance Proof

A lineage chain proves continuity:

```text
Source Dataset
     ↓
Ingest Job (run_id)
     ↓
Validated Table (contract_version)
     ↓
Analytical View
     ↓
Exported Asset (cross-environment risk)
```

## Cross-Environment Governance Risk

Project F explicitly treats environment transitions as governance risk points:

- Linux ingestion pipeline
- Windows consumption and export layer

Key governance questions:

- Does lineage remain visible after export?
- Does contract version persist across environments?
- Does evidence remain auditable outside the platform?

This section becomes the foundation of **Project 3**:

> Business intent preservation across transformations.

---

## Operational Integration (F2–F4)

Metadata and lineage connect directly to operational governance.

### Data Quality Rules (F2)

Data Quality failures must always reference:

- dataset_name
- rule_id
- lineage context

This ensures quality controls remain traceable and explainable.

---

### Monitoring Alerts (F3)

Every alert payload must include:

- contract_version
- lineage_reference
- owner_contact

Without these fields, alerts cannot be routed or audited.

---

### Incident Response (F4)

Every incident ticket must link:

- affected dataset lineage context
- upstream source ownership
- runbook workflow and escalation path

This ensures incidents are not isolated events, but governed operational evidence.

---

## Key Principle

> Governance controls are only real if evidence is traceable.

- Metadata defines accountability  
- Lineage proves continuity  
- Together they make reliability auditable  

Project F demonstrates that:

- reliability is operational  
- governance is evidence-based  
- data becomes an enterprise asset through traceability  

---

