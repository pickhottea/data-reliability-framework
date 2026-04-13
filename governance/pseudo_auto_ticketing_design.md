# Pseudo Auto-Ticketing Design

## Purpose

This document defines a lightweight governance-level pseudo auto-ticketing model for this repository.

The goal is **not** to implement a full enterprise ticketing platform yet.  
The goal is to define how governance evidence can automatically produce:

- ticket candidates
- incident candidates
- escalation candidates
- action-needed records

This design is intended to sit between:

- telemetry-derived evidence
- scorecard interpretation
- exception tracking
- management review
- future corrective action workflows

---

## Why pseudo auto-ticketing exists in this repository

This repository is a governance and evidence-consumption layer.

It already produces:

- observed metrics
- scorecards
- exception rules
- exception register entries
- monthly governance review outputs
- management-review-style outputs

The next natural step is to define when evidence should automatically trigger a governance action candidate.

This is why pseudo auto-ticketing belongs here.

It is not primarily an operational incident-response system.  
It is a **governance action trigger model**.

---

## Scope

In scope:

- rule-based governance ticket candidate generation
- exception-linked action generation
- management-review follow-up candidate generation
- machine-readable candidate output
- future runbook-link support

Out of scope:

- full Jira / Linear / GitHub Issues integration
- enterprise workflow approval logic
- SLA-enforced ticket routing
- full operational paging / on-call response
- enterprise incident management system replacement

---

## Core concept

Pseudo auto-ticketing means:

> When governance evidence crosses defined review thresholds, the repository can automatically generate a structured action candidate.

These outputs are not yet authoritative production tickets.  
They are governance artifacts that make follow-up explicit and repeatable.

Examples:
- a repeated Red freshness condition creates a **timeliness action candidate**
- recurring critical non-retryable failures create an **incident candidate**
- repeated telemetry rollup failures create an **observability corrective-action candidate**
- evidence normalization issues create an **evidence integrity improvement candidate**

---

## Design principles

### 1. Governance-first, not tool-first
Ticket generation starts from governance logic, not from vendor integration.

### 2. Evidence-backed triggers only
No candidate should be generated without evidence references.

### 3. Exception-linked when possible
Ticket candidates should connect to:
- scorecard status
- exception IDs
- review outputs

### 4. Machine-readable output
Candidates should be emitted in a structured format that can later support real integration.

### 5. Lightweight before enterprise
The first version should be simple enough to work entirely inside this repository.

---

## Inputs

Pseudo auto-ticketing should consume the following inputs:

### Primary machine-readable inputs
- `reports/generated/smart_city_observed_metrics.json`
- future generated scorecard extracts
- future generated exception summaries

### Governance inputs
- `scorecards/smart_city_scorecard.yaml`
- `exceptions/smart_city_exception_rules.yaml`
- `exceptions/smart_city_exception_register.md`
- `governance/monthly_review_smart_city.md`

### Domain evidence
- `evidence/smart-city/pipeline_run_log.csv/`
- `evidence/smart-city/error_log.csv/`
- `evidence/smart-city/freshness_metrics.csv/`
- `evidence/smart-city/runtime/`

---

## Candidate output types

## 1. Governance ticket candidate
Used for follow-up actions that require ownership and due date but are not yet incident-level.

Examples:
- repeated Silver-stage instability
- evidence normalization work
- recurring telemetry rollup correctness review

---

## 2. Incident candidate
Used when evidence suggests an issue may require escalation due to severity or recurrence.

Examples:
- repeated critical non-retryable failures
- severe recurring dependency-chain failure
- systemic telemetry correctness breakdown

---

## 3. Timeliness corrective-action candidate
Used when stale conditions materially weaken downstream trust.

Examples:
- all reviewed freshness rows remain stale
- lag stays above defined tolerance across review cycles

---

## 4. Evidence-integrity improvement candidate
Used when governance interpretation itself is weakened by malformed or inconsistent evidence.

