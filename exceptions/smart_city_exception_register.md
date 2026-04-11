# Smart City Exception Register

## Purpose

This register records active and reviewable Smart City reliability exceptions identified from telemetry, curated metrics, and runtime evidence.

It is intended to support:

- monthly governance review
- exception ownership and tracking
- scorecard interpretation
- escalation decisions
- future board reporting

This register is based on current evidence available in:

- `evidence/smart-city/pipeline_run_log.csv/`
- `evidence/smart-city/pipeline_trace.csv/`
- `evidence/smart-city/pipeline_metrics.csv/`
- `evidence/smart-city/quality_metrics_daily.csv/`
- `evidence/smart-city/freshness_metrics.csv/`
- `evidence/smart-city/error_log.csv/`
- `evidence/smart-city/runtime/`

---

## Exception status model

- **Open**: issue is active and requires review or remediation
- **Monitoring**: issue is not yet closed, but immediate escalation is not required
- **Mitigated**: immediate risk reduced, pending confirmation
- **Closed**: no longer an active governance concern

---

## Active exceptions

## SC-EX-001 — Freshness stale condition across reviewed outputs

**Category**: Timeliness exception  
**Status**: Open  
**Severity**: Red  
**First observed**: 2026-04-08  
**Evidence sources**:
- `freshness_metrics.csv`
- `smart_city_reliability_summary.md`

**Observed signal**
- `freshness_status = stale`
- very large `freshness_lag_minutes` values in reviewed sample rows

**Governance interpretation**
Smart City may successfully emit telemetry and curated outputs while still failing timeliness expectations for downstream trust.

This is not only a run-level issue. It is a direct data usefulness and timeliness issue.

**Risk statement**
Downstream users may interpret Smart City outputs as current when the reviewed freshness evidence indicates stale conditions.

**Required review**
- identify worst affected `city` / `pollutant` combinations
- determine whether lag is source-driven, ingestion-driven, or transformation-driven
- confirm whether stale outputs should block downstream trust claims

**Suggested owner**
- Domain owner: TBD
- Technical owner: TBD

**Next action**
- aggregate `freshness_metrics.csv` by `city` and `pollutant`
- identify persistence and spread of stale status
- decide whether formal timeliness SLO breach should be declared

---

## SC-EX-002 — Repeated Silver-stage failures

**Category**: Operational reliability / implementation stability  
**Status**: Open  
**Severity**: Amber  
**First observed**: 2026-04-08  
**Evidence sources**:
- `pipeline_run_log.csv`
- `pipeline_trace.csv`
- `error_log.csv`
- `runtime/error_events.jsonl`

**Observed signal**
Repeated failures appear in `build_silver_table`, including:
- missing pollutant-column assumptions
- unresolved `_source_file`
- `NameError`
- Spark execution failure during count

**Governance interpretation**
The Silver stage is a reliability-critical processing step and currently shows repeated instability.  
Because downstream Gold and telemetry logic depend on successful Silver outputs, Silver instability is a high-leverage reliability concern.

**Risk statement**
If Silver remains unstable, downstream outputs and telemetry interpretation become unreliable or unavailable.

**Required review**
- separate contract mismatch from code-defect failures
- determine recurrence by `error_type`
- determine whether failures are tied to specific source patterns

**Suggested owner**
- Technical owner: TBD

**Next action**
- group `error_log` by `step_name = build_silver_table`
- classify failures into schema, implementation, and runtime buckets
- track recurrence count across runs

---

## SC-EX-003 — Gold dependency failure due to missing Silver artifact

**Category**: Dependency-chain exception  
**Status**: Open  
**Severity**: Amber  
**First observed**: 2026-04-08  
**Evidence sources**:
- `pipeline_run_log.csv`
- `pipeline_trace.csv`
- `error_log.csv`

**Observed signal**
`build_gold_hourly_table` fails with:
- `[PATH_NOT_FOUND] ... data/silver/air_quality_long`

**Governance interpretation**
This indicates that Gold reliability depends directly on Silver artifact availability and that dependency handling is fragile.

**Risk statement**
Gold-layer outputs cannot be treated as reliably available when upstream Silver artifacts are missing.

**Required review**
- confirm whether Gold is expected to hard-fail when Silver is unavailable
- define downstream trust stance when Silver generation fails
- assess whether failed upstream stages should automatically block Gold claims

**Suggested owner**
- Technical owner: TBD

**Next action**
- document dependency-chain policy between Silver and Gold
- track repeated `PATH_NOT_FOUND` occurrences as dependency reliability evidence

---

## SC-EX-004 — Telemetry rollup correctness instability

**Category**: Observability / telemetry exception  
**Status**: Open  
**Severity**: Amber  
**First observed**: 2026-04-08  
**Evidence sources**:
- `pipeline_run_log.csv`
- `pipeline_trace.csv`
- `error_log.csv`
- `runtime/error_events.jsonl`
- `runtime/span_events.jsonl`

**Observed signal**
`build_telemetry_metrics` shows multiple failure modes, including:
- unresolved `event_ts`
- timestamp parsing failure
- unresolved `ingestion_ts`

**Governance interpretation**
The telemetry layer exists and is already useful, but it is not yet fully stable or schema-safe.  
This means governance can use telemetry evidence, but should do so with a maturity caveat.

