"""Reader entry points explain missing arguments and help without tracebacks."""

from pathlib import Path
import subprocess
import sys
import unittest

ROOT = Path(__file__).resolve().parents[3]
SCRIPTS = (
    "lab/companion/ch03/permission_bounded_surrogate.py",
    "lab/companion/ch04/ccs_native_gate.py",
    "lab/companion/ch05/architecture_fitness_v2.py",
    "lab/companion/ch07/independent_oracle_lab.py",
)


class ReaderCommandTests(unittest.TestCase):
    def execute(self, script, *arguments):
        return subprocess.run(
            [sys.executable, str(ROOT / script), *arguments],
            cwd=ROOT,
            text=True,
            capture_output=True,
            timeout=10,
        )

    def test_missing_arguments_show_usage(self):
        for script in SCRIPTS:
            with self.subTest(script=script):
                result = self.execute(script)
                self.assertEqual(result.returncode, 2)
                self.assertIn("usage:", result.stderr)
                self.assertNotIn("Traceback", result.stderr)

    def test_help_exits_successfully(self):
        for script in SCRIPTS:
            with self.subTest(script=script):
                result = self.execute(script, "--help")
                self.assertEqual(result.returncode, 0)
                self.assertIn("case_root", result.stdout)

    def test_invalid_case_directory_has_diagnostic(self):
        for script in SCRIPTS:
            with self.subTest(script=script):
                result = self.execute(script, "missing-case-directory")
                self.assertEqual(result.returncode, 2)
                self.assertIn("case_root", result.stderr)
                self.assertNotIn("Traceback", result.stderr)


if __name__ == "__main__":
    unittest.main()
