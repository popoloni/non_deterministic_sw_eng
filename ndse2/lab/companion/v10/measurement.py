"""Accounting rehearsal, not reconstructed participant or task telemetry."""

from decimal import Decimal
from pathlib import Path
import json

WORK_CATEGORIES = {"development", "review", "rework", "verification"}


def aggregate(events: list[dict]) -> dict:
    ids: set[str] = set()
    totals: dict[str, dict] = {}
    for event in events:
        if event["event_id"] in ids:
            raise ValueError("duplicate event_id")
        ids.add(event["event_id"])
        category = event["category"]
        value = Decimal(str(event["value"]))
        if not value.is_finite() or value < 0:
            raise ValueError("non-finite or negative value")
        expected_unit = "person-minutes" if category in WORK_CATEGORIES else "count"
        if event["unit"] != expected_unit:
            raise ValueError("inconsistent unit")
        arm = totals.setdefault(event["arm"], {})
        arm[category] = arm.get(category, Decimal(0)) + value
    for arm in totals.values():
        if arm["accepted"] > arm["attempts"]:
            raise ValueError("accepted exceeds attempts")
        arm["person_minutes"] = sum((arm[x] for x in WORK_CATEGORIES), Decimal(0))
        arm["minutes_per_accepted"] = (
            arm["person_minutes"] / arm["accepted"] if arm["accepted"] else None
        )
        arm["acceptance_fraction"] = (
            arm["accepted"] / arm["attempts"] if arm["attempts"] else None
        )
        arm["expansion"] = (
            "HOLD" if arm["open_high_severity"] else "ELIGIBLE_FOR_REVIEW"
        )
    return totals


def active_effort(intervals: list[dict]) -> tuple[float, float]:
    """Return person-minutes and overall elapsed minutes; reject same-actor overlap."""
    ordered = sorted(intervals, key=lambda e: (e["actor"], e["start"]))
    last: dict[str, float] = {}
    total = 0.0
    for event in ordered:
        start, end = float(event["start"]), float(event["end"])
        if start < 0 or end < start:
            raise ValueError("invalid interval")
        if event["actor"] in last and start < last[event["actor"]]:
            raise ValueError("overlapping work for one actor")
        last[event["actor"]] = end
        total += end - start
    elapsed = max((float(e["end"]) for e in ordered), default=0) - min(
        (float(e["start"]) for e in ordered), default=0
    )
    return total, elapsed


if __name__ == "__main__":
    records = json.loads(
        Path(__file__).with_name("measurement_events.json").read_text()
    )
    print(json.dumps(aggregate(records), default=str, indent=2))
