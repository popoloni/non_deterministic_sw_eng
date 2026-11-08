import unittest
from replay_harness import (
    candidate_replay,
    circular_self_test,
    independent_replay_check,
)


class ReplayHarnessTests(unittest.TestCase):
    def setUp(self):
        self.stored = {
            "transaction_id": "T-HISTORY",
            "status": "AUTO_APPROVAL_ELIGIBLE",
            "policy_version": "approval-eur-v1",
        }
        self.current = {
            "transaction_id": "T-HISTORY",
            "status": "REVIEW_REQUIRED",
            "policy_version": "approval-eur-v2",
        }

    def test_reference_passes(self):
        self.assertTrue(
            independent_replay_check(
                candidate_replay("reference", self.stored, self.current), self.stored
            )
        )

    def test_shared_mistake_is_rejected(self):
        bad = candidate_replay("reevaluate_mutant", self.stored, self.current)
        self.assertTrue(circular_self_test(bad, self.current))
        self.assertFalse(independent_replay_check(bad, self.stored))

    def test_repeated_mutant_remains_wrong(self):
        for _ in range(3):
            self.assertFalse(
                independent_replay_check(
                    candidate_replay("reevaluate_mutant", self.stored, self.current),
                    self.stored,
                )
            )


if __name__ == "__main__":
    unittest.main()
