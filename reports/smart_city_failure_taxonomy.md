# Smart City Failure Taxonomy

## Purpose

This document classifies observed Smart City telemetry failures into governance-relevant reliability categories.

The goal is not to restate raw logs, but to translate repeated runtime and telemetry failures into a structured failure taxonomy that supports:

- scorecard interpretation
- exception review
- incident candidate review
- remediation prioritization
- monthly governance board reporting

This taxonomy is based on both:

- raw historical runtime and curated evidence, and
- cleaned governance analysis outputs used for recurring review

Primary evidence sources include:

- `evidence/smart-city/pipeline_run_log.csv/`
- `evidence/smart-city/pipeline_trace.csv/`
- `evidence/smart-city/pipeline_metrics.csv/`
- `evidence/smart-city/error_log.csv/`
- `evidence/smart-city/runtime/error_events.jsonl`
- `evidence/smart-city/runtime/run_events.jsonl`
- `evidence/smart-city/runtime/span_events.jsonl`
- `reports/generated/smart_city_observed_metrics.json`
- `reports/smart_city_observed_metrics.md`

Where cleaned observed metrics differ from raw log history, recurring governance interpretation should prefer the cleaned analysis outputs.

---

## Reliability interpretation model

Observed failures should be interpreted in layers:

1. **Data contract / schema failures**  
   The pipeline expects fields, columns, or structural patterns that are not present.

2. **Dependency / artifact-chain failures**  
   Downstream steps fail because expected upstream outputs are missing.

3. **Transformation or implementation defects**  
   The code path itself contains logic or naming defects.

4. **Telemetry rollup and observability defects**  
   The telemetry-producing layer exists, but it is not yet fully reliable or schema-stable.

5. **Platform / runtime execution failures**  
   Failures occur in Spark or execution infrastructure rather than from explicit business logic.

This classification is useful because governance actions differ by category.

---

## Failure categories

## 1. Schema contract failures

### Definition
Failures caused by unresolved columns, missing expected fields, or mismatched structural assumptions.

### Evidence examples
Observed error types and messages include:

- `AnalysisException`
- unresolved column: `event_ts`
- unresolved column: `_source_file`
- unresolved column: `ingestion_ts`
- missing expected pollutant columns:
  - `No pollutant columns found. Expected one of co/no2/o3/so2 or explicit value+pollutant fields.`

### Affected steps
- `build_silver_table`
- `build_telemetry_metrics`

### Governance interpretation
These failures indicate that the producing data or the transformation logic is not aligned with the expected contract.

This is not just a transient run failure. It is a **contract reliability issue**.

### Likely governance risk
- repeated failed runs
- unstable data onboarding
- telemetry outputs that may be incomplete or misleading
- inability to claim reliable schema-controlled processing

### Suggested governance action
- classify as **contract exception candidate**
- require explicit schema expectation documentation
- require upstream/downstream field mapping review
- track recurrence in scorecard

---

## 2. Dependency and artifact-chain failures

### Definition
Failures caused by downstream steps expecting an upstream artifact that was not successfully created.

### Evidence examples
Observed message:

- `[PATH_NOT_FOUND] Path does not exist: ... data/silver/air_quality_long`

### Affected steps
- `build_gold_hourly_table`
- downstream reads from Silver outputs

### Governance interpretation
This category indicates that pipeline stage coupling is real and operationally significant.

The failure is not necessarily in Gold logic itself.  
It often means:
- Silver did not complete successfully, or
- artifact dependency handling is too fragile.

### Likely governance risk
- downstream outputs become unavailable
- Gold-layer reporting cannot be trusted
- failure propagation across stages
- cascading reliability degradation

### Suggested governance action
- classify as **dependency-chain reliability issue**
- review upstream artifact dependency handling
- ensure failed upstream stage clearly blocks downstream claims
- include dependency risk in board pack

---

## 3. Telemetry rollup correctness failures

### Definition
Failures in the telemetry and curated observability layer itself.

### Evidence examples
Observed issues include:

- unresolved `event_ts`
- timestamp parsing failure:
  - `CANNOT_PARSE_TIMESTAMP`
