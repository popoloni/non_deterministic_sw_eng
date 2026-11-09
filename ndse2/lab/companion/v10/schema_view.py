"""Derived policy-view migration; original policies and decision store are untouched."""

from __future__ import annotations
from typing import Any

FIELDS = {"schema", "policy_version", "rules", "cross_border_behavior"}
RULE_FIELDS = {"department", "currency", "limit_minor"}


def decode_view(view: dict[str, Any]) -> dict[str, Any]:
    if (
        not isinstance(view, dict)
        or set(view) != FIELDS
        or view["schema"] != "policy-view-1"
    ):
        raise ValueError("unknown or missing view fields")
    if not isinstance(view["policy_version"], str) or not view["policy_version"]:
        raise ValueError("policy version required")
    if view["cross_border_behavior"] != "REVIEW_REQUIRED":
        raise ValueError("cross-border behavior cannot change in this migration")
    rules = view["rules"]
    if not isinstance(rules, list) or not rules:
        raise ValueError("rules required")
    departments = {}
    for rule in rules:
        if not isinstance(rule, dict) or set(rule) != RULE_FIELDS:
            raise ValueError("invalid rule fields")
        name = rule["department"]
        limit = rule["limit_minor"]
        if not isinstance(name, str) or not name or name in departments:
            raise ValueError("duplicate/invalid department")
        if rule["currency"] != "EUR" or type(limit) is not int or limit < 0:
            raise ValueError("invalid currency/unit")
        departments[name] = limit
    return {
        "policy_version": view["policy_version"],
        "currency": "EUR",
        "departments": departments,
        "cross_border_behavior": "REVIEW_REQUIRED",
    }


def encode_view(policy: dict[str, Any]) -> dict[str, Any]:
    expected = {"policy_version", "currency", "departments", "cross_border_behavior"}
    if (
        not isinstance(policy, dict)
        or set(policy) != expected
        or policy["currency"] != "EUR"
        or not isinstance(policy["departments"], dict)
    ):
        raise ValueError("invalid canonical policy")
    view = {
        "schema": "policy-view-1",
        "policy_version": policy["policy_version"],
        "rules": [
            {"department": k, "currency": "EUR", "limit_minor": v}
            for k, v in policy["departments"].items()
        ],
        "cross_border_behavior": policy["cross_border_behavior"],
    }
    decode_view(view)
    return view
