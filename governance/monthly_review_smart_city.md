# Monthly Governance Review — Smart City

**Domain:** Smart City Air Quality  
**Review cadence:** Monthly  
**Review type:** Pilot governed domain review  
**Review status date:** 2026-04-11  
**Prepared from:** telemetry, curated operational evidence, exception register, and scorecard inputs

---

## 1. Review objective

This monthly review assesses whether Smart City is operating at a level that supports trustworthy downstream use and whether current telemetry is sufficient for governance-led reliability review.

This review focuses on four dimensions:

- operational reliability
- data quality
- freshness / timeliness
- incident and exception posture

---

## 2. Executive summary

Smart City has now reached the stage where it can be reviewed as a governed pilot domain using real telemetry and curated evidence rather than only design intent.

Current evidence shows a mixed reliability profile:

- operational telemetry exists and is rich enough for governance use
- Silver, Gold, and telemetry-related steps are observable at run and span level
- sample quality outputs look strong
- freshness signals show clear stale-data risk
- multiple critical, non-retryable failures are present in reviewed logs
- telemetry rollup itself is useful but not yet fully stable

### Current governance posture
**Overall: Amber with Red timeliness concern**

This means Smart City is mature enough to review, but not yet stable enough to describe as broadly reliable without caveats.

---

## 3. Evidence reviewed

### Curated evidence
- `evidence/smart-city/pipeline_run_log.csv/`
- `evidence/smart-city/pipeline_trace.csv/`
- `evidence/smart-city/pipeline_metrics.csv/`
- `evidence/smart-city/quality_metrics_daily.csv/`
- `evidence/smart-city/freshness_metrics.csv/`
- `evidence/smart-city/error_log.csv/`

### Raw runtime evidence
- `evidence/smart-city/runtime/run_events.jsonl`
- `evidence/smart-city/runtime/span_events.jsonl`
- `evidence/smart-city/runtime/metric_events.jsonl`
- `evidence/smart-city/runtime/error_events.jsonl`

### Governance interpretation artifacts
- `reports/smart_city_reliability_summary.md`
- `reports/smart_city_failure_taxonomy.md`
- `scorecards/smart_city_scorecard.yaml`
- `exceptions/smart_city_exception_rules.yaml`
- `exceptions/smart_city_exception_register.md`

---

## 4. Domain status by dimension

## 4.1 Operational reliability
**Status:** Amber

### What we observed
- run-level evidence includes both success and failed runs
- repeated failures are visible in `build_silver_table`
- `build_gold_hourly_table` failures occur when Silver output is unavailable
- telemetry-related rollup steps have both successful and failed executions

### Interpretation
Operational visibility is good, but stability is still mixed.  
The domain can be monitored, but not yet described as consistently reliable.

### Governance note
The most important operational concern is not a single failed run, but repeated step-level instability in core transformation paths.

---

## 4.2 Data quality
**Status:** Green / Amber pending full aggregation

### What we observed
Reviewed sample rows in `quality_metrics_daily.csv` show:
- `pass_rate = 1.0`
- `null_rate = 0.0`
- `duplicate_rate = 0.0`
- `stale_rate = 0.0`
- `outlier_rate = 0.0`
- `flagged_rate = 0.0`
- `rejected_rate = 0.0`
- `quality_status = pass`

### Interpretation
The reviewed sample is promising and suggests that quality controls are modeled and producing interpretable outputs.

### Governance note
This should remain a provisional positive signal until full-period aggregation confirms that the sample reflects overall domain behavior.

---

## 4.3 Freshness / timeliness
**Status:** Red

### What we observed
`freshness_metrics.csv` sample rows show:
- `freshness_status = stale`
- very large `freshness_lag_minutes`

### Interpretation
This is the clearest high-priority governance risk in the current Smart City evidence.

A pipeline can complete successfully and still fail timeliness expectations.  
That appears to be the case here.

