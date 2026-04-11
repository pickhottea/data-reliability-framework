# RACI Matrix - Smart City Runtime Observability Pilot

This RACI is scoped to the **Urban Air Quality Runtime Observability** domain.

## Roles

- **Domain Owner** - accountable for business fit and governance outcomes
- **Data Steward** - accountable for data definitions, field quality, and review inputs
- **Technical Owner** - accountable for implementation and operational fixes
- **Reliability Reviewer** - accountable for scorecarding, exception review, and threshold interpretation
- **Governance Board Approver** - accountable for approving major control changes and risk acceptance

## Matrix

| Activity | Domain Owner | Data Steward | Technical Owner | Reliability Reviewer | Governance Board Approver |
|---|---|---|---|---|---|
| Define telemetry contract scope | A | C | R | C | I |
| Maintain telemetry helper implementation | I | I | R | C | I |
| Approve KPI / SLO catalog | A | C | C | R | I |
| Review monthly scorecard | A | R | C | C | I |
| Investigate freshness breach | I | C | R | A | I |
| Investigate schema compliance drop | I | A | R | C | I |
| Open incident record | I | C | R | A | I |
| Close corrective action | C | C | R | A | I |
| Approve threshold change | C | C | R | A | I |
| Approve contract-breaking change | C | C | C | R | A |
| Accept temporary exception | A | C | C | R | C |
| Review board pack and decision log | A | R | C | C | I |

## Notes

- **R** = Responsible for execution
- **A** = Accountable for final decision
- **C** = Consulted before decision
- **I** = Informed after decision

This pilot RACI is intentionally compact. Expand role granularity only after additional domains are onboarded.
