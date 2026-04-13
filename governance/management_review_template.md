# Management Review Template

## Purpose

This template supports management-review-style governance for telemetry-driven data reliability oversight.

It is intended to translate governance evidence into a structured review format that can support:

- monthly governance review
- management-facing status interpretation
- control effectiveness discussion
- exception and corrective-action follow-up
- ISO 27001-aligned review preparation

This template does not assume full enterprise ISMS scope.  
It is designed for governed domains reviewed through evidence, scorecards, and exception tracking.

---

## Review metadata

- **Review period:**  
- **Review date:**  
- **Prepared by:**  
- **Reviewed domain:**  
- **Review type:** Monthly / Ad hoc / Escalation / Quarterly  
- **Version:**  

---

## 1. Review objective

Describe the purpose of this review.

Example:
- assess current domain reliability posture
- review major exceptions
- confirm whether current evidence supports downstream trust
- identify corrective-action priorities
- evaluate whether governance controls remain effective

---

## 2. Inputs reviewed

List the governance and evidence inputs used in this review.

### Governance artifacts
- scorecard:
- exception register:
- monthly review:
- failure taxonomy:
- observed metrics summary:
- ISO-aligned control/evidence mapping:

### Machine-readable evidence
- JSON metrics artifact:
- generated analysis outputs:

### Domain evidence
- pipeline run log:
- pipeline trace:
- pipeline metrics:
- quality metrics:
- freshness metrics:
- error log:
- runtime event evidence:

---

## 3. Domain status summary

### Overall status
- Current overall status:
- Previous status:
- Status trend: Improving / Stable / Deteriorating / Mixed

### Dimension-level status
- Operational reliability:
- Data quality:
- Freshness / timeliness:
- Incident / exception posture:
- Evidence integrity:
- Other domain-specific dimension:

### Management interpretation
Provide a plain-language interpretation of the current domain posture.

Example:
- operational reliability remains mixed
- timeliness remains the most serious concern
- quality signals remain strong
- evidence is usable but still requires normalization caution

---

## 4. Key observations

Summarize the most important observations from the review period.

### Observation 1
- Description:
- Evidence:
- Governance relevance:

### Observation 2
- Description:
- Evidence:
- Governance relevance:

### Observation 3
- Description:
- Evidence:
- Governance relevance:

---

## 5. Exceptions reviewed

List reviewed exceptions and management-level interpretation.

| Exception ID | Title | Status | Severity | Management interpretation | Action needed |
|---|---|---|---|---|---|
|  |  |  |  |  |  |

### Notes
Document whether any exception should be:
- retained
- downgraded
- escalated
- closed
- converted into corrective action

---

## 6. Control effectiveness discussion

Describe whether current controls appear effective based on reviewed evidence.

### Control area: Monitoring and measurement
- Effective? Yes / Partially / No
- Evidence:
- Notes:

### Control area: Exception visibility
- Effective? Yes / Partially / No
- Evidence:
- Notes:

### Control area: Timeliness review
- Effective? Yes / Partially / No
- Evidence:
- Notes:

### Control area: Evidence integrity
- Effective? Yes / Partially / No
- Evidence:
- Notes:

### Control area: Corrective follow-up
- Effective? Yes / Partially / No
- Evidence:
- Notes:

---

## 7. Risks and concerns

List the most important current governance risks.

### Risk 1
- Risk description:
- Evidence source:
- Severity posture:
- Likely impact:
- Proposed next step:

### Risk 2
- Risk description:
- Evidence source:
- Severity posture:
- Likely impact:
- Proposed next step:

### Risk 3
- Risk description:
- Evidence source:
- Severity posture:
- Likely impact:
- Proposed next step:

---

## 8. Decisions

This section is the core management review output.

### Decision 1
- Decision:
- Rationale:
- Owner:
- Due date:

### Decision 2
- Decision:
- Rationale:
- Owner:
- Due date:

### Decision 3
- Decision:
- Rationale:
- Owner:
- Due date:

Typical decision examples:
- retain freshness as Red exception
- require owner assignment for recurring Silver-stage failures
- block stronger downstream trust claims until timeliness improves
- require telemetry evidence normalization before executive reporting

---

## 9. Corrective and follow-up actions

Document actions that should result from the review.

| Action ID | Action | Owner | Due date | Linked exception | Status |
|---|---|---|---|---|---|
|  |  |  |  |  |  |

### Notes
This section can later be split into a dedicated corrective action log if recurring governance operations become more formal.

---

## 10. Escalations

Document whether any issue needs to be escalated.

### Escalation required?
- Yes / No

### If yes
- What is being escalated:
- Why:
- To whom:
- By when:
- Supporting evidence:

---

## 11. Review of previous actions

Assess whether prior review actions were completed and effective.

| Previous action | Status | Evidence of completion | Effectiveness assessment | Further action needed |
|---|---|---|---|---|
|  |  |  |  |  |

---

## 12. Suitability, adequacy, and effectiveness conclusion

This section aligns most directly with management-review logic.

### Suitability
Does the current governance model still fit the domain and its evidence?

### Adequacy
Are the current artifacts, controls, and review outputs sufficient?

### Effectiveness
Are current controls and review mechanisms actually working?

### Conclusion
Example structure:
- suitable: yes / partially / no
- adequate: yes / partially / no
- effective: yes / partially / no

Narrative conclusion:
[Write a short concluding management interpretation.]

---

## 13. Output summary

Summarize what changes or follow-up outputs should be produced after this review.

Examples:
- refresh scorecard
- update exception register
- open corrective action
- assign owner
- revise threshold
- improve telemetry parsing
- prepare escalation note

---

## 14. Next review checkpoint

- **Next review date:**  
- **Next review focus:**  
- **Required inputs for next review:**  

---

## Example use in this repository

This template can be used for:
- Smart City monthly governance review
- future governed domains
- ISO 27001-aligned management review preparation
- exception and corrective follow-up discussion

It should be read together with:
- `scorecards/`
- `exceptions/`
- `reports/`
- `governance/iso27001_control_evidence_mapping.md`