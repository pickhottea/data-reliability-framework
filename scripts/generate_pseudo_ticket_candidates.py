#!/usr/bin/env python3

from __future__ import annotations

import json
from datetime import date
from pathlib import Path
from typing import Any


REPO_ROOT = Path(__file__).resolve().parents[1]
RULES_PATH = REPO_ROOT / "governance" / "pseudo_auto_ticketing_rules.yaml"
OBSERVED_METRICS_PATH = REPO_ROOT / "reports" / "generated" / "smart_city_observed_metrics.json"
OUTPUT_PATH = REPO_ROOT / "reports" / "generated" / "ticket_candidates.json"


def read_json(path: Path) -> dict[str, Any]:
    with path.open("r", encoding="utf-8") as f:
        return json.load(f)


def read_yaml_like_json(path: Path) -> dict[str, Any]:
    """
    This project stores rules in YAML, but to avoid adding third-party dependencies,
    this script expects PyYAML to be available. If unavailable, it raises a clear error.
    """
    try:
        import yaml  # type: ignore
    except ImportError as exc:
        raise RuntimeError(
            "PyYAML is required to read governance/pseudo_auto_ticketing_rules.yaml. "
            "Install it with: pip install pyyaml"
        ) from exc

    with path.open("r", encoding="utf-8") as f:
        data = yaml.safe_load(f)

    if not isinstance(data, dict):
        raise ValueError(f"Rules file did not parse to a dictionary: {path}")

    return data


def get_nested(data: dict[str, Any], path: str) -> Any:
    current: Any = data
    for part in path.split("."):
        if not isinstance(current, dict):
            return None
        current = current.get(part)
    return current


def compare(operator: str, actual: Any, expected: Any) -> bool:
    if operator == "equals":
        return actual == expected

    if operator == "greater_than_or_equal":
        try:
            return float(actual) >= float(expected)
        except (TypeError, ValueError):
            return False

    raise ValueError(f"Unsupported operator: {operator}")


def evaluate_condition(condition: dict[str, Any], observed_metrics: dict[str, Any]) -> bool:
    source = condition.get("source")
    path = condition.get("path")
    operator = condition.get("operator")
    value = condition.get("value")

    if source == "observed_metrics_json":
        actual = get_nested(observed_metrics, path)
        return compare(operator, actual, value)

    # For v1, these sources are placeholders unless explicitly handled.
    # They are kept for future extensions.
    if source in {"scorecard", "exception_register", "management_review"}:
        return False

    raise ValueError(f"Unsupported condition source: {source}")


def evaluate_rule(rule: dict[str, Any], observed_metrics: dict[str, Any]) -> bool:
    conditions = rule.get("conditions", {})

    if "all_of" in conditions:
        return all(evaluate_condition(cond, observed_metrics) for cond in conditions["all_of"])

    if "any_of" in conditions:
        return any(evaluate_condition(cond, observed_metrics) for cond in conditions["any_of"])

    return False


def build_trigger_reason(rule: dict[str, Any], observed_metrics: dict[str, Any]) -> str:
    rule_id = rule.get("rule_id", "UNKNOWN")
    title = rule.get("title", "Untitled rule")

    if rule_id == "TC-001":
        stale_count = get_nested(observed_metrics, "freshness.freshness_status_counts.stale")
        freshness_status = get_nested(observed_metrics, "scorecard.dimensions.freshness.status")
        return f"{title}: stale_count={stale_count}, freshness_status={freshness_status}"

    if rule_id == "TC-002":
        critical_false = get_nested(observed_metrics, "error_log.severity_retryable.critical|false")
        return f"{title}: critical_non_retryable={critical_false}"

    if rule_id == "TC-003":
        silver_failures = get_nested(observed_metrics, "error_log.by_step_name.build_silver_table")
        return f"{title}: build_silver_table_failures={silver_failures}"

    if rule_id == "TC-004":
        telemetry_failures = get_nested(observed_metrics, "error_log.by_step_name.build_telemetry_metrics")
        return f"{title}: build_telemetry_metrics_failures={telemetry_failures}"

    if rule_id == "TC-005":
        invalid_run_rows = get_nested(observed_metrics, "run_status.filtered_invalid_rows")
        invalid_error_rows = get_nested(observed_metrics, "error_log.filtered_invalid_rows")
        return (
            f"{title}: filtered_invalid_run_rows={invalid_run_rows}, "
            f"filtered_invalid_error_rows={invalid_error_rows}"
        )

    if rule_id == "TC-006":
        gold_failures = get_nested(observed_metrics, "error_log.by_step_name.build_gold_hourly_table")
        return f"{title}: build_gold_hourly_table_failures={gold_failures}"

    return f"{title}: triggered by configured rule logic"


