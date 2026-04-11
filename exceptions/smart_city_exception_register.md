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
- `reports/generated/smart_city_observed_metrics.json`

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
**Last reviewed**: 2026-04-11  
**Owner**: TBD  
**Due date**: TBD  
**Evidence sources**:
- `freshness_metrics.csv`
- `reports/smart_city_observed_metrics.md`
- `reports/generated/smart_city_observed_metrics.json`

**Observed signal**
- `freshness_status = stale`: 8 valid rows
- avg `freshness_lag_minutes`: 409828.51
- max `freshness_lag_minutes`: 638303.30

**Governance interpretation**
Smart City may successfully emit telemetry and curated outputs while still failing timeliness expectations for downstream trust.

This is not only a run-level issue. It is a direct data usefulness and timeliness issue.

**Risk statement**
Downstream users may interpret Smart City outputs as current when reviewed freshness evidence indicates severe stale conditions.

**Current response**
- freshness retained as explicit Red domain concern
- issue kept separate from operational success/failure

**Required review**
- identify worst affected `city` / `pollutant` combinations
- determine whether lag is source-driven, ingestion-driven, or transformation-driven
- confirm whether stale outputs should block downstream trust claims

**Closure criteria**
- freshness no longer shows all-valid-row stale status
- lag returns to an explicitly accepted threshold
- governance review accepts timeliness posture as no longer Red

**Next action**
- aggregate `freshness_metrics.csv` by `city` and `pollutant`
- decide whether a formal timeliness SLO breach statement should be added to monthly review

---

## SC-EX-002 — Repeated Silver-stage failures

**Category**: Operational reliability / implementation stability  
**Status**: Open  
**Severity**: Amber  
**First observed**: 2026-04-08  
**Last reviewed**: 2026-04-11  
**Owner**: TBD  
**Due date**: TBD  
**Evidence sources**:
- `pipeline_run_log.csv`
- `pipeline_trace.csv`
- `error_log.csv`
- `runtime/error_events.jsonl`
- `reports/generated/smart_city_observed_metrics.json`

**Observed signal**
`build_silver_table` appears as the top cleaned step-level failure hotspot:
- `build_silver_table`: 5 valid error rows

Observed failure types include:
- `ValueError`
- `NameError`
- `AnalysisException`

**Governance interpretation**
The Silver stage is a reliability-critical processing step and currently shows repeated instability. Because downstream Gold and telemetry logic depend on successful Silver outputs, Silver instability is a high-leverage reliability concern.

**Risk statement**
If Silver remains unstable, downstream outputs and telemetry interpretation become unreliable or unavailable.

**Current response**
- Silver retained as the main operational hotspot in the scorecard
- issue remains active in monthly review

**Required review**
- separate contract mismatch from code-defect failures
- determine recurrence by `error_type`
- determine whether failures are tied to specific source patterns

**Closure criteria**
- no repeated Silver-stage critical failures across review cycle
- operational review no longer identifies Silver as the dominant hotspot
- dependency failures into Gold materially reduce

**Next action**
- group `error_log` by `step_name = build_silver_table`
- classify failures into schema, implementation, and runtime buckets
- assign remediation owner

---

## SC-EX-003 — Gold dependency failure due to missing Silver artifact

**Category**: Dependency-chain exception  
**Status**: Open  
**Severity**: Amber  
**First observed**: 2026-04-08  
**Last reviewed**: 2026-04-11  
**Owner**: TBD  
**Due date**: TBD  
**Evidence sources**:
- `pipeline_run_log.csv`
- `pipeline_trace.csv`
- `error_log.csv`
- `reports/generated/smart_city_observed_metrics.json`

**Observed signal**
`build_gold_hourly_table` appears with:
- `build_gold_hourly_table | AnalysisException`: 3

Observed error pattern:
- `[PATH_NOT_FOUND] ... data/silver/air_quality_long`

**Governance interpretation**
This indicates Gold reliability depends directly on Silver artifact availability and that dependency handling is fragile.

**Risk statement**
Gold-layer outputs cannot be treated as reliably available when upstream Silver artifacts are missing.

**Current response**
- dependency fragility remains visible in failure taxonomy and scorecard
- Gold is not treated as independently healthy while Silver is unstable

**Required review**
- confirm whether Gold is expected to hard-fail when Silver is unavailable
- define downstream trust stance when Silver generation fails
- assess whether failed upstream stages should automatically block Gold claims

**Closure criteria**
- dependency-chain failures are not observed across review cycle
- Gold no longer fails due to missing Silver artifacts
- dependency policy is documented and accepted

**Next action**
- document dependency-chain policy between Silver and Gold
- track repeated `PATH_NOT_FOUND` occurrences as dependency reliability evidence

---

## SC-EX-004 — Telemetry rollup correctness instability

**Category**: Observability / telemetry exception  
**Status**: Open  
**Severity**: Amber  
**First observed**: 2026-04-08  
**Last reviewed**: 2026-04-11  
**Owner**: TBD  
**Due date**: TBD  
**Evidence sources**:
- `pipeline_run_log.csv`
- `pipeline_trace.csv`
- `error_log.csv`
- `runtime/error_events.jsonl`
- `runtime/span_events.jsonl`
- `reports/generated/smart_city_observed_metrics.json`

**Observed signal**
`build_telemetry_metrics`: 3 valid cleaned error rows

