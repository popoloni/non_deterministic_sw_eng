"""Evaluate a local file/network permission envelope and record four sample events.

Network requests are policy decisions only: this surrogate never sends traffic.
"""

import argparse
import json
from pathlib import Path

ALLOWED_FILES = frozenset(
    {
        "approval_lab/domain.py",
        "approval_lab/service.py",
        "tests/test_service.py",
        "tests/test_domain_policy.py",
    }
)
NETWORK_ALLOWLIST = frozenset()


class PermissionSurrogate:
    def __init__(
        self, root, allowed_files=ALLOWED_FILES, network_allowlist=NETWORK_ALLOWLIST
    ):
        self.root = Path(root).resolve()
        self.allowed_files = frozenset(allowed_files)
        self.network_allowlist = frozenset(network_allowlist)
        self.events = []

    def event(self, action, target, decision, **details):
        self.events.append(
            {"action": action, "target": target, "decision": decision, **details}
        )

    def read(self, relative):
        target = (self.root / relative).resolve()
        if relative not in self.allowed_files or not target.is_relative_to(self.root):
            self.event("read", relative, "DENIED")
            return None
        if not target.is_file():
            self.event("read", relative, "MISSING")
            return None
        self.event("read", relative, "ALLOWED")
        return target.read_text(encoding="utf-8")

    def request_network(self, url):
        """Evaluate exact approved URLs; even an allowed request is not sent."""
        allowed = url in self.network_allowlist
        decision = "ALLOWED" if allowed else "DENIED"
        self.event(
            "network",
            url,
            decision,
            performed=False,
            reason="URL_IN_ALLOWLIST" if allowed else "URL_OUTSIDE_ALLOWLIST",
        )
        return decision


def case_directory(value):
    path = Path(value).resolve()
    if not (path / "approval_lab").is_dir():
        raise argparse.ArgumentTypeError("case_root must contain approval_lab/")
    return path


def run_demo(root, trace):
    surrogate = PermissionSurrogate(root)
    surrogate.read("approval_lab/service.py")
    surrogate.read("../private.env")
    surrogate.request_network("https://example.org/upload")
    surrogate.event(
        "propose", "candidate:inspect-high-risk-routing", "READY_FOR_REVIEW"
    )
    trace.parent.mkdir(parents=True, exist_ok=True)
    trace.write_text(
        "\n".join(json.dumps(event) for event in surrogate.events) + "\n",
        encoding="utf-8",
    )
    return {
        "status": "READY_FOR_REVIEW",
        "events": len(surrogate.events),
        "denials": sum(event["decision"] == "DENIED" for event in surrogate.events),
        "network_requests_performed": 0,
        "envelope": {
            "allowed_files": sorted(surrogate.allowed_files),
            "network_allowlist": sorted(surrogate.network_allowlist),
        },
        "trace": str(trace),
    }


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("case_root", type=case_directory)
    parser.add_argument(
        "trace", type=Path, help="JSONL destination; parent directories are created"
    )
    args = parser.parse_args(argv)
    print(json.dumps(run_demo(args.case_root, args.trace), indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
