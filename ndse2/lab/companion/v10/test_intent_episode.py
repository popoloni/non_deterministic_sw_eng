"""Synthetic composition regression; no real agent or stakeholder."""

import json, sys, tempfile, unittest
from pathlib import Path

HERE = Path(__file__).resolve().parent
CASE = HERE.parents[1] / "case_study"
sys.path.insert(0, str(CASE))
from approval_lab.domain import Transaction, ConflictError
from approval_lab.policy import Policy
from approval_lab.service import ApprovalService


class IntentEpisode(unittest.TestCase):
    def test_authorized_delta_preserves_history(self):
        with tempfile.TemporaryDirectory() as tmp:
            db = Path(tmp) / "demo.sqlite"
            old = ApprovalService(db, Policy.from_file(CASE / "policies/v1.json"))
            tx = Transaction("T-HISTORY", 400000, "EUR", "TREASURY", "LOW", "demo")
            first = old.evaluate(tx, "idem-history")
            old.close()
            now = ApprovalService(db, Policy.from_file(CASE / "policies/v2.json"))
            try:
                self.assertEqual(first, now.evaluate(tx, "idem-history"))
                self.assertEqual("approval-eur-v1", first.policy_version)
                fresh = now.evaluate(
                    Transaction("T-NEW", 400000, "EUR", "TREASURY", "LOW", "demo"),
                    "idem-new",
                )
                self.assertEqual("REVIEW_REQUIRED", fresh.status)
                self.assertEqual("approval-eur-v2", fresh.policy_version)
                with self.assertRaises(ConflictError):
                    now.evaluate(
                        Transaction(
                            "T-HISTORY", 300000, "EUR", "TREASURY", "LOW", "demo"
                        ),
                        "idem-history",
                    )
                self.assertEqual(2, now.stored_decisions())
                self.assertEqual(
                    2, now.db.execute("SELECT COUNT(*) FROM audit").fetchone()[0]
                )
            finally:
                now.close()

    def test_clarification_scope_and_gap_records(self):
        q = json.loads((HERE / "clarifications.json").read_text())["questions"]
        self.assertTrue(q[0]["answer"])
        self.assertIsNone(q[1]["answer"])
        self.assertEqual(["help-heading publication only"], q[1]["blocks"])
        g = json.loads((HERE / "specification_gaps.json").read_text())["records"]
        self.assertEqual(3, len(g))
        self.assertTrue(all(x["source"] and x["owner"] and x["impact"] for x in g))


if __name__ == "__main__":
    unittest.main()
