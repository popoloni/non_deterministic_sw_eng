"""Scope/source check for ONE synthetic threshold-card schema, not general fact verification."""

from __future__ import annotations
import hashlib, json
from pathlib import Path


def check_threshold_card(
    card: dict, source: Path, active_policy: str, purpose: str
) -> str:
    required = {
        "policy_version",
        "department",
        "ceiling_minor",
        "source_sha256",
        "owner",
        "state",
    }
    if not isinstance(card, dict) or not required.issubset(card) or not card["owner"]:
        return "HOLD_MISSING_PROVENANCE"
    if card["state"] not in {"CURRENT", "SUPERSEDED"}:
        return "HOLD_UNRESOLVED_STATE"
    if purpose not in {"new_decision", "historical_explanation"}:
        return "HOLD_UNKNOWN_PURPOSE"
    try:
        content = source.read_bytes()
        policy = json.loads(content)
        if hashlib.sha256(content).hexdigest() != card["source_sha256"]:
            return "HOLD_SOURCE_CHANGED"
        if policy["policy_version"] != card["policy_version"]:
            return "HOLD_VERSION_MISMATCH"
        if (
            type(card["ceiling_minor"]) is not int
            or policy["departments"].get(card["department"]) != card["ceiling_minor"]
        ):
            return "HOLD_UNSUPPORTED_VALUE"
    except (OSError, ValueError, KeyError, TypeError):
        return "HOLD_UNREADABLE_SOURCE"
    if purpose == "new_decision":
        if card["policy_version"] != active_policy or card["state"] != "CURRENT":
            return "HOLD_STALE_FOR_NEW"
        return "CURRENT_SOURCE_MATCH_NOT_AUTHORIZATION"
    return "HISTORICAL_SOURCE_MATCH_NOT_AUTHORIZATION"
