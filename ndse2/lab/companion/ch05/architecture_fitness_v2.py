"""Synthetic architecture fitness: a negative control and versioned service behavior."""

import argparse
import ast
import json
from pathlib import Path
import sys
import tempfile


def case_directory(value):
    path = Path(value).resolve()
    for relative in (
        "approval_lab/__init__.py",
        "policies/v1.json",
        "policies/v2.json",
    ):
        if not (path / relative).is_file():
            raise argparse.ArgumentTypeError(f"case_root is missing {relative}")
    return path


def run_fitness(case):
    sys.path.insert(0, str(case))
    from approval_lab.policy import Policy
    from approval_lab.domain import Transaction, ConflictError
    from approval_lab.service import ApprovalService

    v1 = Policy.from_file(case / "policies/v1.json")
    v2 = Policy.from_file(case / "policies/v2.json")

    def tx(tid, amount=400000, risk="LOW", cross=False, department="TREASURY"):
        return Transaction(tid, amount, "EUR", department, risk, "fixture-user", cross)

    # Candidate A is an adapter with a duplicated stale ceiling; an intentionally flawed negative control.
    def candidate_a(amount_minor, risk="LOW", cross=False):
        if risk != "LOW" or cross:
            return "REVIEW_REQUIRED"
        return "AUTO_APPROVAL_ELIGIBLE" if amount_minor <= 500000 else "REVIEW_REQUIRED"

    # Candidate B delegates every policy decision to the domain interface.
    def candidate_b(policy, transaction):
        return policy.evaluate(transaction).status

    checks = []

    def check(name, condition, kind="fitness"):
        checks.append({"check": name, "passed": bool(condition), "kind": kind})

    check("A_v1_happy_path_passes", candidate_a(400000) == candidate_b(v1, tx("T-A")))
    check(
        "A_v2_boundary_is_detected_as_defect",
        candidate_a(400000) != candidate_b(v2, tx("T-B")),
        "negative-control",
    )
    check("B_v1_boundary", candidate_b(v1, tx("T-1")) == "AUTO_APPROVAL_ELIGIBLE")
    check("B_v2_boundary", candidate_b(v2, tx("T-2")) == "REVIEW_REQUIRED")
    for version, policy in [("v1", v1), ("v2", v2)]:
        check(
            version + "_high_risk",
            candidate_b(policy, tx("H-" + version, 100000, "HIGH"))
            == "REVIEW_REQUIRED",
        )
        check(
            version + "_cross_border",
            candidate_b(policy, tx("X-" + version, 100000, "LOW", True))
            == "REVIEW_REQUIRED",
        )
        check(
            version + "_unknown_department",
            candidate_b(policy, tx("U-" + version, 100000, department="UNKNOWN"))
            == "REVIEW_REQUIRED",
        )
    with tempfile.TemporaryDirectory() as td:
        db = Path(td) / "audit.sqlite"
        s = ApprovalService(db, v1)
        original = s.evaluate(tx("OLD"), "old-key")
        s.close()
        s = ApprovalService(db, v2)
        replay = s.evaluate(tx("OLD"), "old-key")
        fresh = s.evaluate(tx("NEW"), "new-key")
        check(
            "replay_preserves_v1_status",
            replay.status == original.status == "AUTO_APPROVAL_ELIGIBLE",
        )
        check(
            "replay_preserves_v1_provenance",
            replay.policy_version == original.policy_version == v1.version,
        )
        check(
            "new_v2_request_requires_review",
            fresh.status == "REVIEW_REQUIRED" and fresh.policy_version == v2.version,
        )
        check("audit_chain_contiguous", s.audit_is_contiguous())
        check("only_two_stored_decisions", s.stored_decisions() == 2)
        try:
            s.evaluate(tx("OLD", 300000), "old-key")
        except ConflictError:
            check("payload_conflict_rejected", True)
        else:
            check("payload_conflict_rejected", False)
        s.close()
    # A real architecture inspection: inspect production adapter AST for copied policy constant.
    policy_source = (case / "approval_lab/policy.py").read_text()
    service_source = (case / "approval_lab/service.py").read_text()
    service_ast = ast.parse(service_source)
    policy_ast = ast.parse(policy_source)
    service_imports = {
        n.module for n in ast.walk(service_ast) if isinstance(n, ast.ImportFrom)
    }
    check("service_depends_on_domain_policy", "policy" in service_imports)
    check("service_has_no_treasury_literal", "TREASURY" not in service_source)
    check("policy_contains_rule_ownership", "departments" in policy_source)
    report = {
        "passed": sum(x["passed"] for x in checks),
        "total": len(checks),
        "checks": checks,
        "interpretation": "Synthetic fitness tests only; no model-vendor comparison.",
    }
    return report


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("case_root", type=case_directory)
    args = parser.parse_args(argv)
    report = run_fitness(args.case_root)
    print(json.dumps(report, indent=2))
    return 0 if report["passed"] == report["total"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
