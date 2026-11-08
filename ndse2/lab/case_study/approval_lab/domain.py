"""Canonical domain types and strict boundary validation (stdlib only)."""

from dataclasses import dataclass, asdict
import re

TOKEN = re.compile(r"^[A-Za-z0-9][A-Za-z0-9_.-]{0,63}$")


class ValidationError(ValueError):
    pass


class ConflictError(ValueError):
    pass


@dataclass(frozen=True)
class Transaction:
    transaction_id: str
    amount_minor: int
    currency: str
    department: str
    risk: str
    requester: str
    cross_border: bool = False

    def __post_init__(self):
        for name in ("transaction_id", "department", "requester"):
            value = getattr(self, name)
            if not isinstance(value, str) or not TOKEN.fullmatch(value):
                raise ValidationError(
                    f"{name}: expected safe identifier 1–64 characters"
                )
        if type(self.amount_minor) is not int or not 0 < self.amount_minor <= 10**12:
            raise ValidationError("amount_minor must be a positive integer <= 10^12")
        if self.currency != "EUR":
            raise ValidationError("only synthetic EUR policies are supported")
        if self.risk not in {"LOW", "HIGH"}:
            raise ValidationError(
                "risk must be LOW or HIGH; unknown values fail closed"
            )
        if type(self.cross_border) is not bool:
            raise ValidationError("cross_border must be boolean")

    def as_payload(self) -> dict:
        return asdict(self)


@dataclass(frozen=True)
class Decision:
    transaction_id: str
    status: str
    reason_code: str
    policy_version: str
    policy_rule: str
    policy_amount_minor: int | None
    evidence_kind: str = "SYNTHETIC_DETERMINISTIC_RULE"

    def as_payload(self) -> dict:
        return asdict(self)
