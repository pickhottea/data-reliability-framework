#!/usr/bin/env python3

from __future__ import annotations

import csv
import glob
import json
import math
from collections import Counter
from pathlib import Path
from typing import Any


REPO_ROOT = Path(__file__).resolve().parents[1]
EVIDENCE_ROOT = REPO_ROOT / "evidence" / "smart-city"
GENERATED_ROOT = REPO_ROOT / "reports" / "generated"
JSON_OUTPUT = GENERATED_ROOT / "smart_city_observed_metrics.json"


EXPECTED_RUN_STATUS = {"failed", "success", "running", "succeeded"}
EXPECTED_SEVERITY = {"critical", "high", "medium", "low", "warning", "info"}
EXPECTED_RETRYABLE = {"true", "false"}


def find_single_part_csv(directory_name: str) -> Path:
    matches = glob.glob(str(EVIDENCE_ROOT / directory_name / "part-*.csv"))
    if not matches:
        raise FileNotFoundError(
            f"No part-*.csv found under {EVIDENCE_ROOT / directory_name}"
        )
    if len(matches) > 1:
        print(f"[WARN] Multiple part files under {directory_name}; using first: {matches[0]}")
    return Path(matches[0])


def safe_text(value: Any) -> str:
    if value is None:
        return ""
    return str(value).strip()


def safe_float(value: Any) -> float | None:
    text = safe_text(value)
    if not text:
        return None
    try:
        v = float(text)
        if math.isnan(v):
            return None
        return v
    except ValueError:
        return None


def print_counter(title: str, counter: Counter, limit: int | None = None) -> None:
    print(f"\n=== {title} ===")
    items = counter.most_common(limit)
    if not items:
        print("(no rows)")
        return
    for key, count in items:
        print(f"{key}: {count}")


def rows_from_csv(path: Path) -> list[dict[str, str | None]]:
    with path.open("r", encoding="utf-8", newline="") as f:
        return list(csv.DictReader(f))


def is_valid_run_row(row: dict[str, str | None]) -> bool:
    status = safe_text(row.get("status")).lower()
    run_id = safe_text(row.get("run_id"))
    pipeline_name = safe_text(row.get("pipeline_name"))
    started_at = safe_text(row.get("started_at"))

    if status not in EXPECTED_RUN_STATUS:
        return False
    if not run_id or not pipeline_name or not started_at:
        return False
    return True


def is_valid_error_row(row: dict[str, str | None]) -> bool:
    error_ts = safe_text(row.get("error_ts"))
    run_id = safe_text(row.get("run_id"))
    step_name = safe_text(row.get("step_name"))
    error_type = safe_text(row.get("error_type"))
    severity = safe_text(row.get("severity")).lower()
    retryable = safe_text(row.get("retryable")).lower()

    if not error_ts or not run_id or not step_name or not error_type:
        return False
    if severity not in EXPECTED_SEVERITY:
        return False
    if retryable not in EXPECTED_RETRYABLE:
        return False
    return True


def is_valid_freshness_row(row: dict[str, str | None]) -> bool:
    metric_ts = safe_text(row.get("metric_ts"))
    status = safe_text(row.get("freshness_status")).lower()
    lag = safe_float(row.get("freshness_lag_minutes"))
    return bool(metric_ts and status and lag is not None)


def is_valid_quality_row(row: dict[str, str | None]) -> bool:
    metric_date = safe_text(row.get("metric_date"))
    quality_status = safe_text(row.get("quality_status")).lower()
    pass_rate = safe_float(row.get("pass_rate"))
    return bool(metric_date and quality_status and pass_rate is not None)


def analyze_run_status() -> dict[str, Any]:
    path = find_single_part_csv("pipeline_run_log.csv")
    raw_rows = rows_from_csv(path)

    valid_rows = []
    invalid_rows = 0
    status_counter: Counter[str] = Counter()
    error_count_nonzero = 0

    for row in raw_rows:
        if not is_valid_run_row(row):
            invalid_rows += 1
            continue
        valid_rows.append(row)

        status = safe_text(row.get("status")).lower()
        status_counter[status] += 1

        err = safe_float(row.get("error_count"))
        if err and err > 0:
            error_count_nonzero += 1

    print_counter("Run status counts", status_counter)
    print(f"\nValid run rows: {len(valid_rows)}")
    print(f"Filtered invalid run rows: {invalid_rows}")
    print(f"Runs with non-zero error_count: {error_count_nonzero}")
    print(f"Source file: {path}")

    return {
        "source_file": str(path),
        "valid_rows": len(valid_rows),
        "filtered_invalid_rows": invalid_rows,
        "status_counts": dict(status_counter),
        "runs_with_nonzero_error_count": error_count_nonzero,
    }


