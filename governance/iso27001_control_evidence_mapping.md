# ISO 27001 Control-to-Evidence Mapping

## Purpose

This document maps governance outputs and telemetry-derived evidence in this repository to ISO 27001-aligned control and review expectations.

The goal is not to claim full ISO 27001 certification coverage.  
Instead, the goal is to show how this repository can support **audit-aligned evidence generation**, **control monitoring**, and **management review** for data reliability and observability governance.

This mapping is especially relevant for:

- evidence-based governance review
- control monitoring
- exception tracking
- management review inputs
- corrective-action-oriented governance follow-up

---

## Scope

This mapping currently focuses on the Smart City pilot domain and the governance outputs maintained in this repository.

In scope:

- telemetry-derived observed metrics
- scorecards
- exception rules
- exception registers
- monthly governance review
- failure taxonomy
- evidence normalization and interpretation artifacts

Out of scope:

- formal ISO 27001 certification assertion
- full enterprise ISMS scope definition
- organization-wide Statement of Applicability
- enterprise-wide access control implementation evidence
- enterprise-wide asset inventory

---

## Mapping logic

This repository is most useful for ISO 27001-aligned work in the following areas:

1. **Monitoring and measurement**
2. **Operational control evidence**
3. **Management review support**
4. **Risk and exception tracking**
5. **Nonconformity and corrective-action support**
6. **Evidence retention for governance review**

This repository is less about broad enterprise security architecture and more about:

- control evidence
- operational review
- exception visibility
- governance decision support
- continuous improvement inputs

---

## Primary repository evidence sources

### Governance artifacts
- `scorecards/smart_city_scorecard.yaml`
- `exceptions/smart_city_exception_rules.yaml`
- `exceptions/smart_city_exception_register.md`
- `governance/monthly_review_smart_city.md`
- `reports/smart_city_failure_taxonomy.md`
- `reports/smart_city_reliability_summary.md`
- `reports/smart_city_observed_metrics.md`

### Machine-readable evidence
- `reports/generated/smart_city_observed_metrics.json`

### Domain evidence
- `evidence/smart-city/pipeline_run_log.csv/`
- `evidence/smart-city/pipeline_trace.csv/`
- `evidence/smart-city/pipeline_metrics.csv/`
- `evidence/smart-city/quality_metrics_daily.csv/`
- `evidence/smart-city/freshness_metrics.csv/`
- `evidence/smart-city/error_log.csv/`
- `evidence/smart-city/runtime/`

---

## ISO 27001-aligned mapping

## Clause 6 — Planning

### Relevant governance objective
Identify reliability and governance risks and determine how they are tracked and treated.

### Repository support
- `exceptions/smart_city_exception_register.md`
- `exceptions/smart_city_exception_rules.yaml`
- `reports/smart_city_failure_taxonomy.md`

### Evidence value
These artifacts support structured identification of:
- timeliness risk
- dependency-chain risk
- telemetry correctness risk
- implementation defect risk
- evidence integrity risk

### Governance interpretation
This repository helps translate operational telemetry into reviewable risk categories and treatment candidates.

---

## Clause 7 — Support

### Relevant governance objective
Ensure evidence, governance artifacts, and review inputs are documented and usable.

### Repository support
- `guides/`
- `contracts/`
- `domains/`
- `upstream-docs/`
- `reports/generated/smart_city_observed_metrics.json`

### Evidence value
These artifacts support:
- documentation structure
- reusable governance templates
- evidence reproducibility
- traceable review inputs

### Governance interpretation
This repository acts as a structured evidence workspace that supports repeatable review and interpretation.

---

## Clause 8 — Operation

### Relevant governance objective
Show that governance review is grounded in operational evidence and that control-relevant events are visible.

### Repository support
- `evidence/smart-city/runtime/`
- `evidence/smart-city/pipeline_run_log.csv/`
- `evidence/smart-city/pipeline_trace.csv/`
- `evidence/smart-city/error_log.csv/`
- `scripts/analyze_smart_city_telemetry.py`

### Evidence value
These artifacts show:
- operational runs
- failures
- telemetry rollup events
- step-level instability
- critical error conditions
- freshness and quality outcomes

### Governance interpretation
This repository provides reviewable operational control evidence rather than only policy statements.

---

## Clause 9 — Performance Evaluation

### Relevant governance objective
Monitor, measure, analyze, and evaluate governance-relevant evidence.

### Repository support
- `reports/smart_city_observed_metrics.md`
- `reports/generated/smart_city_observed_metrics.json`
- `scorecards/smart_city_scorecard.yaml`
- `governance/monthly_review_smart_city.md`

