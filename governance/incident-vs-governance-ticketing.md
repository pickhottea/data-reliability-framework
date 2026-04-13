# Incident vs Governance Ticketing

## Purpose

This document explains the difference between:

- implementation-side incident candidate generation
- governance-side pseudo ticket candidate generation

Both are valid, but they belong to different repositories and serve different purposes.

---

## Why this distinction matters

As the Smart City implementation and the data reliability governance layer evolved, two different action-generation patterns emerged:

1. **Operational / implementation-side incident candidates**
2. **Governance / review-side pseudo ticket candidates**

These should not be merged into a single script or repository because they answer different questions.

---

## 1. Implementation-side incident candidates

### Repository
`smart-city-air-quality-platform`

### Current script
`spark/jobs/build_incident_candidates.py`

### Primary inputs
- `data/telemetry/curated/pipeline_run_log.csv`
- `data/telemetry/curated/quality_metrics_daily.csv`
- `data/telemetry/curated/error_log.csv`
- `configs/incident_thresholds.yaml`

### Primary output
- `data/telemetry/curated/incident_candidates.csv`

### Purpose
This script generates **operational incident candidates** directly from the latest Smart City telemetry outputs.

It is intended to answer questions such as:

- Did the latest run fail badly enough to require incident review?
- Did quality or rejection metrics exceed operational thresholds?
- Did the latest run produce critical errors that deserve immediate follow-up?

### Nature of this logic
This is:

- pipeline-local
- implementation-side
- threshold-driven
- operationally oriented
- close to the execution context

### What it is good for
- latest-run triage
- operational visibility
- pipeline-level escalation candidates
- lightweight alert/incident prototyping

### Why it belongs in Smart City
It depends directly on:

- local curated telemetry outputs
- Spark processing
- Smart City pipeline semantics
- latest-run execution context

That makes it part of the implementation repository.

---

## 2. Governance-side pseudo ticket candidates

### Repository
`data-reliability-framework`

### Current / planned scripts
- `scripts/generate_pseudo_ticket_candidates.py`

### Primary inputs
- `reports/generated/smart_city_observed_metrics.json`
- `governance/pseudo_auto_ticketing_rules.yaml`
- `scorecards/smart_city_scorecard.yaml`
- `exceptions/smart_city_exception_register.md`
- `governance/monthly_review_smart_city.md`

### Primary output
- `reports/generated/ticket_candidates.json`

### Purpose
This logic generates **governance-level pseudo ticket candidates** from reviewed evidence.

It is intended to answer questions such as:

- Which issues now require formal follow-up?
- Which open governance exceptions should produce an action candidate?
- Which recurring risks should become corrective-action candidates?
- Which review outputs should now become tracked governance work?

### Nature of this logic
This is:

- governance-side
- evidence-consumption oriented
- review-aware
- scorecard-aware
- exception-aware
- management-review-aligned

### What it is good for
- governance follow-up tracking
- corrective-action candidate generation
- exception-linked action creation
- management-review action capture
- ISO-aligned improvement workflow support

### Why it belongs in `data-reliability-framework`
It depends on:

- reviewed evidence snapshots
- normalized observed metrics
- scorecard interpretation
- exception tracking
- governance review outputs

That makes it part of the governance repository rather than the implementation repository.

---

## 3. One sentence summary

### Smart City repo
Generates:
**incident candidates from operational telemetry**

### Data reliability framework repo
Generates:
**pseudo ticket candidates from governance review evidence**

---

## 4. Functional comparison

| Dimension | Smart City incident candidate generation | Governance pseudo ticket candidate generation |
|---|---|---|
| Repository | `smart-city-air-quality-platform` | `data-reliability-framework` |
| Script example | `spark/jobs/build_incident_candidates.py` | `scripts/generate_pseudo_ticket_candidates.py` |
| Main focus | Operational incident triage | Governance follow-up and corrective action |
| Main inputs | Latest curated telemetry | Observed metrics, scorecards, exceptions, review outputs |
| Main output | `incident_candidates.csv` | `ticket_candidates.json` |
| Time horizon | Latest run / immediate execution context | Review cycle / governance context |
| Logic type | Threshold-based operational triggers | Rule-based governance action generation |
| Audience | Pipeline/operator/implementation owner | Governance reviewer / management / control owner |

---

## 5. Why these should not be collapsed into one script

These two mechanisms look similar because both create “candidates,” but they are not the same.

### If merged too early, the risks are:
- operational logic and governance logic get mixed
- repository ownership becomes unclear
- evidence and review semantics become blurred
- incident triage and governance corrective action lose distinction

### Better separation
Keep them separate so that:

- Smart City owns operational escalation logic
- the reliability framework owns governance action logic

This is cleaner, easier to explain, and more scalable for future domains.

---

## 6. Relationship between the two layers

The two layers should be related, but not identical.

### Flow
1. Smart City generates telemetry and curated evidence
2. Smart City may generate operational incident candidates
3. Evidence is copied into `data-reliability-framework`
4. Governance analysis produces observed metrics
5. Scorecards and exception review are updated
6. Governance pseudo tickets are generated

### Interpretation
Operational incidents are closer to:
- what just happened

Governance pseudo tickets are closer to:
- what now requires tracked follow-up

---

## 7. Example distinction

### Example A — latest run failed
In Smart City:
- latest run failed
- error severity is critical
- `build_incident_candidates.py` may generate an incident candidate immediately

In the governance repo:
- repeated failures across review evidence may generate a governance pseudo ticket
- that pseudo ticket may ask for owner assignment, due date, and corrective action tracking

These are related, but they are not the same artifact.

---

### Example B — freshness remains red
In Smart City:
- this might or might not create an operational incident candidate depending on pipeline design

In the governance repo:
- a red freshness condition should produce a timeliness corrective-action candidate
- because this affects downstream trust and management review

This is a clear governance-side action, not just an operational alert.

---

## 8. Current recommended repository ownership

### `smart-city-air-quality-platform`
Owns:
- telemetry production
- curated telemetry outputs
- local threshold logic
- incident candidate generation
- future operational alert/runbook experiments

### `data-reliability-framework`
Owns:
- evidence ingestion
- observed metrics analysis
- scorecards
- exception register
- monthly governance review
- ISO-aligned control/evidence mapping
- pseudo auto-ticketing
- governance action candidate generation

---

## 9. Naming guidance

To keep the distinction visible, naming should remain explicit.

### Recommended names

#### Smart City repo
- `build_incident_candidates.py`

#### Data reliability framework repo
- `generate_pseudo_ticket_candidates.py`

This naming helps avoid confusion between:
- operational incidents
- governance follow-up tickets

---

## 10. Future evolution

Over time, these two layers may become more connected.

### Possible future Smart City evolution
- alert-to-ticket experiments
- runbook links
- stronger operational incident workflows

### Possible future governance evolution
- corrective action log integration
- owner and due-date assignment
- management-review action tracking
- optional integration with real ticketing systems

Even then, the distinction should remain:

- implementation-side action generation
- governance-side action generation

---

## Conclusion

Both incident candidate generation and pseudo ticket candidate generation are useful, but they belong to different layers.

The correct model is:

- **Smart City** generates operational incident candidates from pipeline telemetry
- **Data Reliability Framework** generates governance pseudo ticket candidates from reviewed evidence

This separation keeps repository responsibilities clear and allows both operational and governance workflows to mature without being confused with each other.