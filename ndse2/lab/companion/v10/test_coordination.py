import unittest
from coordination import Coordinator


class CoordinationTests(unittest.TestCase):
    def test_conflicting_target(self):
        c = Coordinator()
        _, g = c.grant("A", "policy", now=0, expiry=10)
        self.assertEqual(
            "HOLD_TARGET_ALREADY_LEASED", c.grant("B", "policy", now=1, expiry=10)[0]
        )
        self.assertEqual(
            "ADMITTED_TO_REVIEW_QUEUE_NOT_ACCEPTED",
            c.submit("e1", "A", "policy", "INT-002", g, now=1),
        )

    def test_expired(self):
        c = Coordinator()
        _, g = c.grant("A", "policy", now=0, expiry=10)
        self.assertEqual(
            "HOLD_EXPIRED_LEASE", c.submit("e1", "A", "policy", "INT-002", g, now=10)
        )

    def test_capacity(self):
        c = Coordinator(capacity=1)
        _, g1 = c.grant("A", "policy", now=0, expiry=10)
        _, g2 = c.grant("B", "docs", now=0, expiry=10)
        c.submit("e1", "A", "policy", "INT-002", g1, now=1)
        self.assertEqual(
            "HOLD_REVIEW_CAPACITY", c.submit("e2", "B", "docs", "INT-002", g2, now=1)
        )

    def test_duplicate_event_and_conflicting_reuse(self):
        c = Coordinator()
        _, g = c.grant("A", "policy", now=0, expiry=10)
        c.submit("e1", "A", "policy", "INT-002", g, now=1)
        self.assertEqual(
            "DUPLICATE_NO_NEW_SUBMISSION",
            c.submit("e1", "A", "policy", "INT-002", g, now=2),
        )
        self.assertEqual(1, len(c.pending))
        self.assertEqual(
            "HOLD_EVENT_ID_CONFLICT", c.submit("e1", "A", "docs", "INT-002", g, now=2)
        )

    def test_stale_intent(self):
        c = Coordinator()
        _, g = c.grant("A", "policy", now=0, expiry=10)
        c.change_intent("SCN-COORD")
        self.assertEqual(
            "HOLD_STALE_INTENT", c.submit("e1", "A", "policy", "INT-002", g, now=2)
        )

    def test_old_generation_cannot_reuse_new_lease(self):
        c = Coordinator()
        _, g1 = c.grant("A", "policy", now=0, expiry=10)
        c.revoke("policy", "late intention needs new lease")
        _, g2 = c.grant("A", "policy", now=1, expiry=20)
        self.assertNotEqual(g1, g2)
        self.assertEqual(
            "HOLD_WRONG_LEASE", c.submit("e1", "A", "policy", "INT-002", g1, now=2)
        )

    def test_withdraw_releases_capacity_without_acceptance(self):
        c = Coordinator(capacity=1)
        _, g = c.grant("A", "policy", now=0, expiry=10)
        c.submit("e1", "A", "policy", "INT-002", g, now=1)
        c.withdraw("e1", "superseded candidate")
        self.assertEqual(0, len(c.pending))
        self.assertIn("e1", c.events)


if __name__ == "__main__":
    unittest.main()
