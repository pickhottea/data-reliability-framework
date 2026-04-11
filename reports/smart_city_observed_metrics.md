# Smart City Observed Metrics

**Status date:** 2026-04-11  
**Evidence root:** `evidence/smart-city/`  
**Analysis script:** `scripts/analyze_smart_city_telemetry.py`  
**Generated JSON:** `reports/generated/smart_city_observed_metrics.json`

---

## 1. Operational run summary

### Run status counts
- failed: 30
- success: 12
- running: 1

### Row quality
- valid run rows: 43
- filtered invalid run rows: 65

### Run-level error signal
- runs with non-zero `error_count`: 40

### Initial interpretation
- Smart City operational reliability is currently mixed and materially unstable.
- Failed runs substantially outnumber successful runs in the currently valid run snapshot.
- A high share of valid runs carries non-zero `error_count`.
- Invalid or malformed run rows remain present and should be treated as an evidence-normalization concern, not ignored.

---

## 2. Error distribution

### Errors by step_name
- `build_silver_table`: 5
- `build_telemetry_metrics`: 3
- `build_gold_hourly_table`: 3

### Errors by error_type
- `AnalysisException`: 6
- `ValueError`: 2
- `NameError`: 2
- `DateTimeException`: 1

### Severity x retryable
- `critical | false`: 11

### Top observed step_name x error_type pairs
- `build_gold_hourly_table | AnalysisException`: 3
- `build_telemetry_metrics | AnalysisException`: 2
- `build_silver_table | ValueError`: 2
- `build_silver_table | NameError`: 2
- `build_telemetry_metrics | DateTimeException`: 1
- `build_silver_table | AnalysisException`: 1

### Error row quality
- valid error rows: 11
- filtered invalid error rows: 66

### Initial interpretation
- The main operational hotspot is `build_silver_table`.
- The telemetry layer itself is not neutral; `build_telemetry_metrics` is also a visible failure cluster.
- `build_gold_hourly_table` failures indicate dependency fragility, especially reliance on Silver output availability.
- All valid error rows in the current cleaned snapshot are `critical` and `non-retryable`.

---

## 3. Freshness summary

### Freshness status counts
- `stale`: 8

### Freshness lag summary
- count: 8
- min freshness lag minutes: 273171.50
- avg freshness lag minutes: 409828.51
- max freshness lag minutes: 638303.30

### Row quality
- valid freshness rows: 8
- filtered invalid freshness rows: 0

### Initial interpretation
- Freshness is currently the clearest red-domain governance signal.
- All valid reviewed freshness rows are stale.
- Lag values are far beyond normal operational tolerance and should be treated as a formal timeliness exception.

---

## 4. Quality summary

### Quality status counts
- `pass`: 5834

### Quality metric averages
- avg `pass_rate`: 1.000000
- avg `rejected_rate`: 0.000000
- avg `duplicate_rate`: 0.000000
- avg `flagged_rate`: 0.000000

### Row quality
- valid quality rows: 5834
- filtered invalid quality rows: 0

### Initial interpretation
- The current quality evidence snapshot is very strong.
- Quality outputs appear materially healthier than operational reliability and freshness.
- This positive quality signal should remain visible, but must not mask severe timeliness risk.

---

## 5. Governance interpretation

### Current posture by dimension
- Operational reliability: **Amber**
- Data quality: **Green**
- Freshness / timeliness: **Red**
- Incident / exception posture: **Red-leaning Amber**
- Evidence integrity / normalization: **Amber**

### Main governance conclusions
1. Smart City is governable using real telemetry and curated evidence.
2. Freshness is the strongest active high-severity concern.
3. Silver-stage instability remains the primary operational hotspot.
4. Telemetry production is useful but not fully stable, because telemetry-related failures are also present.
5. Critical non-retryable failures are not isolated noise; they are a real governance signal.
6. Evidence normalization remains necessary because malformed rows still exist in run and error outputs.

---

## 6. Recommended next actions

1. Keep freshness as an open Red exception.
2. Keep Silver-stage instability under active operational exception review.
3. Keep telemetry rollup instability visible as a governance concern, not only an engineering concern.
4. Use this cleaned metrics snapshot to update the Smart City scorecard.
5. Improve evidence normalization before stronger executive or board-level claims are made.