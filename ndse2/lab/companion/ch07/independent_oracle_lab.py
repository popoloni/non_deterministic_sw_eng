"""Chapter 7 behavioral checks for the synthetic Treasury case.

Expected outcomes come from INT-001/INT-002 and their acceptance obligations.
The separate mutation_runner.py probes sensitivity to named implementation faults.
No network, model account, or real banking integration is required.
"""

import argparse
import json
from pathlib import Path
import sys
import tempfile


def case_directory(value):
    root = Path(value).resolve()
    required = (
        "approval_lab/__init__.py",
        "policies/v1.json",
        "policies/v2.json",
        "docs/01_intent_contract.json",
        "docs/02_late_intent_delta.json",
    )
    missing = [name for name in required if not (root / name).is_file()]
    if missing:
        raise argparse.ArgumentTypeError(
            f"not a case-study root: {root}; missing {', '.join(missing)}"
        )
    return root


def run_checks(root):
    sys.path.insert(0, str(root))
    from approval_lab.domain import ConflictError, Transaction
    from approval_lab.policy import Policy
    from approval_lab.service import ApprovalService

    intent = json.loads((root / "docs/01_intent_contract.json").read_text())
    delta = json.loads((root / "docs/02_late_intent_delta.json").read_text())
    if intent["intent_id"] != "INT-001" or delta["base_intent"] != "INT-001":
        raise ValueError("the oracle requires the INT-001 / INT-002 case contracts")
    v1 = Policy.from_file(root / "policies/v1.json")
    v2 = Policy.from_file(root / "policies/v2.json")
    checks = []

    def tx(tid, amount=400000, risk="LOW", cross=False, dept="TREASURY"):
        return Transaction(tid, amount, "EUR", dept, risk, "case-user", cross)

    def record(name, actual, expected):
        checks.append(
            {
                "name": name,
                "actual": actual,
                "expected": expected,
                "pass": actual == expected,
                "kind": "behavioral",
            }
        )

    def counts(service):
        return {
            "decisions": service.stored_decisions(),
            "audit_rows": service.db.execute("SELECT COUNT(*) FROM audit").fetchone()[
                0
            ],
        }

    record(
        "contract_high_risk",
        v2.evaluate(tx("H", 100, "HIGH")).status,
        "REVIEW_REQUIRED",
    )
    record(
        "contract_cross_border",
        v1.evaluate(tx("X", 100, "LOW", True)).status,
        "REVIEW_REQUIRED",
    )
    record("v1_treasury_4000", v1.evaluate(tx("A")).status, "AUTO_APPROVAL_ELIGIBLE")
    record("v2_treasury_4000", v2.evaluate(tx("B")).status, "REVIEW_REQUIRED")
    record(
        "v2_boundary_3000",
        v2.evaluate(tx("C", 300000)).status,
        "AUTO_APPROVAL_ELIGIBLE",
    )
    record(
        "v2_boundary_3000_plus_one",
        v2.evaluate(tx("D", 300001)).status,
        "REVIEW_REQUIRED",
    )
    for amount in (1, 300000, 300001, 400000, 500000, 500001):
        record(
            "high_risk_property_" + str(amount),
            v2.evaluate(tx("HP" + str(amount), amount, "HIGH")).status,
            "REVIEW_REQUIRED",
        )
    unknown = v2.evaluate(tx("UNKNOWN", 100, dept="UNLISTED"))
    record(
        "unknown_department_status_and_reason",
        [unknown.status, unknown.reason_code],
        ["REVIEW_REQUIRED", "UNRECOGNIZED_DEPARTMENT"],
    )

    with tempfile.TemporaryDirectory() as tmp:
        db = Path(tmp) / "audit.sqlite"
        service = ApprovalService(db, v1)
        original = service.evaluate(tx("OLD"), "old-key")
        before_replay = counts(service)
        service.close()
        service = ApprovalService(db, v2)
        try:
            replay = service.evaluate(tx("OLD"), "old-key")
            record("replay_status", replay.status, original.status)
            record("replay_version", replay.policy_version, original.policy_version)
            record(
                "replay_preserves_audit_row_count",
                counts(service)["audit_rows"],
                before_replay["audit_rows"],
            )
            fresh = service.evaluate(tx("NEW"), "new-key")
            record("new_policy_v2", fresh.status, "REVIEW_REQUIRED")
            try:
                service.evaluate(tx("OLD", 300000), "old-key")
            except ConflictError:
                conflict = True
            else:
                conflict = False
            record("changed_payload_conflict", conflict, True)
            before_conflict = counts(service)
            try:
                service.evaluate(tx("OLD"), "another-key")
            except ConflictError:
                conflict = True
            else:
                conflict = False
            record(
                "existing_transaction_new_key_conflict",
                {"conflict": conflict, "counts": counts(service)},
                {"conflict": True, "counts": before_conflict},
            )
            record("audit_continuity", service.audit_is_contiguous(), True)
        finally:
            service.close()
        # Corruption is isolated so it cannot contaminate the valid-chain checks.
        corrupted = ApprovalService(Path(tmp) / "tampered.sqlite", v2)
        try:
            corrupted.evaluate(tx("TAMPER", 100), "tamper-key")
            corrupted.db.execute("UPDATE audit SET event_json = event_json || ' '")
            record(
                "tampered_audit_row_rejected", corrupted.audit_is_contiguous(), False
            )
        finally:
            corrupted.close()
    passed = sum(check["pass"] for check in checks)
    return {
        "schema_version": 2,
        "execution_status": "COMPLETE",
        "case": "synthetic offline",
        "authority": "INT-001/INT-002 illustrative only",
        "tests": checks,
        "passed": passed,
        "total": len(checks),
        "count_kind": "behavioral_records",
        "candidate_state": "READY_FOR_REVIEW" if passed == len(checks) else "REJECTED",
        "acceptance": "NOT_AUTHORIZED",
    }


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "case_root",
        type=case_directory,
        help="directory containing approval_lab, policies and docs",
    )
    args = parser.parse_args(argv)
    try:
        report = run_checks(args.case_root)
    except Exception as error:
        print(
            json.dumps(
                {
                    "schema_version": 2,
                    "execution_status": "ERROR",
                    "error_type": type(error).__name__,
                    "error": str(error),
                },
                indent=2,
            )
        )
        return 2
    print(json.dumps(report, indent=2))
    return 0 if report["passed"] == report["total"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
