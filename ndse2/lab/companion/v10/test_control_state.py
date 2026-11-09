import tempfile, unittest
from dataclasses import replace
from pathlib import Path
from control_state import LoopState, admit, record_diagnostic


class ControlStateTests(unittest.TestCase):
    def step(self, state, **overrides):
        args = dict(
            current_intent="INT-002",
            current_contract_digest="synthetic-contract-v2",
            now=10,
            next_upper_bound_minor=50,
        )
        args.update(overrides)
        return admit(state, **args)

    def test_action_not_acceptance(self):
        status, state = self.step(LoopState(), new_candidate=True)
        self.assertEqual(status, "ACTION_ADMITTED_NOT_ACCEPTED")
        self.assertEqual(
            (state.used_minor, state.calls_used, state.attempts_used), (50, 1, 1)
        )

    def test_cost_exhaustion(self):
        original = replace(LoopState(), used_minor=190)
        status, unchanged = self.step(original, next_upper_bound_minor=20)
        self.assertEqual(status, "STOP_BUDGET")
        self.assertEqual(unchanged, original)

    def test_restart_retains_budget(self):
        state = replace(LoopState(), used_minor=200, calls_used=2)
        with tempfile.TemporaryDirectory() as folder:
            path = Path(folder) / "state.json"
            state.save(path)
            restored = LoopState.load(path)
            self.assertEqual(restored, state)
            self.assertEqual(self.step(restored)[0], "STOP_BUDGET")

    def test_stale_intent_and_digest(self):
        self.assertEqual(
            self.step(replace(LoopState(), intent="INT-001"))[0], "STOP_STALE_INTENT"
        )
        self.assertEqual(
            self.step(replace(LoopState(), contract_digest="old"))[0],
            "STOP_STALE_INTENT",
        )

    def test_deadline_and_revocation(self):
        self.assertEqual(self.step(LoopState(), now=900)[0], "STOP_DEADLINE")
        self.assertEqual(
            self.step(replace(LoopState(), revoked=True))[0], "STOP_REVOKED"
        )

    def test_unknown_cost_and_call_limit(self):
        self.assertEqual(
            self.step(LoopState(), next_upper_bound_minor=None)[0],
            "STOP_UNBOUNDED_COST",
        )
        self.assertEqual(
            self.step(replace(LoopState(), calls_used=4))[0], "STOP_BUDGET"
        )

    def test_repeat_and_attempt_limit(self):
        state = record_diagnostic(record_diagnostic(LoopState(), "REPLAY"), "REPLAY")
        self.assertEqual(self.step(state)[0], "ESCALATE_REPEATED_DIAGNOSTIC")
        self.assertEqual(
            self.step(replace(LoopState(), attempts_used=2), new_candidate=True)[0],
            "STOP_ATTEMPTS",
        )

    def test_invalid_reservation_rejected(self):
        for cost in (-1, True, float("nan")):
            with self.assertRaises(ValueError):
                self.step(LoopState(), next_upper_bound_minor=cost)


if __name__ == "__main__":
    unittest.main()
