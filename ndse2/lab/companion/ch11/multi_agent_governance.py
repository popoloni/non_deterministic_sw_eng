"""Deterministic multi-agent/reviewer governance *simulation*.
Agents are simulated proposals, not LLM invocations. No production release.
Run: python multi_agent_governance.py [output.json]
"""

from dataclasses import dataclass, asdict
from typing import Optional
import json, sys


@dataclass(frozen=True)
class Proposal:
    ident: str
    actor: str
    intent: str
    base_revision: int
    files: tuple
    evidence: tuple
    reviewer: str
    checker: str
    asks_release: bool = False
    approval_signature: Optional[str] = None


AUTHORITY = {"INT-001": 1, "INT-002": 2}
ALLOWED = {
    "policies/v2.json",
    "approval_lab/policy.py",
    "tests/test_domain_policy.py",
    "docs/02_late_intent_delta.json",
}
REQUIRED = {"independent_policy_tests", "replay_regression"}


def gate(p: Proposal, current_revision: int, lock_owners: dict):
    reasons = []
    if p.intent not in AUTHORITY:
        reasons.append("UNKNOWN_INTENT")
    elif p.base_revision != current_revision or p.base_revision != AUTHORITY[p.intent]:
        reasons.append("STALE_INTENT_REVISION")
    if not set(p.files) <= ALLOWED:
        reasons.append("PATH_OUTSIDE_ALLOWLIST")
    if "policies/v2.json" in p.files and p.intent != "INT-002":
        reasons.append("WRONG_POLICY_REVISION")
    if p.actor == p.reviewer:
        reasons.append("SELF_REVIEW")
    if p.actor == p.checker or p.checker == p.reviewer:
        reasons.append("NO_INDEPENDENT_CHECKER")
    if not REQUIRED <= set(p.evidence):
        reasons.append("MISSING_INDEPENDENT_EVIDENCE")
    for f in p.files:
        if f in lock_owners and lock_owners[f] != p.ident:
            reasons.append("FILE_OWNERSHIP_CONFLICT:" + f)
    if p.asks_release:
        reasons.append("RELEASE_NOT_AUTHORIZED_IN_LAB")
    if p.approval_signature is not None:
        reasons.append("UNVERIFIED_SIGNATURE_NOT_ACCEPTED")
    return {
        "proposal": p.ident,
        "state": "REJECTED" if reasons else "READY_FOR_HUMAN_REVIEW",
        "reasons": reasons,
        "human_approval_verified": False,
    }


proposals = [
    Proposal(
        "A1",
        "agent_A",
        "INT-001",
        1,
        ("approval_lab/policy.py",),
        ("independent_policy_tests", "replay_regression"),
        "reviewer_1",
        "checker_1",
    ),
    Proposal(
        "B1",
        "agent_B",
        "INT-001",
        1,
        ("approval_lab/policy.py",),
        ("independent_policy_tests", "replay_regression"),
        "reviewer_2",
        "checker_2",
    ),
    Proposal(
        "B2",
        "agent_B",
        "INT-002",
        2,
        ("policies/v2.json",),
        ("independent_policy_tests", "replay_regression"),
        "reviewer_2",
        "checker_2",
    ),
    Proposal(
        "A2",
        "agent_A",
        "INT-001",
        1,
        ("policies/v2.json",),
        ("independent_policy_tests", "replay_regression"),
        "reviewer_1",
        "checker_1",
    ),
    Proposal(
        "C2",
        "agent_C",
        "INT-002",
        2,
        ("tests/test_domain_policy.py",),
        ("independent_policy_tests",),
        "reviewer_3",
        "checker_3",
    ),
    Proposal(
        "D2",
        "agent_D",
        "INT-002",
        2,
        (".env",),
        ("independent_policy_tests", "replay_regression"),
        "agent_D",
        "agent_D",
        True,
        "self-declared",
    ),
    Proposal(
        "E2",
        "agent_E",
        "INT-002",
        2,
        ("docs/02_late_intent_delta.json",),
        ("independent_policy_tests", "replay_regression"),
        "reviewer_4",
        "checker_4",
    ),
]
results = []
lock = {}
revision = 1
for p in proposals:
    if p.ident == "B2":
        revision = 2
        lock = {}  # Authorized delta invalidates prior unmerged lock state
    result = gate(p, revision, lock)
    results.append(result)
    if result["state"] == "READY_FOR_HUMAN_REVIEW":
        for f in p.files:
            lock[f] = p.ident
# Tests for expected behavior, not outcomes measured from real agents
expected = {
    "A1": "READY_FOR_HUMAN_REVIEW",
    "B1": "REJECTED",
    "A2": "REJECTED",
    "B2": "READY_FOR_HUMAN_REVIEW",
    "C2": "REJECTED",
    "D2": "REJECTED",
    "E2": "READY_FOR_HUMAN_REVIEW",
}
assert {x["proposal"]: x["state"] for x in results} == expected
assert any("FILE_OWNERSHIP_CONFLICT" in s for x in results for s in x["reasons"])
assert any("STALE_INTENT_REVISION" in s for x in results for s in x["reasons"])
assert all(not x["human_approval_verified"] for x in results)
report = {
    "scenarios": results,
    "counts": {
        "ready_for_human_review": sum(
            x["state"] == "READY_FOR_HUMAN_REVIEW" for x in results
        ),
        "rejected": sum(x["state"] == "REJECTED" for x in results),
    },
    "interpretation": "Deterministic control simulation. No LLM agents, human reviewers, cryptographic approvals or production releases were executed.",
}
print(json.dumps(report, indent=2))
if len(sys.argv) > 1:
    open(sys.argv[1], "w").write(json.dumps(report, indent=2))