Observed failure types include:
- `AnalysisException`
- `DateTimeException`

**Governance interpretation**
The telemetry layer exists and is already useful, but it is not yet fully stable or schema-safe. Governance can use telemetry evidence, but should do so with a maturity caveat.

**Risk statement**
The measurement system itself may produce incomplete or inconsistent evidence, especially for freshness and rollup outputs.

**Current response**
- telemetry instability remains governance-visible
- not collapsed into generic pipeline failure

**Required review**
- define canonical telemetry field requirements
- confirm expected schema for runtime event ingestion
- review whether curated telemetry outputs need validation before formal board use

**Closure criteria**
- telemetry rollup no longer produces repeated cleaned critical failures
- evidence normalization and rollup outputs are stable across review cycles
- governance accepts telemetry layer as stable enough for recurring reporting

**Next action**
- classify telemetry rollup failures separately from core pipeline failures
- add telemetry-layer stability review to each monthly governance cycle

---

## SC-EX-005 — Critical non-retryable failures present in error evidence

**Category**: Incident candidate / exception escalation  
**Status**: Open  
**Severity**: Red  
**First observed**: 2026-04-08  
**Last reviewed**: 2026-04-11  
**Owner**: TBD  
**Due date**: TBD  
**Evidence sources**:
- `error_log.csv`
- `runtime/error_events.jsonl`
- `reports/generated/smart_city_observed_metrics.json`

**Observed signal**
Cleaned analysis shows:
- valid error rows: 11
- `critical | false`: 11

**Governance interpretation**
Critical non-retryable failures should not be treated as low-priority noise. They are direct candidates for exception escalation and, where recurring, incident review.

**Risk statement**
Repeated critical non-retryable failures weaken operational trust and suggest unresolved systemic issues.

**Current response**
- retained as Red exception
- still active pending ownership and recurrence review

**Required review**
- count recurrence by `error_type`
- count recurrence by `step_name`
- identify which critical failures are implementation-driven versus contract-driven

**Closure criteria**
- critical non-retryable recurrence materially reduced
- high-severity failures have assigned remediation and closure evidence
- governance no longer considers issue incident-candidate level

**Next action**
- open incident candidate review for recurring critical failures
- tie recurrence thresholds to exception rule escalation

---

## SC-EX-006 — Evidence integrity concerns in curated run history

**Category**: Evidence integrity exception  
**Status**: Monitoring  
**Severity**: Amber  
**First observed**: 2026-04-08  
**Last reviewed**: 2026-04-11  
**Owner**: TBD  
**Due date**: TBD  
**Evidence sources**:
- `pipeline_run_log.csv`
- `pipeline_trace.csv`
- `reports/generated/smart_city_observed_metrics.json`

**Observed signal**
Cleaned analysis shows:
- valid run rows: 43
- filtered invalid run rows: 65
- valid error rows: 11
- filtered invalid error rows: 66

**Governance interpretation**
The issue is not only pipeline reliability, but evidence reliability. If telemetry history is not normalized, scorecard and board interpretation may become misleading.

**Risk statement**
Governance conclusions may be distorted unless run history is normalized before review.

**Current response**
- cleaned analysis used in place of raw blank-row counts
- evidence-integrity caution retained in scorecard

**Required review**
- define run deduplication or normalization policy
- determine how repeated rollup runs should be represented in scorecards
- avoid simple raw-count interpretation without cleanup rules

**Closure criteria**
- malformed or invalid telemetry-derived rows materially reduce
- normalization policy is documented and applied consistently
- governance can use recurring metrics without major cleanup caveat

**Next action**
- define evidence normalization rules before formal recurring board reporting
- review whether invalid rows reflect multiline error rendering, export artifact, or upstream telemetry formatting

---

## Monitoring items

## SC-MON-001 — Quality metrics look healthy in current cleaned snapshot
**Category**: Quality monitoring  
**Status**: Monitoring  
**Severity**: Green  
**Last reviewed**: 2026-04-11  
**Owner**: TBD  
**Due date**: TBD  
**Evidence sources**:
- `quality_metrics_daily.csv`
- `reports/generated/smart_city_observed_metrics.json`

**Observed signal**
Cleaned analysis shows:
- valid quality rows: 5834
- `quality_status = pass`: 5834
- avg `pass_rate = 1.0`
- avg `rejected_rate = 0.0`
- avg `duplicate_rate = 0.0`
- avg `flagged_rate = 0.0`

**Interpretation**
This is a strong positive signal for current quality posture.

**Closure criteria**
- not applicable; monitoring item remains until quality materially degrades or review model changes

**Next action**
- continue monitoring across future review cycles
- ensure strong quality posture is not used to mask freshness risk

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
| SC-MON-001 | Quality metrics look healthy in current cleaned snapshot | Quality monitoring | Monitoring | Green |

---

## Recommended next governance actions

### Immediate
- assign owners for all open exceptions
- confirm whether freshness exception remains Red after next snapshot
- count recurring critical failures by `step_name` and `error_type`
- separate Silver failures into schema, implementation, and runtime buckets

### Before next review cycle
- align exception register with refreshed scorecard values
- define evidence normalization rules for repeated rollup runs
- confirm telemetry rollup stability threshold for governance use

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

This register should remain the working bridge between raw telemetry and formal governance review.