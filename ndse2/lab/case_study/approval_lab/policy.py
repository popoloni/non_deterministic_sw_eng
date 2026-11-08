"""Versioned policy selection. Unknown fields/units fail closed for safety."""

import json
from pathlib import Path
from .domain import Transaction, Decision, ValidationError


class Policy:
    ALLOWED = {"policy_version", "currency", "departments", "cross_border_behavior"}

    def __init__(
        self,
        policy_version: str,
        currency: str,
        departments: dict,
        cross_border_behavior: str,
    ):
        if not policy_version or not isinstance(policy_version, str):
            raise ValidationError("policy version required")
        if currency != "EUR":
            raise ValidationError("only EUR policy is valid")
        if not isinstance(departments, dict) or not departments:
            raise ValidationError("departments must be nonempty")
        for name, limit in departments.items():
            if not isinstance(name, str) or type(limit) is not int or limit < 0:
                raise ValidationError("invalid policy department or threshold")
        if cross_border_behavior != "REVIEW_REQUIRED":
            raise ValidationError("cross_border must explicitly route to human review")
        self.version = policy_version
        self.currency = currency
        self.departments = dict(departments)
        self.cross_border_behavior = cross_border_behavior

    @classmethod
    def from_file(cls, path: str | Path):
        with open(path, encoding="utf-8") as fh:
            data = json.load(fh)
        if set(data) != cls.ALLOWED:
            raise ValidationError("unexpected/missing policy keys")
        return cls(
            data["policy_version"],
            data["currency"],
            data["departments"],
            data["cross_border_behavior"],
        )

    def evaluate(self, tx: Transaction) -> Decision:
        if tx.currency != self.currency:
            raise ValidationError("unsupported currency")
        max_amount = self.departments.get(tx.department)
        if tx.risk == "HIGH":
            return Decision(
                tx.transaction_id,
                "REVIEW_REQUIRED",
                "HIGH_RISK",
                self.version,
                "risk",
                None,
            )
        if tx.cross_border:
            return Decision(
                tx.transaction_id,
                "REVIEW_REQUIRED",
                "CROSS_BORDER",
                self.version,
                "cross_border",
                None,
            )
        if max_amount is None:
            return Decision(
                tx.transaction_id,
                "REVIEW_REQUIRED",
                "UNRECOGNIZED_DEPARTMENT",
                self.version,
                "department",
                None,
            )
        if tx.amount_minor > max_amount:
            return Decision(
                tx.transaction_id,
                "REVIEW_REQUIRED",
                "THRESHOLD_EXCEEDED",
                self.version,
                tx.department,
                max_amount,
            )
        return Decision(
            tx.transaction_id,
            "AUTO_APPROVAL_ELIGIBLE",
            "WITHIN_THRESHOLD",
            self.version,
            tx.department,
            max_amount,
        )
