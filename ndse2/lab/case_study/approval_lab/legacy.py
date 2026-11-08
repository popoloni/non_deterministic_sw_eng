"""Intentionally defective, isolated teaching baseline. Never use for real decisions."""

from .domain import Transaction


def legacy_route(tx: Transaction) -> str:
    # Historical bug: ignores high risk, department and cross-border status.
    return (
        "AUTO_APPROVAL_ELIGIBLE" if tx.amount_minor <= 1_000_000 else "REVIEW_REQUIRED"
    )