### Evidence value
These artifacts support:
- observed metric aggregation
- trend review inputs
- domain-level status assessment
- repeatable review cadence

### Governance interpretation
This is one of the strongest ISO-aligned uses of the repository.  
The repository already demonstrates monitoring, measurement, and review logic.

---

## Clause 10 — Improvement

### Relevant governance objective
Track issues, define follow-up actions, and support corrective review.

### Repository support
- `exceptions/smart_city_exception_register.md`
- `governance/monthly_review_smart_city.md`
- `scorecards/smart_city_scorecard.yaml`

### Evidence value
These artifacts support:
- identification of open exceptions
- review of recurring issues
- prioritization of follow-up
- action-oriented governance review

### Governance interpretation
The repository does not yet implement a full corrective action log, but it already provides a strong base for nonconformity and improvement tracking.

---

## Annex A-aligned control themes

This mapping is intentionally thematic rather than claiming exact one-to-one Annex A implementation coverage.

## A.5 / organizational controls — governance, responsibilities, review

### Repository support
- `governance/`
- `domains/`
- `contracts/`
- `exceptions/`
- `scorecards/`

### Relevance
Supports governance structure, review logic, and control interpretation responsibilities.

---

## A.8 / technological and operational evidence themes — monitoring, logging, traceability

### Repository support
- `evidence/smart-city/runtime/`
- `evidence/smart-city/pipeline_trace.csv/`
- `evidence/smart-city/pipeline_metrics.csv/`
- `scripts/analyze_smart_city_telemetry.py`

### Relevance
Supports event visibility, runtime evidence review, telemetry analysis, and trace-oriented governance interpretation.

---

## Logging and monitoring evidence alignment

This repository is especially useful for ISO-aligned review where evidence needs to show that:

- events are captured
- failures are visible
- repeated issues can be classified
- timeliness and quality can be reviewed
- operational evidence is preserved for later governance interpretation

Relevant artifacts:
- runtime event logs
- curated error evidence
- pipeline trace evidence
- observed metrics JSON
- monthly governance review

---

## Management review support

The following artifacts can serve as management review inputs:

- `governance/monthly_review_smart_city.md`
- `scorecards/smart_city_scorecard.yaml`
- `exceptions/smart_city_exception_register.md`
- `reports/smart_city_observed_metrics.md`

These can support management-review-like questions such as:

- What is the current status of the governed domain?
- What are the most important open exceptions?
- Is timeliness acceptable?
- Are failures recurring in specific transformation stages?
- Is telemetry evidence stable enough for executive reporting?

---

## Corrective action support

This repository does not yet maintain a formal corrective action register, but the following artifacts already form a strong base:

- exception register
- monthly review actions
- scorecard status changes
- observed metrics deltas across review cycles

Recommended next extension:
- add a dedicated corrective action log
- connect exception items to action owners and closure evidence
- define closure criteria for recurring exceptions

---

## Evidence retention and audit-readiness value

The repository improves audit-readiness by preserving:

- operational evidence snapshots
- machine-readable observed metrics
- classification logic
- review outputs
- exception decisions
- governance rationale

This is valuable because it moves governance review from informal interpretation into retained, inspectable evidence.

---

## Current strongest ISO-aligned use cases

At the current stage of maturity, the strongest ISO 27001-aligned use cases for this repository are:

1. **Monitoring and measurement evidence**
2. **Management review input preparation**
3. **Exception and nonconformity visibility**
4. **Operational evidence retention**
5. **Control effectiveness discussion support**

---

## Current limitations

This repository should not currently be described as a full ISO 27001 implementation system.

Current limitations include:

- no formal organization-wide ISMS scope control set
- no complete corrective action register yet
- no enterprise-wide control ownership model
- no formal Statement of Applicability
- no enterprise-wide asset and access evidence model

This repository is best described as:

**an ISO 27001-aligned governance evidence and review layer for telemetry-driven data reliability oversight**

---

## Recommended next steps

1. Add a corrective action log linked to exception items.
2. Add owner and due-date fields consistently across exception tracking.
3. Add a management review input/output template aligned to monthly review.
4. Add a control-to-evidence index for each governed domain.
5. Continue using Smart City as the first audit-aligned pilot domain.

---

## Conclusion

This repository already demonstrates a meaningful subset of ISO 27001-aligned governance behavior:

- evidence is collected
- evidence is analyzed
- exceptions are classified
- review outputs are produced
- governance decisions can be supported by retained artifacts

That makes this repository a strong base for extending data reliability governance into audit-aligned control evidence and management review support.