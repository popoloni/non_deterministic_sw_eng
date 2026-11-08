"""Independent expected results derived from INT-001 and INT-002, not maker tests.
From lab/case_study: python -m unittest answer_keys.oracle_solution -v
Synthetic only; not a real authorization service.
"""

import tempfile
from pathlib import Path
import unittest
from approval_lab.domain import Transaction, ConflictError
from approval_lab.policy import Policy
from approval_lab.service import ApprovalService


def tx(
    tid="EXAMPLE-1",
    amount=400000,
    department="TREASURY",
    risk="LOW",
    cross_border=False,
):
    return Transaction(tid, amount, "EUR", department, risk, "reader", cross_border)


class IndependentContractExamples(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.v1 = Policy.from_file("policies/v1.json")
        cls.v2 = Policy.from_file("policies/v2.json")

    def test_changed_ceiling_and_inclusive_boundary(self):
        self.assertEqual(self.v1.evaluate(tx()).status, "AUTO_APPROVAL_ELIGIBLE")
        self.assertEqual(self.v2.evaluate(tx()).status, "REVIEW_REQUIRED")
        self.assertEqual(
            self.v1.evaluate(tx(amount=300000)).status, "AUTO_APPROVAL_ELIGIBLE"
        )
        self.assertEqual(
            self.v2.evaluate(tx(amount=300000)).status, "AUTO_APPROVAL_ELIGIBLE"
        )

    def test_high_risk_and_cross_border_fail_closed(self):
        for p in (self.v1, self.v2):
            self.assertEqual(
                p.evaluate(tx(amount=100, risk="HIGH")).status, "REVIEW_REQUIRED"
            )
            self.assertEqual(
                p.evaluate(tx(amount=100, cross_border=True)).status, "REVIEW_REQUIRED"
            )

    def test_unrecognized_department_fails_closed(self):
        self.assertEqual(
            self.v2.evaluate(tx(department="UNKNOWN")).status, "REVIEW_REQUIRED"
        )

    def test_old_idempotency_decision_and_conflict(self):
        with tempfile.TemporaryDirectory() as root:
            path = Path(root) / "test.sqlite"
            first = ApprovalService(path, self.v1)
            try:
                d1 = first.evaluate(tx(), "EXAMPLE-KEY-1")
                self.assertEqual(d1.status, "AUTO_APPROVAL_ELIGIBLE")
                self.assertEqual(d1.policy_version, self.v1.version)
            finally:
                first.close()
            second = ApprovalService(path, self.v2)
            try:
                replay = second.evaluate(tx(), "EXAMPLE-KEY-1")
                self.assertEqual(replay, d1)
                self.assertEqual(second.stored_decisions(), 1)
                with self.assertRaises(ConflictError):
                    second.evaluate(tx(amount=300000), "EXAMPLE-KEY-1")
                self.assertEqual(
                    second.evaluate(tx("EXAMPLE-2"), "EXAMPLE-KEY-2").status,
                    "REVIEW_REQUIRED",
                )
            finally:
                second.close()


if __name__ == "__main__":
    unittest.main()
