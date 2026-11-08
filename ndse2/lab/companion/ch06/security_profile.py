"""Deterministic security-policy demonstrator. No shell, network or real credentials."""

from pathlib import Path
import json

ALLOWED_READS = {
    "approval_lab/domain.py",
    "approval_lab/policy.py",
    "tests/test_domain_policy.py",
}
ALLOWED_ACTIONS = {"read", "propose_patch", "run_tests"}
APPROVED_DEPENDENCIES = {"fixture-parser": "1.2.3"}


def authorize_request(role: str, amount_minor: int, policy_fn):
    if role != "approver":
        return {"status": "DENIED", "reason": "ROLE_NOT_AUTHORIZED"}
    result = policy_fn(amount_minor)
    return {"status": result}  # never returns internal audit/credential data


def validate_manifest(manifest):
    findings = []
    for name, version in manifest.get("dependencies", {}).items():
        if name not in APPROVED_DEPENDENCIES or version != APPROVED_DEPENDENCIES[name]:
            findings.append("UNAPPROVED_OR_UNPINNED_DEPENDENCY")
    for grant in manifest.get("permissions", []):
        if grant not in ALLOWED_ACTIONS:
            findings.append("OVERBROAD_PERMISSION")
    if manifest.get("network", False):
        findings.append("NETWORK_NOT_AUTHORIZED")
    return sorted(set(findings))


def broker(action, target="", root=None):
    if action == "network":
        return {"decision": "DENIED", "reason": "NO_NETWORK"}
    if action == "shell":
        return {"decision": "DENIED", "reason": "NO_SHELL"}
    if action == "read":
        if root is None or target not in ALLOWED_READS:
            return {"decision": "DENIED", "reason": "NOT_ALLOWLISTED"}
        path = (Path(root) / target).resolve()
        if not path.is_relative_to(Path(root).resolve()) or not path.is_file():
            return {"decision": "DENIED", "reason": "OUTSIDE_WORKSPACE_OR_MISSING"}
        return {"decision": "ALLOWED", "reason": "READ_ONLY"}
    if action == "propose_patch":
        return {"decision": "ALLOWED", "reason": "READY_FOR_REVIEW_ONLY"}
    return {"decision": "DENIED", "reason": "UNKNOWN_ACTION"}


def evaluate_untrusted_note(note, root):
    # No model and no parsing of instructions into actions: the note remains data.
    return {
        "note_treated_as": "UNTRUSTED_DATA",
        "network": broker("network", root=root),
        "secret_read": broker("read", "secrets/example.txt", root=root),
        "instruction_executed": False,
    }
