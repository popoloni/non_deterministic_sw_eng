"""Failures in the test machinery must never become mutation successes."""

import json
from pathlib import Path
import subprocess
import tempfile
import unittest
from unittest.mock import patch

import mutation_runner as runner


def completed_report(passed):
    return json.dumps(
        {
            "execution_status": "COMPLETE",
            "count_kind": "behavioral_records",
            "tests": [{"name": "contract", "kind": "behavioral", "pass": passed}],
            "passed": int(passed),
            "total": 1,
        }
    )


class MutationEvidenceTests(unittest.TestCase):
    def test_completed_failed_assertion_is_behavioral_failure(self):
        result = runner.interpret_result(1, completed_report(False), "")
        self.assertEqual(result["outcome"], "BEHAVIORAL_FAILURE")
        self.assertEqual(result["failed_behavioral_records"], ["contract"])

    def test_unchanged_behavior_is_a_survivor(self):
        self.assertEqual(
            runner.interpret_result(0, completed_report(True), "")["outcome"], "PASS"
        )

    def test_crash_without_completed_report_is_infrastructure_error(self):
        for stderr in (
            "SyntaxError: invalid syntax",
            "ModuleNotFoundError: missing",
            "RuntimeError: database unavailable",
        ):
            with self.subTest(stderr=stderr):
                result = runner.interpret_result(1, "", stderr)
                self.assertEqual(result["outcome"], "INFRASTRUCTURE_ERROR")
                self.assertEqual(result["failed_behavioral_records"], [])

    def test_inconsistent_exit_or_counts_is_infrastructure_error(self):
        data = json.loads(completed_report(False))
        data["total"] = 2
        for exit_code, stdout in (
            (0, completed_report(False)),
            (1, completed_report(True)),
            (1, json.dumps(data)),
        ):
            with self.subTest(exit_code=exit_code, stdout=stdout):
                self.assertEqual(
                    runner.interpret_result(exit_code, stdout, "")["outcome"],
                    "INFRASTRUCTURE_ERROR",
                )

    def test_timeout_is_infrastructure_error(self):
        with patch.object(
            runner.subprocess,
            "run",
            side_effect=subprocess.TimeoutExpired("oracle", 30),
        ):
            self.assertEqual(
                runner.run_oracle(Path("oracle.py"), Path.cwd())["outcome"],
                "INFRASTRUCTURE_ERROR",
            )

    def test_failing_baseline_stops_before_mutation(self):
        with tempfile.TemporaryDirectory() as temporary:
            with patch.object(
                runner, "run_oracle", return_value={"outcome": "BEHAVIORAL_FAILURE"}
            ):
                with patch.object(runner, "apply_fault") as apply_fault:
                    result = runner.campaign(Path(temporary))
            self.assertEqual(result["status"], "INFRASTRUCTURE_ERROR")
            self.assertEqual(result["mutants"], [])
            apply_fault.assert_not_called()


if __name__ == "__main__":
    unittest.main()
