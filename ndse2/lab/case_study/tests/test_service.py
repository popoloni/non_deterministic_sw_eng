import tempfile
import unittest
from pathlib import Path
from approval_lab.domain import Transaction, ConflictError
from approval_lab.policy import Policy
from approval_lab.service import ApprovalService

ROOT = Path(__file__).resolve().parents[1]


def make_tx(tid="T-200", amount=400000):
    return Transaction(tid, amount, "EUR", "TREASURY", "LOW", "demo-user")


class ServiceTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.path = Path(self.tmp.name) / "evidence.sqlite"
        self.v1 = Policy.from_file(ROOT / "policies/v1.json")
        self.v2 = Policy.from_file(ROOT / "policies/v2.json")

    def tearDown(self):
        self.tmp.cleanup()

    def test_replay_is_same_and_not_double_audited(self):
        svc = ApprovalService(self.path, self.v1)
        try:
            first = svc.evaluate(make_tx(), "idem-1")
            second = svc.evaluate(make_tx(), "idem-1")
            self.assertEqual(first, second)
            self.assertEqual(1, svc.stored_decisions())
            self.assertEqual(
                1, svc.db.execute("SELECT COUNT(*) FROM audit").fetchone()[0]
            )
            self.assertTrue(svc.audit_is_contiguous())
        finally:
            svc.close()

    def test_payload_change_with_same_key_conflicts(self):
        svc = ApprovalService(self.path, self.v1)
        try:
            svc.evaluate(make_tx(), "idem-1")
            with self.assertRaises(ConflictError):
                svc.evaluate(make_tx(amount=300000), "idem-1")
            self.assertTrue(svc.audit_is_contiguous())
            self.assertEqual(1, svc.stored_decisions())
        finally:
            svc.close()

    def test_duplicate_transaction_with_new_key_conflicts(self):
        svc = ApprovalService(self.path, self.v1)
        try:
            svc.evaluate(make_tx(), "idem-1")
            with self.assertRaises(ConflictError):
                svc.evaluate(make_tx(), "idem-2")
        finally:
            svc.close()

    def test_version_delta_preserves_prior_replay(self):
        svc = ApprovalService(self.path, self.v1)
        first = svc.evaluate(make_tx(), "idem-old")
        svc.close()
        new = ApprovalService(self.path, self.v2)
        try:
            replay = new.evaluate(make_tx(), "idem-old")
            self.assertEqual(first, replay)
            self.assertEqual("approval-eur-v1", replay.policy_version)
            changed = new.evaluate(make_tx("T-NEW"), "idem-new")
            self.assertEqual("REVIEW_REQUIRED", changed.status)
            self.assertEqual("approval-eur-v2", changed.policy_version)
            self.assertTrue(new.audit_is_contiguous())
            self.assertEqual(2, new.stored_decisions())
        finally:
            new.close()

    def test_evidence_chain_corruption_is_detected(self):
        svc = ApprovalService(self.path, self.v1)
        try:
            svc.evaluate(make_tx(), "idem-1")
            svc.db.execute("UPDATE audit SET event_json='changed' WHERE sequence=1")
            self.assertFalse(svc.audit_is_contiguous())
        finally:
            svc.close()

    def test_replay_after_policy_change_is_old_decision(self):
        svc = ApprovalService(self.path, self.v1)
        self.assertEqual(
            "AUTO_APPROVAL_ELIGIBLE", svc.evaluate(make_tx(), "idem-1").status
        )
        svc.close()
        svc = ApprovalService(self.path, self.v2)
        try:
            self.assertEqual(
                "AUTO_APPROVAL_ELIGIBLE", svc.evaluate(make_tx(), "idem-1").status
            )
        finally:
            svc.close()


if __name__ == "__main__":
    unittest.main()
