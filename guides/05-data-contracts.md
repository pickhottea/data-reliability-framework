# F5 — Data Contracts (Project F)

## Purpose

Data contracts prevent silent drift.

They define the explicit agreement between:

- producers (who publish data)
- consumers (who rely on data)

A governed dataset must not change unexpectedly.

Project F uses contracts to ensure:

- schema stability
- semantic consistency
- audit-ready accountability

---

## Why Contracts Matter

Without contracts:

- columns appear/disappear silently  
- definitions shift over time  
- downstream dashboards break  
- compliance evidence becomes unreliable  

Key principle:

> Trust requires explicit guarantees.

---

## Contract Scope

A contract applies to:

- dataset schema
- required fields
- allowed value ranges
- freshness expectations
- ownership and versioning

---

## Contract Template

Every contract must specify:

| Element | Description |
|--------|-------------|
| Dataset Name | Asset identifier |
| Version | Semantic version (v1.0, v1.1…) |
| Owner | Accountable person/team |
| Schema Definition | Fields + types |
| Required Fields | Non-null guarantees |
| Validity Constraints | Allowed ranges/categories |
| Refresh SLA | Timeliness requirement |
| Compatibility Rules | Backward/forward expectations |

---

## Example Contract — Yield Monitoring Dataset

### Dataset Metadata

- **Dataset:** `yield_monitoring.daily`
- **Domain:** Manufacturing Analytics
- **Owner:** Data Reliability Owner
- **Version:** v1.0

---

### Schema Definition

| Field | Type | Required | Notes |
|------|------|----------|------|
| wafer_id | string | ✅ | primary identifier |
| lot_id | string | ✅ | batch grouping |
| process_step | string | ✅ | manufacturing stage |
| yield_rate | float | ✅ | must be within [0,1] |
| measurement_time | timestamp | ✅ | event timestamp |
| region | string | optional | governance tension dimension |

---

### Validity Constraints

| Field | Constraint |
|------|------------|
| yield_rate | must be between 0 and 1 |
| process_step | must belong to approved step list |
| measurement_time | cannot be in the future |

---

### Freshness SLA

| Requirement | Threshold |
|------------|-----------|
| Daily refresh | < 24h lag |
| Partition arrival | before 09:00 |

Failure triggers:

- Sev2 alert (F3)
- Incident escalation if repeated (F4)

---

## Versioning Policy

Contracts follow semantic versioning:

| Change Type | Example | Version Impact |
|------------|---------|---------------|
| Breaking | remove/rename column | Major bump (v2.0) |
| Additive | add optional field | Minor bump (v1.1) |
| Patch | documentation/metadata update | Patch bump (v1.0.1) |

Rule:

> Breaking changes must never happen silently.

---

## Enforcement Workflow

On every pipeline run:

1. Validate schema against contract
2. Record contract version in metadata evidence (F6)
3. Fail fast if breaking drift detected (Sev1)
4. Trigger incident workflow if needed (F4)

---

## Contract Evidence Output

Each run should store:

- contract version used
- validation pass/fail
- drift type (if any)
- owner notified

This produces audit-ready proof of stability.

---

## Contract + Governance Link

Contracts connect directly to:

- **F2 Rules Catalog** (quality constraints)
- **F3 Monitoring** (drift alerts)
- **F4 Playbook** (incident escalation)
- **F6 Metadata & Lineage** (evidence traceability)

---

## Key Principle

> Data contracts transform datasets from informal outputs into governed enterprise assets.

Project F treats contracts as reliability guarantees, not documentation.