def build_candidate(
    rule: dict[str, Any],
    observed_metrics: dict[str, Any],
    sequence: int,
    defaults: dict[str, Any],
) -> dict[str, Any]:
    today = date.today()
    candidate_id = f"GT-{today.year}-{sequence:03d}"

    return {
        "candidate_id": candidate_id,
        "domain_id": rule.get("domain_id", "unknown"),
        "candidate_type": rule.get("candidate_type"),
        "title": rule.get("suggested_title"),
        "trigger_source": rule.get("trigger_source"),
        "trigger_reason": build_trigger_reason(rule, observed_metrics),
        "severity": rule.get("severity"),
        "linked_exception_ids": rule.get("linked_exception_ids", []),
        "linked_scorecard_dimensions": rule.get("linked_scorecard_dimensions", []),
        "evidence_refs": rule.get("evidence_refs", []),
        "suggested_owner": defaults.get("suggested_owner", "TBD"),
        "suggested_due_date": defaults.get("suggested_due_date", "TBD"),
        "suggested_action": rule.get("suggested_action"),
        "runbook_link": defaults.get("runbook_link"),
        "status": defaults.get("candidate_status", "candidate_open"),
    }


def deduplicate_candidates(candidates: list[dict[str, Any]]) -> list[dict[str, Any]]:
    seen: set[tuple[Any, ...]] = set()
    deduped: list[dict[str, Any]] = []

    for candidate in candidates:
        key = (
            candidate.get("domain_id"),
            candidate.get("candidate_type"),
            candidate.get("title"),
            candidate.get("trigger_reason"),
        )
        if key in seen:
            continue
        seen.add(key)
        deduped.append(candidate)

    return deduped


def main() -> None:
    print("Generating governance ticket candidates")
    print(f"Repo root: {REPO_ROOT}")
    print(f"Rules file: {RULES_PATH}")
    print(f"Observed metrics: {OBSERVED_METRICS_PATH}")
    print(f"Output path: {OUTPUT_PATH}")

    rules_data = read_yaml_like_json(RULES_PATH)
    observed_metrics = read_json(OBSERVED_METRICS_PATH)

    defaults = rules_data.get("defaults", {})
    rules = rules_data.get("rules", [])

    if not isinstance(rules, list):
        raise ValueError("Expected 'rules' to be a list in pseudo_auto_ticketing_rules.yaml")

    candidates: list[dict[str, Any]] = []
    sequence = 1

    for rule in rules:
        if not rule.get("enabled", False):
            continue

        try:
            matched = evaluate_rule(rule, observed_metrics)
        except Exception as exc:
            print(f"[WARN] Rule {rule.get('rule_id')} evaluation failed: {exc}")
            continue

        if not matched:
            continue

        candidate = build_candidate(
            rule=rule,
            observed_metrics=observed_metrics,
            sequence=sequence,
            defaults=defaults,
        )
        candidates.append(candidate)
        sequence += 1

    candidates = deduplicate_candidates(candidates)

    output = {
        "generated_at": str(date.today()),
        "repository": "data-reliability-framework",
        "domain_id": "smart_city",
        "source_rules": str(RULES_PATH.relative_to(REPO_ROOT)),
        "source_observed_metrics": str(OBSERVED_METRICS_PATH.relative_to(REPO_ROOT)),
        "candidate_count": len(candidates),
        "candidates": candidates,
    }

    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    with OUTPUT_PATH.open("w", encoding="utf-8") as f:
        json.dump(output, f, ensure_ascii=False, indent=2)

    print(f"Generated {len(candidates)} ticket candidate(s)")
    print(f"Wrote: {OUTPUT_PATH}")


if __name__ == "__main__":
    main()