Examples:
- high invalid-row counts
- repeated normalization caveats
- contradictory run-history evidence

---

## Trigger model

The first version should use explicit threshold-based trigger rules.

### Trigger family A — scorecard-driven triggers
A candidate is generated when:
- a scorecard dimension is `red`
- or a dimension remains `amber` across repeated review cycles
- or a dimension deteriorates between review periods

Examples:
- `freshness = red`
- `incident_and_exception_management = amber_red`
- `evidence_integrity = amber`

---

### Trigger family B — exception-driven triggers
A candidate is generated when:
- an exception remains `open`
- severity is `red`
- ownership is missing
- due date is missing
- recurrence is visible in evidence

Examples:
- open Red freshness exception with no owner
- repeated Silver-stage exception still open after next review cycle

---

### Trigger family C — metrics-driven triggers
A candidate is generated when observed metrics exceed defined thresholds.

Examples:
- critical non-retryable errors >= threshold
- failed runs >= threshold
- stale rows >= threshold
- invalid evidence rows >= threshold

---

### Trigger family D — management review triggers
A candidate is generated when management review produces:
- a required action
- an escalation condition
- a control effectiveness gap
- a corrective-action recommendation

---

## Initial trigger candidates for Smart City

The first pilot domain should use these trigger candidates.

## TC-001 — Freshness red condition
### Trigger
- `freshness.status = red`
- or all valid freshness rows are `stale`

### Candidate type
- timeliness corrective-action candidate

### Why it matters
Timeliness is currently the strongest governance risk in Smart City.

### Suggested output
- require owner assignment
- require due date
- require downstream trust-position review

---

## TC-002 — Critical non-retryable error recurrence
### Trigger
- `critical_false >= threshold`

### Candidate type
- incident candidate

### Why it matters
Critical non-retryable failures are direct escalation signals.

### Suggested output
- mark as incident candidate
- link to exception register
- require recurrence review by step and error type

---

## TC-003 — Silver-stage instability recurrence
### Trigger
- repeated `build_silver_table` errors
- or Silver remains the dominant hotspot across review cycles

### Candidate type
- governance ticket candidate

### Why it matters
Silver instability affects downstream Gold and governance trust.

### Suggested output
- require remediation owner
- require root-cause category split
- require next review checkpoint

---

## TC-004 — Telemetry rollup instability
### Trigger
- repeated `build_telemetry_metrics` failures
- or telemetry remains governance-visible weakness across review cycles

### Candidate type
- governance ticket candidate

### Why it matters
The measurement system itself becomes a governance concern.

### Suggested output
- require telemetry validation improvement
- require evidence quality review
- link to observability-control weakness category

---

## TC-005 — Evidence integrity concern
### Trigger
- filtered invalid rows exceed threshold
- or management review flags evidence-normalization weakness

### Candidate type
- evidence-integrity improvement candidate

### Why it matters
Governance cannot rely on evidence that is not consistently interpretable.

### Suggested output
- require normalization rule update
- require evidence handling review
- require next-cycle validation

---

## Proposed candidate schema

The first machine-readable candidate format should look like this:

```json
{
  "candidate_id": "GT-2026-001",
  "domain_id": "smart_city",
  "candidate_type": "governance_ticket",
  "title": "Repeated Silver-stage instability requires remediation owner",
  "trigger_source": "observed_metrics_json",
  "trigger_reason": "build_silver_table remains the dominant cleaned failure hotspot",
  "severity": "amber",
  "linked_exception_ids": ["SC-EX-002"],
  "linked_scorecard_dimensions": ["operational_reliability"],
  "evidence_refs": [
    "reports/generated/smart_city_observed_metrics.json",
    "scorecards/smart_city_scorecard.yaml",
    "exceptions/smart_city_exception_register.md"
  ],
  "suggested_owner": "TBD",
  "suggested_due_date": "TBD",
  "suggested_action": "Review recurring Silver-stage failures by error category and assign remediation owner",
  "runbook_link": null,
  "status": "candidate_open"
}

```