def analyze_error_log() -> dict[str, Any]:
    path = find_single_part_csv("error_log.csv")
    raw_rows = rows_from_csv(path)

    valid_rows = []
    invalid_rows = 0
    step_counter: Counter[str] = Counter()
    error_type_counter: Counter[str] = Counter()
    severity_retryable_counter: Counter[str] = Counter()
    step_error_counter: Counter[str] = Counter()

    for row in raw_rows:
        if not is_valid_error_row(row):
            invalid_rows += 1
            continue
        valid_rows.append(row)

        step = safe_text(row.get("step_name"))
        error_type = safe_text(row.get("error_type"))
        severity = safe_text(row.get("severity")).lower()
        retryable = safe_text(row.get("retryable")).lower()

        step_counter[step] += 1
        error_type_counter[error_type] += 1
        severity_retryable_counter[f"{severity}|{retryable}"] += 1
        step_error_counter[f"{step}|{error_type}"] += 1

    print_counter("Errors by step_name", step_counter)
    print_counter("Errors by error_type", error_type_counter)
    print_counter("Severity x retryable", severity_retryable_counter)
    print_counter("Top step_name x error_type pairs", step_error_counter, limit=10)
    print(f"\nValid error rows: {len(valid_rows)}")
    print(f"Filtered invalid error rows: {invalid_rows}")
    print(f"Source file: {path}")

    return {
        "source_file": str(path),
        "valid_rows": len(valid_rows),
        "filtered_invalid_rows": invalid_rows,
        "by_step_name": dict(step_counter),
        "by_error_type": dict(error_type_counter),
        "severity_retryable": dict(severity_retryable_counter),
        "top_step_error_pairs": dict(step_error_counter.most_common(10)),
    }


def analyze_freshness() -> dict[str, Any]:
    path = find_single_part_csv("freshness_metrics.csv")
    raw_rows = rows_from_csv(path)

    valid_rows = []
    invalid_rows = 0
    status_counter: Counter[str] = Counter()
    lags: list[float] = []

    for row in raw_rows:
        if not is_valid_freshness_row(row):
            invalid_rows += 1
            continue
        valid_rows.append(row)

        status = safe_text(row.get("freshness_status")).lower()
        lag = safe_float(row.get("freshness_lag_minutes"))

        status_counter[status] += 1
        if lag is not None:
            lags.append(lag)

    print_counter("Freshness status counts", status_counter)

    lag_summary: dict[str, float | int] = {}
    if lags:
        lag_summary = {
            "count": len(lags),
            "min": round(min(lags), 2),
            "avg": round(sum(lags) / len(lags), 2),
            "max": round(max(lags), 2),
        }
        print("\n=== Freshness lag summary (minutes) ===")
        print(f"count: {lag_summary['count']}")
        print(f"min: {lag_summary['min']:.2f}")
        print(f"avg: {lag_summary['avg']:.2f}")
        print(f"max: {lag_summary['max']:.2f}")
    else:
        print("\nNo valid freshness_lag_minutes values found.")

    print(f"\nValid freshness rows: {len(valid_rows)}")
    print(f"Filtered invalid freshness rows: {invalid_rows}")
    print(f"Source file: {path}")

    return {
        "source_file": str(path),
        "valid_rows": len(valid_rows),
        "filtered_invalid_rows": invalid_rows,
        "freshness_status_counts": dict(status_counter),
        "lag_minutes": lag_summary,
    }


def analyze_quality() -> dict[str, Any]:
    path = find_single_part_csv("quality_metrics_daily.csv")
    raw_rows = rows_from_csv(path)

    valid_rows = []
    invalid_rows = 0
    quality_status_counter: Counter[str] = Counter()
    pass_rates: list[float] = []
    rejected_rates: list[float] = []
    duplicate_rates: list[float] = []
    flagged_rates: list[float] = []

    for row in raw_rows:
        if not is_valid_quality_row(row):
            invalid_rows += 1
            continue
        valid_rows.append(row)

        quality_status = safe_text(row.get("quality_status")).lower()
        quality_status_counter[quality_status] += 1

        for field_name, target in [
            ("pass_rate", pass_rates),
            ("rejected_rate", rejected_rates),
            ("duplicate_rate", duplicate_rates),
            ("flagged_rate", flagged_rates),
        ]:
            val = safe_float(row.get(field_name))
            if val is not None:
                target.append(val)

    print_counter("Quality status counts", quality_status_counter)

    averages = {
        "pass_rate": round(sum(pass_rates) / len(pass_rates), 6) if pass_rates else None,
        "rejected_rate": round(sum(rejected_rates) / len(rejected_rates), 6) if rejected_rates else None,
        "duplicate_rate": round(sum(duplicate_rates) / len(duplicate_rates), 6) if duplicate_rates else None,
        "flagged_rate": round(sum(flagged_rates) / len(flagged_rates), 6) if flagged_rates else None,
    }

    print("\n=== Quality metric averages ===")
    for key, value in averages.items():
        if value is not None:
            print(f"avg {key}: {value:.6f}")

    print(f"\nValid quality rows: {len(valid_rows)}")
    print(f"Filtered invalid quality rows: {invalid_rows}")
    print(f"Source file: {path}")

    return {
        "source_file": str(path),
        "valid_rows": len(valid_rows),
        "filtered_invalid_rows": invalid_rows,
        "quality_status_counts": dict(quality_status_counter),
        "averages": averages,
    }


def write_json_report(results: dict[str, Any]) -> None:
    GENERATED_ROOT.mkdir(parents=True, exist_ok=True)
    with JSON_OUTPUT.open("w", encoding="utf-8") as f:
        json.dump(results, f, ensure_ascii=False, indent=2)
    print(f"\nJSON report written to: {JSON_OUTPUT}")


def main() -> None:
    print("Smart City telemetry analysis")
    print(f"Repo root: {REPO_ROOT}")
    print(f"Evidence root: {EVIDENCE_ROOT}")

    results = {
        "status_date": "2026-04-11",
        "repo_root": str(REPO_ROOT),
        "evidence_root": str(EVIDENCE_ROOT),
        "run_status": analyze_run_status(),
        "error_log": analyze_error_log(),
        "freshness": analyze_freshness(),
        "quality": analyze_quality(),
    }

    write_json_report(results)


if __name__ == "__main__":
    main()