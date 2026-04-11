# Smart City Reliability Summary

## Scope

This summary reviews Smart City pilot reliability evidence currently stored in:

- `evidence/smart-city/pipeline_run_log.csv/`
- `evidence/smart-city/quality_metrics_daily.csv/`
- `evidence/smart-city/freshness_metrics.csv/`
- `evidence/smart-city/error_log.csv/`
- `evidence/smart-city/runtime/`

The purpose of this review is to convert upstream telemetry and quality outputs into governance-ready reliability evidence for:
- scorecards
- exception review
- incident threshold validation
- monthly board reporting

---

## Current governance interpretation

Smart City is now usable as the first governed pilot domain in this repository because it already produces evidence for:

- run-level execution status
- runtime duration and failure status
- quality metrics by city and pollutant
- freshness lag and stale-data signals
- structured error records with severity and retryability
- raw runtime event evidence for deeper traceability

This means Smart City is no longer only a pipeline implementation example. It can now support evidence-based reliability review.

---

## Evidence reviewed

### 1. Pipeline run log
Observed columns:
- `run_id`
- `trace_id`
- `pipeline_name`
- `started_at`
- `finished_at`
- `duration_ms`
- `status`
- `rows_in`
- `rows_out`
- `rows_flagged`
- `rows_rejected`
- `error_count`
- `artifact_path`
- `error_message`

Governance interpretation:
- supports run success/failure review
- supports runtime trend review
- supports failed-run inventory
- supports linking failed runs to affected artifacts and error messages

Current evidence note:
- at least some runs failed during the reviewed snapshot
- observed failure reasons include schema/field-shape problems and Spark internal execution failure messages

---

### 2. Quality metrics daily
Observed columns:
- `metric_date`
- `run_id`
- `city`
- `pollutant`
- `total_records`
- `null_rate`
- `duplicate_rate`
- `stale_rate`
- `outlier_rate`
- `flagged_rate`
- `rejected_rate`
- `pass_rate`
- `quality_status`

Governance interpretation:
- supports daily quality KPI review
- supports duplicate / stale / outlier / rejection monitoring
- supports city-level and pollutant-level quality review
- supports quality status rollup

Current evidence note:
- sample rows show `pass_rate = 1.0`
- sample rows show all listed quality defect rates at `0.0`
- sample rows show `quality_status = pass`

Interpretation caution:
- these sample rows look strong, but governance review should not assume the entire dataset is uniformly healthy without aggregate rollup

---

### 3. Freshness metrics
Observed columns:
- `metric_ts`
- `run_id`
- `city`
- `pollutant`
- `latest_observed_at`
- `latest_ingested_at`
- `freshness_lag_minutes`
- `freshness_status`

Governance interpretation:
- supports timeliness SLO review
- supports stale-data detection
- supports city/pollutant freshness risk review

Current evidence note:
- sample rows show very high `freshness_lag_minutes`
- sample rows are labeled `freshness_status = stale`

Interpretation:
- freshness is currently the clearest governance risk visible in the available sample evidence
- Smart City may be operationally producing telemetry while still failing timeliness expectations for upstream data currency

---

### 4. Error log
Observed columns:
- `error_ts`
- `run_id`
- `trace_id`
- `span_id`
- `pipeline_name`
- `step_name`
- `city`
- `pollutant`
- `batch_month`
- `source_name`
- `error_type`
- `error_message`
- `retryable`
- `severity`

Governance interpretation:
- supports incident candidate review
- supports recurring error signature analysis
- supports severity-based exception handling
- supports stage-specific remediation tracking

Current evidence note:
- sample rows show `severity = critical`
- observed error types include `AnalysisException` and `ValueError`
- observed errors include unresolved-column failure and missing pollutant-column failure
- sample rows show `retryable = false` for critical failures

Interpretation:
- non-retryable critical failures should be treated as strong exception or incident-review candidates
- remediation should focus on schema contract enforcement and transformation robustness

---

### 5. Raw runtime evidence
Files:
- `runtime/run_events.jsonl`
- `runtime/span_events.jsonl`
- `runtime/metric_events.jsonl`
- `runtime/error_events.jsonl`

Governance interpretation:
- supports forensic reconstruction of failures
- supports trace validation against curated summaries
- supports auditability for exception review and incident deep dive

---

## Initial reliability view

### Strengths
- Smart City now emits structured run, quality, freshness, and error evidence
- data quality metrics appear formally modeled and reviewable
- error records include severity and retryability fields, which is useful for governance escalation
- raw runtime evidence exists for audit and traceability

### Concerns
- run-level evidence shows failed executions in the reviewed snapshot
- error evidence includes critical and non-retryable failures
- freshness evidence shows stale status and extremely high lag values in the reviewed sample
- telemetry rollup and metric-building logic may still be sensitive to schema inconsistencies

### Most likely current governance posture
**Amber / Red boundary**

Reasoning:
- the domain is strong enough to support governance review
- however, available sample evidence shows clear operational and freshness risk
- if stale freshness is widespread rather than isolated, the domain should likely be treated as **Red for timeliness**
- if run failures are recurring rather than isolated, the domain should likely be **Amber or Red for operational reliability**

---

## Preliminary domain assessment by dimension

### Operational reliability
Status: **Amber**

Reason:
- run failures are visible in pipeline execution evidence
- error logs show critical failures tied to specific processing steps
- remediation is needed before claiming stable operational reliability

### Data quality
Status: **Green / Amber pending aggregate validation**

Reason:
- sample quality rows look clean
- pass rates in the sample are strong
- final status should depend on full-period aggregation, not sample rows only

### Freshness
Status: **Red**

Reason:
- reviewed sample rows show `freshness_status = stale`
- lag values are extremely high in the sample evidence
- this represents a direct timeliness governance concern

### Incident / exception readiness
Status: **Amber**

Reason:
- evidence is now sufficient to support exception handling
- however, exception rules and review workflow still need to be operationalized in this repository

---

## Recommended immediate governance actions

### 1. Formalize scorecard population
Populate the Smart City scorecard with observed values from:
- `pipeline_run_log.csv`
- `quality_metrics_daily.csv`
- `freshness_metrics.csv`
- `error_log.csv`

### 2. Open initial freshness exception review
Because sample evidence already shows stale freshness conditions, create a first exception review focused on:
- cities and pollutants with the worst lag
- whether lag is source-driven or pipeline-driven
- whether stale data should block downstream trust claims

### 3. Review recurring critical failures
Group `error_log` entries by:
- `step_name`
- `error_type`
- `error_message`
- `severity`
- `retryable`

This should identify whether failures are:
- one-off implementation defects
- recurring contract mismatches
- systemic pipeline reliability issues

### 4. Tighten upstream schema controls
Observed failures suggest that Smart City still needs stronger validation for:
- pollutant column expectations
- telemetry event schema consistency
- rollup metric input assumptions

### 5. Produce first pilot scorecard and exception register
This repository should next create:
- `scorecards/smart_city_scorecard.yaml`
- `exceptions/smart_city_exception_rules.yaml`
- a first populated exception register or review note

---

## Reliability review conclusion

Smart City has reached the point where telemetry is useful for governance, not only for engineering debugging.

The current evidence shows that:
- governance review is now possible
- data quality evidence is structured and promising
- freshness is a likely high-priority risk area
- critical pipeline failures remain relevant and should not be treated as isolated until trend analysis confirms otherwise

The next meaningful step is to convert this evidence into:
- a populated scorecard
- explicit exception triggers
- a recurring monthly review workflow

Until those are populated with observed values, Smart City should be treated as a **pilot governed domain with active reliability risk under review**.