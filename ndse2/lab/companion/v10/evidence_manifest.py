"""Version/digest consistency of synthetic evidence. Not signatures or proof of execution."""

from __future__ import annotations
import hashlib
from pathlib import Path
from typing import Any

ROLES = {"candidate", "intent", "oracle", "environment"}


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def make_manifest(
    paths: dict[str, Path],
    intent_id: str,
    command: list[str],
    exit_code: int,
    unchecked: list[str],
    created_at: int,
) -> dict[str, Any]:
    if set(paths) != ROLES or not intent_id or not command:
        raise ValueError("all four artifact roles, intent and command required")
    if type(exit_code) is not int or type(created_at) is not int or created_at < 0:
        raise ValueError("invalid execution metadata")
    return {
        "intent_id": intent_id,
        "artifacts": {
            role: {"path": str(p), "sha256": sha(p)} for role, p in paths.items()
        },
        "command": command,
        "exit_code": exit_code,
        "unchecked": unchecked,
        "created_at": created_at,
        "producer": "synthetic trusted harness",
        "producer_authenticated": False,
        "execution_attested": False,
    }


def verify_manifest(
    bundle: dict[str, Any], current: dict[str, Path], intent_id: str
) -> dict[str, str]:
    if set(current) != ROLES:
        return {"status": "HOLD", "reason": "INCOMPLETE_CURRENT_CONTEXT"}
    if bundle.get("intent_id") != intent_id:
        return {"status": "HOLD", "reason": "STALE_INTENT"}
    artifacts = bundle.get("artifacts", {})
    if set(artifacts) != ROLES:
        return {"status": "HOLD", "reason": "INCOMPLETE_MANIFEST"}
    for role, path in current.items():
        try:
            matches = artifacts[role].get("sha256") == sha(path)
        except (OSError, AttributeError):
            matches = False
        if not matches:
            return {"status": "HOLD", "reason": "STALE_OR_MISSING_" + role.upper()}
    if type(bundle.get("exit_code")) is not int or bundle["exit_code"] != 0:
        return {"status": "HOLD", "reason": "FAILED_OR_MISSING_RESULT"}
    if not bundle.get("command") or "unchecked" not in bundle:
        return {"status": "HOLD", "reason": "INCOMPLETE_EXECUTION_METADATA"}
    return {
        "status": "READY_FOR_HUMAN_REVIEW_AUTHORITY_UNVERIFIED",
        "reason": "RECORDED_DIGESTS_MATCH",
    }