### Governance note
Freshness must be reported separately from operational success.  
Timeliness risk should not be hidden inside a generic pipeline-health label.

---

## 4.4 Incident and exception posture
**Status:** Amber / Red

### What we observed
`error_log.csv` and runtime error evidence show:
- `severity = critical`
- `retryable = false`
- recurring error types including:
  - `AnalysisException`
  - `ValueError`
  - `DateTimeException`
  - `NameError`
  - `Py4JJavaError`

### Interpretation
The domain already has enough evidence to support formal exception review and incident candidate review.

### Governance note
Critical non-retryable failures should be treated as governance-visible reliability issues, not just engineering noise.

---

## 5. Most important risk themes this month

## Risk theme 1 — Timeliness risk is currently too high
Freshness evidence shows stale conditions and large lag values.  
This is currently the strongest red-domain signal.

## Risk theme 2 — Silver-stage instability has downstream impact
Repeated Silver failures create direct risk for downstream Gold availability and interpretability.

## Risk theme 3 — Telemetry is useful but still maturing
The observability layer is already valuable for governance, but telemetry rollup itself still shows correctness and schema fragility.

## Risk theme 4 — Evidence trust needs normalization
Repeated rollup attempts and inconsistent run history patterns mean governance should normalize evidence before executive-level reporting.

---

## 6. Active exceptions reviewed

The following exceptions are currently relevant:

- **SC-EX-001** — Freshness stale condition across reviewed outputs
- **SC-EX-002** — Repeated Silver-stage failures
- **SC-EX-003** — Gold dependency failure due to missing Silver artifact
- **SC-EX-004** — Telemetry rollup correctness instability
- **SC-EX-005** — Critical non-retryable failures present in error evidence
- **SC-EX-006** — Evidence integrity concerns in curated run history

Monitoring item:
- **SC-MON-001** — Quality metrics look healthy in reviewed sample

---

## 7. Governance conclusions for this cycle

### What is going well
- Smart City now emits structured reliability evidence
- telemetry is rich enough to support real governance review
- quality outputs appear modeled and interpretable
- raw runtime evidence supports traceability and forensic review

### What remains concerning
- repeated operational failures remain visible
- freshness posture is currently weak
- telemetry rollup has its own failure modes
- some failures are clearly critical and non-retryable
- evidence normalization is still needed before stronger executive reporting claims

### Current review conclusion
Smart City should continue to be treated as a **pilot governed domain under active reliability review**, not as a fully stabilized governed service.

---

## 8. Decisions and actions for next cycle

## Decision 1
Retain **Amber overall status** with explicit **Red freshness concern**.

## Decision 2
Treat timeliness as a separate governance dimension requiring explicit review each cycle.

## Decision 3
Continue using Smart City as the first governed pilot domain and as the working model for telemetry-driven governance in this repository.

### Required actions before next review
1. Aggregate `freshness_metrics.csv` by city and pollutant to quantify worst timeliness segments.
2. Aggregate `pipeline_run_log.csv` to compute run success rate and recurring failure patterns.
3. Group `error_log.csv` by `step_name`, `error_type`, `severity`, and `retryable`.
4. Normalize repeated rollup-related run history before final scorecard rollup.
5. Populate observed values into `scorecards/smart_city_scorecard.yaml`.

---

## 9. Board-facing message

Smart City is now governable using real telemetry and operational evidence.  
However, current evidence shows that:

- reliability is measurable but mixed
- timeliness is the most serious active concern
- critical operational failures still require structured follow-up
- telemetry maturity is improving, but measurement integrity must still be strengthened

The domain is therefore suitable for pilot governance review, but not yet for unqualified reliability claims.

---

## 10. Next review checkpoint

**Next review focus:**
- freshness trend confirmation
- recurring critical failure count
- Silver-stage stability
- evidence normalization for scorecard production

**Planned outputs before next cycle:**
- updated scorecard with observed values
- refreshed exception register
- normalized monthly reliability summary