**Risk statement**
The measurement system itself may produce incomplete or inconsistent evidence, especially for freshness and rollup outputs.

**Required review**
- define canonical telemetry field requirements
- confirm expected schema for runtime event ingestion
- review whether curated telemetry outputs need validation before formal board use

**Suggested owner**
- Observability / technical owner: TBD

**Next action**
- classify telemetry rollup failures separately from core pipeline failures
- add telemetry-layer stability review to monthly governance cycle

---

## SC-EX-005 — Critical non-retryable failures present in error evidence

**Category**: Incident candidate / exception escalation  
**Status**: Open  
**Severity**: Red  
**First observed**: 2026-04-08  
**Evidence sources**:
- `error_log.csv`
- `runtime/error_events.jsonl`

**Observed signal**
Reviewed error rows show:
- `severity = critical`
- `retryable = false`

Observed error types include:
- `AnalysisException`
- `ValueError`
- `DateTimeException`
- `NameError`
- `Py4JJavaError`

**Governance interpretation**
Critical non-retryable failures should not be treated as low-priority noise.  
They are direct candidates for exception escalation and, where recurring, incident review.

**Risk statement**
Repeated critical non-retryable failures weaken operational trust and suggest unresolved systemic issues.

**Required review**
- count recurrence by `error_type`
- count recurrence by `step_name`
- identify which critical failures are implementation-driven versus contract-driven

**Suggested owner**
- Governance owner: TBD
- Technical owner: TBD

**Next action**
- open incident candidate review for recurring critical failures
- tie recurrence thresholds to exception rule escalation

---

## SC-EX-006 — Evidence integrity concerns in curated run history

**Category**: Evidence integrity exception  
**Status**: Monitoring  
**Severity**: Amber  
**First observed**: 2026-04-08  
**Evidence sources**:
- `pipeline_run_log.csv`
- `pipeline_trace.csv`

**Observed signal**
Reviewed curated evidence shows signs of measurement inconsistency, including:
- negative `duration_ms`
- repeated rollup-related run entries
- mixed success/failure states across similar rollup sequences

**Governance interpretation**
The issue is not only pipeline reliability, but evidence reliability.  
If the telemetry history is not normalized, scorecard and board interpretation may become misleading.

**Risk statement**
Governance conclusions may be distorted unless run history is normalized before review.

**Required review**
- define run deduplication or normalization policy
- determine how repeated rollup runs should be represented in scorecards
- avoid simple raw-count interpretation without cleanup rules

**Suggested owner**
- Governance owner: TBD
- Observability owner: TBD

**Next action**
- define evidence normalization rules before formal recurring board reporting
- review whether negative duration rows should be excluded or separately flagged

---

## Monitoring items

## SC-MON-001 — Quality metrics look healthy in reviewed sample
**Category**: Quality monitoring  
**Status**: Monitoring  
**Severity**: Green / Amber pending aggregation  
**Evidence sources**:
- `quality_metrics_daily.csv`

**Observed signal**
Sample rows show:
- `pass_rate = 1.0`
- `null_rate = 0.0`
- `duplicate_rate = 0.0`
- `stale_rate = 0.0`
- `outlier_rate = 0.0`
- `flagged_rate = 0.0`
- `rejected_rate = 0.0`
- `quality_status = pass`

**Interpretation**
This is promising, but sample evidence alone is not enough to declare full quality health across the review period.

**Next action**
- aggregate by `metric_date`, `city`, and `pollutant`
- confirm whether strong sample quality generalizes across the full evidence set

---

## Summary view

| Exception ID | Title | Category | Status | Severity |
|---|---|---|---|---|
| SC-EX-001 | Freshness stale condition across reviewed outputs | Timeliness | Open | Red |
| SC-EX-002 | Repeated Silver-stage failures | Operational reliability | Open | Amber |
| SC-EX-003 | Gold dependency failure due to missing Silver artifact | Dependency-chain | Open | Amber |
| SC-EX-004 | Telemetry rollup correctness instability | Observability / telemetry | Open | Amber |
| SC-EX-005 | Critical non-retryable failures present in error evidence | Incident candidate | Open | Red |
| SC-EX-006 | Evidence integrity concerns in curated run history | Evidence integrity | Monitoring | Amber |
| SC-MON-001 | Quality metrics look healthy in reviewed sample | Quality monitoring | Monitoring | Green / Amber |

---

## Recommended next governance actions

### Immediate
- confirm whether freshness exception should remain Red after full aggregation
- count recurring critical errors by `step_name` and `error_type`
- separate Silver failures into:
  - schema contract issues
  - implementation defects
  - runtime/platform issues

### Before next review cycle
- populate `scorecards/smart_city_scorecard.yaml` with observed values
- align exception register with `smart_city_exception_rules.yaml`
- define evidence normalization rules for repeated rollup runs

### Before board reporting
- confirm whether telemetry rollup evidence is stable enough for executive summary use
- decide whether timeliness risk requires explicit downstream usage caution

---

## Conclusion

Smart City now has enough telemetry and curated evidence to support a real exception register.

The current register shows that the domain’s key governance concerns are not only operational failure, but also:

- stale timeliness
- dependency fragility
- telemetry correctness instability
- critical non-retryable failure recurrence
- evidence integrity concerns

This register should now become the working bridge between raw telemetry and formal governance review.