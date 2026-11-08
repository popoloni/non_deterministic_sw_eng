import copy, tempfile, unittest
from pathlib import Path
from evidence_manifest import make_manifest, verify_manifest
from file_broker import FileBroker
from replay_harness import (
    candidate_replay,
    circular_self_test,
    independent_replay_check,
)


class EvidenceTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name)
        self.paths = {}
        for role, rel in {
            "candidate": "candidate/policy_patch.txt",
            "intent": "authority/intent.json",
            "oracle": "oracle/expected.json",
            "environment": "environment.txt",
        }.items():
            p = self.root / rel
            p.parent.mkdir(parents=True, exist_ok=True)
            p.write_text(role + "-v2")
            self.paths[role] = p
        self.bundle = make_manifest(
            self.paths,
            "INT-002",
            ["synthetic-check"],
            0,
            ["real authority", "production safety"],
            1,
        )

    def tearDown(self):
        self.tmp.cleanup()

    def test_matching_is_ready_not_accepted(self):
        r = verify_manifest(self.bundle, self.paths, "INT-002")
        self.assertEqual("READY_FOR_HUMAN_REVIEW_AUTHORITY_UNVERIFIED", r["status"])
        self.assertFalse(self.bundle["producer_authenticated"])

    def test_stale_intent(self):
        self.assertEqual(
            "STALE_INTENT",
            verify_manifest(self.bundle, self.paths, "SCN-EVIDENCE")["reason"],
        )

    def test_changed_artifacts(self):
        for role in self.paths:
            with self.subTest(role=role):
                p = self.paths[role]
                old = p.read_text()
                p.write_text(old + "changed")
                self.assertEqual(
                    "HOLD",
                    verify_manifest(self.bundle, self.paths, "INT-002")["status"],
                )
                p.write_text(old)

    def test_failed_result_and_missing_role(self):
        failed = copy.deepcopy(self.bundle)
        failed["exit_code"] = 1
        self.assertEqual(
            "HOLD", verify_manifest(failed, self.paths, "INT-002")["status"]
        )
        missing = copy.deepcopy(self.bundle)
        del missing["artifacts"]["oracle"]
        self.assertEqual(
            "HOLD", verify_manifest(missing, self.paths, "INT-002")["status"]
        )

    def test_shared_bug_and_protected_expected(self):
        stored = {
            "status": "AUTO_APPROVAL_ELIGIBLE",
            "policy_version": "approval-eur-v1",
        }
        current = {"status": "REVIEW_REQUIRED", "policy_version": "approval-eur-v2"}
        wrong = candidate_replay("reevaluate_mutant", stored, current)
        self.assertTrue(circular_self_test(wrong, current))
        self.assertFalse(independent_replay_check(wrong, stored))
        before = self.paths["oracle"].read_bytes()
        broker = FileBroker(self.root)
        self.assertEqual(
            "DENIED",
            broker.invoke(
                "demo-maker",
                "write_candidate",
                "oracle/expected.json",
                "make test pass",
                now=2,
            )["status"],
        )
        self.assertEqual(before, self.paths["oracle"].read_bytes())


if __name__ == "__main__":
    unittest.main()
