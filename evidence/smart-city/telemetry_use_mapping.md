# Smart City Telemetry Use Mapping

## Purpose

This document explains how Smart City telemetry and curated operational outputs are used inside the data-reliability-framework repository.

The goal is not to duplicate pipeline implementation logic, but to convert upstream runtime and quality telemetry into governance-ready reliability evidence for:
- scorecards
- exception review
- incident threshold validation
- monthly governance board reporting

---

## Upstream evidence source

Repository:
- smart-city-air-quality-platform

Primary telemetry locations:
- `data/telemetry/curated/`
- `data/telemetry/runtime/`

Governance copy location in this repository:
- `evidence/smart-city/`
- `evidence/smart-city/runtime/`

---

## Evidence classification

### 1. Curated operational evidence

These files are intended for regular governance review and scorecard generation.

#### `pipeline_run_log.csv`
Use:
- run-level execution tracking
- success/failure rate calculation
- runtime trend monitoring
- pipeline availability review

Governance questions supported:
- How often did the pipeline run?
- What percentage of runs completed successfully?
- Are failures increasing over time?
- Are runtimes becoming unstable?

Derived indicators:
- total_runs
- successful_runs
- failed_runs
- run_success_rate
- average_runtime_seconds
- longest_runtime_seconds

---

#### `pipeline_trace.csv`
Use:
- stage-level execution analysis
- bottleneck identification
- failed stage diagnosis
- latency and flow review

Governance questions supported:
- Which stage is slowest?
- Which stage fails most often?
- Is one part of the pipeline degrading over time?

Derived indicators:
- slowest_stage
- stage_failure_count
- stage_duration_p95_seconds
- recurring_failed_stage

---

#### `pipeline_metrics.csv`
Use:
- operational metric summary
- throughput and volume review
- pipeline performance evidence

Governance questions supported:
- How much data is processed per run?
- Are output volumes stable?
- Is throughput changing unexpectedly?

Derived indicators:
- records_processed
- rows_written
- rows_dropped
- throughput_per_run

---

#### `quality_metrics_daily.csv`
Use:
- daily quality trend monitoring
- quality exception detection
- quality KPI / SLA / SLO review

Governance questions supported:
- Is data quality stable?
- Are reject or duplicate rates increasing?
- Are flagged rows trending upward?

Derived indicators:
- quality_pass_rate
- reject_rate
- flagged_rate
- duplicate_rate
- null_or_invalid_rate

---

#### `freshness_metrics.csv`
Use:
- timeliness review
- freshness KPI / SLO validation
- stale data detection

Governance questions supported:
- Is Smart City data arriving on time?
- Are freshness breaches occurring?
- Is lag persistent or isolated?

Derived indicators:
- freshness_lag_hours
- stale_day_count
- freshness_slo_attainment

---

#### `error_log.csv`
Use:
- operational issue inventory
- incident candidate review
- recurring error pattern analysis

Governance questions supported:
- What errors are recurring?
- Are critical failures unresolved?
- Which failure classes appear most often?

Derived indicators:
- error_count
- error_type_distribution
- recurring_error_signature
- critical_error_count

---

## 2. Raw runtime evidence

These files are not intended for routine board-level review. They support auditability, traceability, and incident drill-down.

#### `runtime/run_events.jsonl`
Use:
- run-level event audit trail
- execution chronology validation

#### `runtime/span_events.jsonl`
Use:
- stage/span forensic trace
- bottleneck and breakdown investigation

#### `runtime/metric_events.jsonl`
Use:
- raw metric validation
- curated metric backtracking

#### `runtime/error_events.jsonl`
Use:
- raw error validation
- incident forensic review

---

## Governance outputs supported

The Smart City telemetry set supports the following governance outputs:

### Scorecard
Primary sources:
- `pipeline_run_log.csv`
- `quality_metrics_daily.csv`
- `freshness_metrics.csv`
- `error_log.csv`

### Exception review
Primary sources:
- `quality_metrics_daily.csv`
- `freshness_metrics.csv`
- `error_log.csv`
- `pipeline_trace.csv`

### Incident threshold validation
Primary sources:
- `pipeline_run_log.csv`
- `error_log.csv`
- `runtime/error_events.jsonl`
- `runtime/span_events.jsonl`

### Monthly governance board pack
Primary sources:
- all curated evidence files
- raw runtime evidence when drill-down is required

---

## Interpretation guidance

This repository treats telemetry as governance evidence, not merely as pipeline exhaust.

Interpretation should follow this sequence:
1. Review curated operational evidence for stability, quality, freshness, and error trends.
2. Identify threshold breaches or recurring reliability patterns.
3. Escalate candidate exceptions or incidents when rules are met.
4. Use raw runtime evidence only when deeper audit or causal review is required.

---

## Current scope note

Smart City is currently the first governed domain in this repository.

Telemetry from Smart City should therefore be treated as:
- the first production-like evidence set
- the pilot input for scorecards and board review
- the reference example for future governed domains