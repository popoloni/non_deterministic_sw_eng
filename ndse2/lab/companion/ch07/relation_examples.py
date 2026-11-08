"""Check two precisely scoped, finite relations on the pure routing policy.

Metamorphic: with the policy, EUR currency, department, risk, cross-border flag
and requester fixed, increasing a valid positive integer amount cannot turn
REVIEW_REQUIRED into AUTO_APPROVAL_ELIGIBLE.

Differential: compare status only between v1 and v2, without persisted replay.
The statuses differ exactly for LOW-risk domestic Treasury amounts from 300001
through 500000 cents inclusive. Whole Decision objects also carry version data.
"""

import argparse
import dataclasses
import itertools
import json
from pathlib import Path
import sys
import tempfile

from independent_oracle_lab import case_directory

AMOUNTS = (
    1,
    99999,
    100000,
    299999,
    300000,
    300001,
    400000,
    499999,
    500000,
    500001,
    999999,
    1000000,
    1000001,
    10**12,
)


def run_relations(root):
    sys.path.insert(0, str(root))
    from approval_lab.domain import ConflictError, Transaction
    from approval_lab.policy import Policy
    from approval_lab.service import ApprovalService

    policies = {
        version: Policy.from_file(root / f"policies/{version}.json")
        for version in ("v1", "v2")
    }
    contexts = list(
        itertools.product(
            ("TREASURY", "OPS", "UNKNOWN"), ("LOW", "HIGH"), (False, True)
        )
    )

    def transaction(
        amount,
        department="TREASURY",
        risk="LOW",
        cross_border=False,
        identifier="PURE-POLICY",
    ):
        return Transaction(
            identifier, amount, "EUR", department, risk, "case-reader", cross_border
        )

    pairs = []
    for version, policy in policies.items():
        for department, risk, cross in contexts:
            for smaller, larger in itertools.combinations(AMOUNTS, 2):
                lower = policy.evaluate(
                    transaction(smaller, department, risk, cross)
                ).status
                higher = policy.evaluate(
                    transaction(larger, department, risk, cross)
                ).status
                pairs.append(
                    {
                        "policy": version,
                        "department": department,
                        "risk": risk,
                        "cross_border": cross,
                        "smaller": smaller,
                        "larger": larger,
                        "pass": not (
                            lower == "REVIEW_REQUIRED"
                            and higher == "AUTO_APPROVAL_ELIGIBLE"
                        ),
                    }
                )

    cases, boundaries, countercontexts = [], [], []
    for department, risk, cross in contexts:
        for amount in AMOUNTS:
            tx = transaction(amount, department, risk, cross)
            first, second = (policies[v].evaluate(tx) for v in ("v1", "v2"))
            expected_difference = (
                department == "TREASURY"
                and risk == "LOW"
                and not cross
                and 300001 <= amount <= 500000
            )
            row = {
                "department": department,
                "risk": risk,
                "cross_border": cross,
                "amount_minor": amount,
                "v1_status": first.status,
                "v2_status": second.status,
                "expected_status_difference": expected_difference,
                "pass": (first.status != second.status) == expected_difference,
            }
            cases.append(row)
            if department == "TREASURY" and risk == "LOW" and not cross:
                if amount in (300000, 300001, 500000, 500001):
                    boundaries.append(
                        {
                            **row,
                            "v1_policy_version": first.policy_version,
                            "v2_policy_version": second.policy_version,
                            "whole_decisions_equal": first == second,
                        }
                    )
            if amount == 400000 and (department, risk, cross) in (
                ("TREASURY", "HIGH", False),
                ("TREASURY", "LOW", True),
                ("OPS", "LOW", False),
                ("UNKNOWN", "LOW", False),
            ):
                countercontexts.append(row)

    # Relations use pure evaluation. Service replay has a different contract.
    with tempfile.TemporaryDirectory(prefix="ndse-relations-") as temporary:
        database = Path(temporary) / "case.sqlite"
        service = ApprovalService(database, policies["v1"])
        original = service.evaluate(transaction(400000, identifier="OLD"), "old-key")
        try:
            service.evaluate(transaction(500000, identifier="OLD"), "old-key")
        except ConflictError:
            changed_payload_conflict = True
        else:
            changed_payload_conflict = False
        service.close()
        service = ApprovalService(database, policies["v2"])
        replay = service.evaluate(transaction(400000, identifier="OLD"), "old-key")
        fresh = service.evaluate(transaction(400000, identifier="NEW"), "new-key")
        service.close()
    identity = [
        {"name": "changed_amount_same_key_conflicts", "pass": changed_payload_conflict},
        {"name": "replay_preserves_original_decision", "pass": replay == original},
        {
            "name": "fresh_id_and_key_use_v2",
            "pass": fresh.policy_version == "approval-eur-v2"
            and fresh.status == "REVIEW_REQUIRED",
        },
    ]
    return {
        "schema_version": 1,
        "status": (
            "PASS" if all(row["pass"] for row in pairs + cases + identity) else "FAIL"
        ),
        "scope": "Finite boundary-focused samples; not an exhaustive proof over all valid amounts.",
        "comparison": "status only",
        "amounts_sampled": AMOUNTS,
        "contexts_per_policy": len(contexts),
        "metamorphic": {
            "sampled_pairs": len(pairs),
            "passed": sum(row["pass"] for row in pairs),
            "failures": [row for row in pairs if not row["pass"]],
        },
        "differential": {
            "sampled_cases": len(cases),
            "passed": sum(row["pass"] for row in cases),
            "failures": [row for row in cases if not row["pass"]],
            "boundary_examples": boundaries,
            "countercontexts": countercontexts,
        },
        "identity_controls": {
            "total": len(identity),
            "passed": sum(row["pass"] for row in identity),
            "checks": identity,
            "original": dataclasses.asdict(original),
            "replay": dataclasses.asdict(replay),
            "fresh": dataclasses.asdict(fresh),
        },
        "service_guidance": "Use pure Policy.evaluate, or fresh transaction IDs AND fresh idempotency keys. Historical replay is a separate contract.",
    }


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("case_root", type=case_directory)
    args = parser.parse_args(argv)
    report = run_relations(args.case_root)
    print(json.dumps(report, indent=2))
    return 0 if report["status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