- unresolved `ingestion_ts`
- partial success followed by later failed rollup attempts

### Affected steps
- `build_telemetry_metrics`
- `read_runtime_events`
- `rollup_telemetry`
- `emit_freshness_metrics`
- `write_curated_telemetry`

### Governance interpretation
This is a particularly important category for this repository.

The telemetry layer exists and is valuable, but it is **not yet fully reliable as a measurement system**.

This means the governance layer must treat telemetry as useful but still maturing.

### Likely governance risk
- curated operational evidence may be partially inconsistent across runs
- derived metrics may contain correctness defects
- freshness outputs may fail even when run logging succeeds
- observability itself becomes a source of reliability risk

### Suggested governance action
- classify as **observability-control weakness**
- distinguish engineering-pipeline health from telemetry-rollup health
- require explicit validation checks for telemetry layer
- treat repeated telemetry rollup failure as governance-visible risk

---

## 4. Transformation implementation defects

### Definition
Failures caused by code-level defects, variable naming mistakes, or transformation logic bugs.

### Evidence examples
Observed messages include:

- `name 'ruㄈn_id' is not defined`
- `name 'silver_count' is not defined`

### Affected steps
- `build_silver_table`

### Governance interpretation
These are not source-data problems.  
They are implementation defects in the transformation logic.

This category is useful because it should not be mislabeled as upstream data quality failure.

### Likely governance risk
- avoidable operational instability
- repeated production-like incidents caused by code hygiene
- unreliable deployment confidence

### Suggested governance action
- classify as **engineering implementation defect**
- require fix owner and closure tracking
- distinguish from source-quality exceptions
- consider recurrence count for severity escalation

---

## 5. Platform or runtime execution failures

### Definition
Failures caused by Spark execution problems, engine instability, cache/execution plan problems, or low-level runtime exceptions.

### Evidence examples
Historical runtime evidence includes:

- `Py4JJavaError`
- Spark internal execution failure
- internal error during `count`
- Spark plan/session/cache related exception chain

### Affected steps
- `build_silver_table`

### Governance interpretation
These failures may not reflect bad source data or bad contract assumptions.  
They may indicate instability in the execution environment, Spark usage pattern, or interaction with caching / query execution.

These issues are visible in historical runtime evidence, even though they are less dominant in the current cleaned error snapshot.

### Likely governance risk
- unstable reruns
- low operational predictability
- difficult incident triage
- elevated support burden

### Suggested governance action
- classify as **runtime/platform incident candidate**
- distinguish from business-data reliability issues
- track recurrence separately from data-quality exceptions
- review whether platform hardening is required

---

## 6. Freshness and timeliness failures

### Definition
Failures where data is present but not timely enough for trustworthy downstream use.

### Evidence examples
Observed in curated outputs and cleaned analysis:

- `freshness_status = stale`
- very large `freshness_lag_minutes`

### Affected outputs
- `freshness_metrics.csv`
- `reports/generated/smart_city_observed_metrics.json`

### Governance interpretation
This category is distinct from run failure.

The pipeline may complete successfully and still fail timeliness expectations.  
That makes freshness a **governance risk even when operational success exists**.

### Likely governance risk
- stale downstream analytics
- invalid trust assumptions for consumers
- mismatch between “pipeline success” and “data usefulness”

### Suggested governance action
- classify as **timeliness exception**
- escalate if stale conditions are widespread or persistent
- include freshness separately in scorecard instead of hiding under run success

---

## 7. Measurement inconsistency and temporal integrity issues

### Definition
Failures or anomalies where operational evidence appears internally inconsistent across timestamps, durations, or repeated rollups.

### Evidence examples
Observed in curated run logs and evidence cleanup work:

- negative `duration_ms`
- repeated `run_rollup_runtime` rows with conflicting success/failure outcomes
- same logical run family appearing across multiple rollup attempts
- malformed or invalid rows requiring filtering during cleaned governance analysis

### Governance interpretation
This category matters because it affects **trust in the evidence itself**.