## Recommended output location

Generated candidate outputs should be written to:

```
reports/generated/ticket_candidates.json
```

Optional future human-readable summary:

```
reports/ticket_candidates_summary.md
```

---

## Relationship to exception register

Pseudo auto-ticketing does not replace the exception register.

### Exception register answers:

- what is open
- why it matters
- what governance interpretation exists

### Pseudo auto-ticketing answers:

- what action should now be created
- why now
- which evidence triggered it
- who should own it next

So the relationship should be:

- exception register = governance risk tracking
- pseudo ticket candidate = governance action trigger

---

## Relationship to management review

Pseudo auto-ticketing should also support management review outputs.

Examples:

- management review says owner missing → create candidate
- management review says escalate freshness issue → create candidate
- management review says corrective action required → create candidate

This means pseudo auto-ticketing is not only metrics-triggered.

It can also be review-triggered.

---

## Relationship to implementation repositories

This repository should own **governance-level pseudo auto-ticketing**.

Implementation repositories, such as Smart City, may later own:

- operational alert rules
- runbook links
- operational incident triggers
- true alert-to-ticket experiments

Recommended split:

### `data-reliability-framework`

- governance ticket candidates
- incident candidates
- corrective-action candidates
- review-linked action triggers

### Smart City / implementation repo

- alert condition generation
- operational runbook linkage
- alert-to-ticket experiment
- incident workflow proof of concept

---

## Initial implementation plan

## Phase 1 — Design

Create and approve this design artifact.

## Phase 2 — Rule definition

Add a machine-readable rule file, for example:

```
governance/pseudo_auto_ticketing_rules.yaml
```

This file should define:

- trigger IDs
- thresholds
- candidate types
- evidence sources
- linked scorecard dimensions
- linked exception IDs where applicable

## Phase 3 — Candidate generation script

Add:

```
scripts/generate_ticket_candidates.py
```

This script should:

- read observed metrics JSON
- read scorecard YAML
- optionally read exception metadata
- generate candidate JSON

## Phase 4 — Generated output

Write:

```
reports/generated/ticket_candidates.json
```

## Phase 5 — Review integration

Reference ticket candidates in:

- monthly governance review
- management review
- future corrective action log

---

## Initial Smart City thresholds (draft)

These are draft examples only.

### Draft threshold examples

- freshness red → generate candidate immediately
- `critical_false >= 5` → generate incident candidate
- dominant hotspot repeats across 2 review cycles → generate governance ticket
- invalid evidence rows remain material across 2 review cycles → generate evidence-integrity candidate

These thresholds should later be moved to a rules file.

---

## Benefits

A pseudo auto-ticketing model would help this repository:

- move from passive review to action-oriented governance
- make follow-up explicit
- support ISO-aligned corrective-action thinking
- prepare future integration with real ticketing systems
- keep action logic reproducible and evidence-based

---

## Limitations

This design does not yet provide:

- real ticket creation
- workflow approval
- real routing logic
- escalation chains
- enterprise notification integration

This is intentional.

The purpose is to establish **governance action generation logic first**.

---

## Recommended next artifacts

After this design, the next recommended artifacts are:

- `governance/pseudo_auto_ticketing_rules.yaml`
- `scripts/generate_ticket_candidates.py`
- `reports/generated/ticket_candidates.json`

Optional later artifact:

- `reports/ticket_candidates_summary.md`

---

## Conclusion

Pseudo auto-ticketing is the next logical extension for this repository.

The repository already knows how to:

- collect evidence
- classify issues
- generate scorecards
- track exceptions
- support management review

The next step is to let governance logic generate **structured action candidates** automatically.

That is the role of pseudo auto-ticketing in this repository.