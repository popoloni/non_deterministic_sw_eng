"""Transparent scenario arithmetic, never calibrated production estimates."""

from __future__ import annotations
from decimal import Decimal


def nonnegative(value: object, name: str) -> Decimal:
    if isinstance(value, bool):
        raise ValueError(name)
    try:
        d = Decimal(str(value))
    except Exception as exc:
        raise ValueError(name) from exc
    if not d.is_finite() or d < 0:
        raise ValueError(name)
    return d


def break_even_minutes(extra_cost: object, hourly_rate: object) -> Decimal:
    extra = nonnegative(extra_cost, "extra_cost")
    rate = nonnegative(hourly_rate, "hourly_rate")
    if rate == 0:
        raise ValueError("positive hourly rate required")
    return Decimal(60) * extra / rate


def net_optional_cost(
    extra_cost: object, saved_minutes: object, hourly_rate: object
) -> Decimal:
    return nonnegative(extra_cost, "extra_cost") - nonnegative(
        saved_minutes, "saved_minutes"
    ) * nonnegative(hourly_rate, "hourly_rate") / Decimal(60)


def local_period_cost(
    *,
    active_watts: object,
    active_hours: object,
    idle_watts: object,
    idle_hours: object,
    price_per_kwh: object,
    allocated_hardware_cost: object,
    support_cost: object,
    accepted_changes: int,
) -> dict[str, Decimal | None]:
    """All inputs observed or explicitly assumed over ONE common period.
    Hardware/support allocation policy is supplied, not inferred.
    Active/idle hours must be disjoint. Cost per accepted change is undefined at zero.
    """
    if type(accepted_changes) is not int or accepted_changes < 0:
        raise ValueError("accepted_changes")
    energy = (
        nonnegative(active_watts, "active_watts")
        * nonnegative(active_hours, "active_hours")
        + nonnegative(idle_watts, "idle_watts") * nonnegative(idle_hours, "idle_hours")
    ) / Decimal(1000)
    energy_cost = energy * nonnegative(price_per_kwh, "price_per_kwh")
    total = (
        energy_cost
        + nonnegative(allocated_hardware_cost, "allocated_hardware_cost")
        + nonnegative(support_cost, "support_cost")
    )
    return {
        "kwh": energy,
        "energy_cost": energy_cost,
        "total_allocated_cost": total,
        "cost_per_accepted_change": (
            total / Decimal(accepted_changes) if accepted_changes else None
        ),
    }