The question is no longer only “did the pipeline fail?”  
It becomes “can governance reliably interpret this telemetry snapshot?”

### Likely governance risk
- ambiguous incident history
- misleading runtime trend analysis
- scorecard instability if evidence is not normalized

### Suggested governance action
- classify as **evidence integrity issue**
- define normalization rules before monthly board reporting
- avoid raw-count interpretation without run-dedup, filtering, or rollup logic

---

## Failure-to-governance mapping

| Failure category | Main governance impact | Typical severity posture | Primary outputs affected |
|---|---|---|---|
| Schema contract failures | Contract exception | Amber / Red | Silver, telemetry rollup |
| Dependency and artifact-chain failures | Stage dependency risk | Amber / Red | Gold outputs |
| Telemetry rollup correctness failures | Observability reliability risk | Amber / Red | Curated telemetry evidence |
| Transformation implementation defects | Engineering defect risk | Amber | Silver stability |
| Platform/runtime execution failures | Incident candidate | Amber / Red | Run stability |
| Freshness and timeliness failures | Timeliness exception | Red | Freshness scorecard |
| Measurement inconsistency | Evidence trust issue | Amber | Scorecard / board pack reliability |

---

## Current dominant patterns in Smart City

Based on the currently reviewed evidence, the dominant failure patterns are:

1. **Persistent timeliness concern**
   - stale freshness signals across all valid reviewed freshness rows
   - very high freshness lag values

2. **Silver-stage operational instability**
   - repeated failures centered on `build_silver_table`

3. **Schema and contract mismatch**
   - unresolved columns
   - missing pollutant assumptions
   - telemetry field mismatches

4. **Dependency-chain fragility**
   - Gold step failing because Silver artifact is unavailable

5. **Telemetry-layer instability**
   - telemetry rollup failures remain governance-visible
   - telemetry evidence is useful but not yet fully stable

This means the domain is not suffering from only one isolated defect.  
It shows a **mixed reliability profile** across:
- transformation stability
- dependency robustness
- telemetry correctness
- timeliness
- evidence integrity

---

## Governance implications

### 1. Run success alone is not enough
A successful run does not guarantee:
- good freshness
- valid telemetry rollup
- reliable downstream trust

### 2. Telemetry itself must be governed
Because telemetry rollup has its own failure modes, governance must review:
- pipeline reliability
- telemetry reliability

as related but distinct concerns.

### 3. Exceptions should be categorized, not lumped together
Not all failures should enter the same bucket.

Recommended separation:
- contract exceptions
- timeliness exceptions
- implementation defects
- platform/runtime incidents
- evidence-integrity issues

### 4. Board reporting should surface mixed status
Smart City should not be summarized as simply “working” or “failing.”

A more accurate current posture is:
- **Data quality: Green**
- **Freshness / timeliness: Red**
- **Operational reliability: Amber**
- **Incident / exception posture: Amber-Red**
- **Evidence integrity: Amber**

---

## Recommended next governance actions

### Immediate
- map all current `error_type` and `step_name` combinations into this taxonomy
- tag current open issues by category
- separate timeliness risk from run reliability risk

### Next review cycle
- compute counts by failure category
- compute counts by affected step
- identify recurring versus one-off failures
- distinguish implementation defects from source or contract defects

### Board-level reporting
Include:
- top recurring failure category
- top affected step
- whether freshness remains red
- whether telemetry rollup itself is stable enough for executive reporting

---

## Suggested follow-on artifacts

This taxonomy should feed:

- `scorecards/smart_city_scorecard.yaml`
- `exceptions/smart_city_exception_rules.yaml`
- `exceptions/smart_city_exception_register.md`
- `governance/monthly_review_smart_city.md`

---

## Conclusion

Smart City telemetry is already valuable enough for governance use, but the failure evidence shows that the domain is still in a reliability-maturing state.

The most important governance insight is not merely that failures exist.

It is that failures cluster into identifiable patterns:

- contract mismatch
- dependency propagation
- telemetry correctness weakness
- implementation defects
- timeliness risk
- evidence integrity concerns

That classification is what allows this repository to move from storing telemetry to governing reliability.