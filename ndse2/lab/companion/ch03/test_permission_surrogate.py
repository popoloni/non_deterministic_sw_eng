"""The permission example evaluates a configurable allowlist without egress."""

from pathlib import Path
import socket
import tempfile
import unittest
from unittest.mock import patch

from permission_bounded_surrogate import PermissionSurrogate, run_demo


class PermissionEnvelopeTests(unittest.TestCase):
    def test_empty_network_allowlist_denies(self):
        surrogate = PermissionSurrogate(Path.cwd())
        self.assertEqual(
            surrogate.request_network("https://example.org/upload"), "DENIED"
        )
        self.assertEqual(surrogate.events[-1]["reason"], "URL_OUTSIDE_ALLOWLIST")

    def test_only_exact_allowlisted_url_is_admitted_without_egress(self):
        allowed = "https://example.org/approved"
        surrogate = PermissionSurrogate(Path.cwd(), network_allowlist={allowed})
        with patch.object(
            socket, "socket", side_effect=AssertionError("network egress attempted")
        ):
            self.assertEqual(surrogate.request_network(allowed), "ALLOWED")
            self.assertEqual(surrogate.request_network(allowed + "-other"), "DENIED")
        self.assertTrue(all(event["performed"] is False for event in surrogate.events))

    def test_trace_parent_is_created_and_denial_count_is_derived(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            (root / "approval_lab").mkdir()
            (root / "approval_lab/service.py").write_text("# sample source\n")
            trace = root / "new/reports/trace.jsonl"
            report = run_demo(root, trace)
            self.assertTrue(trace.is_file())
            self.assertEqual(len(trace.read_text().splitlines()), 4)
            self.assertEqual(report["events"], 4)
            self.assertEqual(report["denials"], 2)


if __name__ == "__main__":
    unittest.main()
