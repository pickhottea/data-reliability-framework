# F3 — Monitoring & Alert Specification (Project F)

## Purpose

Monitoring is the operational proof that governance controls are alive.

This document defines:

- reliability signals (what to measure)
- alert thresholds (when to escalate)
- routing rules (who responds)
- evidence requirements (what must be recorded)

Goal:

> Convert data quality and governance intent into measurable operational evidence.

---

## Monitoring Scope

Project F monitors reliability across:

- ingestion jobs
- governed datasets
- schema/contract stability
- freshness and timeliness
- downstream decision readiness
- incident escalation triggers

---

## Key Reliability Signals

### 1. Freshness & Timeliness

| Metric | Meaning | Alert Condition |
|-------|---------|----------------|
| `freshness_lag_hours` | Time since last successful update | Sev2 if > 24h |
| `missing_partition_count` | Expected partitions not delivered | Sev1 if > 0 |

Business risk:

- stale data becomes incorrect enterprise truth

---

### 2. Data Quality Failures

| Metric | Meaning | Alert Condition |
|-------|---------|----------------|
| `dq_failed_rule_count` | Number of failed DQ rules | Sev1 if > 0 (critical rules) |
| `dq_failure_rate` | % of checks failing | Sev2 if > 5% |

Linked artifact:

- Rule definitions come from **F2 — DQ Rules Catalog**

---

### 3. Schema / Contract Drift

| Metric | Meaning | Alert Condition |
|-------|---------|----------------|
| `schema_drift_detected` | Contract mismatch found | Sev1 immediately |
| `unexpected_column_count` | New fields appear without version bump | Sev1 |

Linked artifact:

- Contract enforcement comes from **F5 — Data Contracts**

---

### 4. Pipeline Execution Health

| Metric | Meaning | Alert Condition |
|-------|---------|----------------|
| `job_success_rate` | % of successful runs | Sev2 if < 95% |
| `job_runtime_anomaly` | Runtime deviates from baseline | Sev3 investigation |

Governance requirement:

- Every run must produce evidence metadata.

---

### 5. Decision Readiness Signals

| Metric | Meaning | Alert Condition |
|-------|---------|----------------|
| `decision_ready_flag` | Dataset meets minimum governance requirements | Sev1 if false |
| `consumer_blocked_count` | Downstream usage blocked due to failures | Sev2 |

Key question:

> Can this dataset be trusted *right now* for decisions?

---

## Alert Payload Requirements (Audit Evidence)

Every alert must include the following fields:

| Field | Required |
|------|----------|
| dataset_name | ✅ |
| run_id / job_id | ✅ |
| timestamp | ✅ |
| failed_rule_id (if applicable) | ✅ |
| severity | ✅ |
| owner_contact | ✅ |
| contract_version | ✅ |
| lineage_reference | ✅ |
| runbook_url (F4) | ✅ |

Example alert annotation:

```yaml
dataset: yield_monitoring.daily
severity: Sev1
failed_rule: DQ-C-01
contract_version: v1.0
runbook_url: ./04-incident-response-playbook.md
```
---

## Severity & Routing Rules

| Severity | Trigger Example | Response |
|---------|----------------|----------|
| **Sev1** | Schema drift, critical DQ failure | Stop serving + open incident ticket |
| **Sev2** | Freshness lag > SLA | Investigate within SLA window |
| **Sev3** | Minor anomalies | Track for improvement |

### Routing Ownership

- **Producer Owner** (upstream responsibility)  
- **Data Reliability Owner** (controls + evidence)  
- **Consumer Owner** (impact confirmation)

Rule:

> No owner → no alert routing → no governance.

---

## Minimal Automation: Alert → Ticket → Playbook

1. Alert fired (monitoring)  
2. Ticket automatically created  
3. Ticket links to runbook (F4)  
4. Evidence stored for audit review  

Bridge toward **Project 2 (ELK evidence automation).**

---

## Evidence Storage (ELK Alignment)

- Elasticsearch (searchable evidence)
- Kibana dashboards (audit visibility)
- Logstash pipelines (structured alerts)

---

## Key Principle

> Governance controls are only real if they are monitored.

