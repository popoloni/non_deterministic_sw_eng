"""Reader entry point for the offline NDSE laboratory.

Run from the companion root: python scripts/run_lab_checks.py
Uses only the Python standard library and synthetic local files.
"""

from pathlib import Path
import hashlib
import json
import os
import platform
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "audit/current_run"
OUT.mkdir(parents=True, exist_ok=True)
GUARD = ROOT / "scripts/offline_test_guard/offline_exec.py"
PHASES = [
    ("original_companion", "scripts/run_companion_checks_v10.py"),
    ("first_example", "lab/examples/policy_boundary.py"),
    ("case_trace", "scripts/build_case_trace.py"),
]


def main() -> int:
    environment = os.environ.copy()
    environment["PYTHONNOUSERSITE"] = "1"
    environment["PYTHONDONTWRITEBYTECODE"] = "1"
    results = []
    for name, relative in PHASES:
        command = [sys.executable, str(GUARD), str(ROOT / relative)]
        completed = subprocess.run(
            command,
            cwd=ROOT,
            env=environment,
            capture_output=True,
            text=True,
            timeout=120,
        )
        log = OUT / (name + ".log")
        log.write_text(completed.stdout + completed.stderr)
        results.append(
            {
                "phase": name,
                "script": relative,
                "script_sha256": hashlib.sha256(
                    (ROOT / relative).read_bytes()
                ).hexdigest(),
                "returncode": completed.returncode,
                "passed": completed.returncode == 0,
                "log": log.relative_to(ROOT).as_posix(),
            }
        )
        if completed.returncode != 0:
            break
    passed = len(results) == len(PHASES) and all(r["passed"] for r in results)
    report = {
        "python": platform.python_version(),
        "platform": platform.system(),
        "phases_passed": sum(r["passed"] for r in results),
        "phases_total": len(PHASES),
        "passed": passed,
        "results": results,
        "scope": "Synthetic local software execution. No model, participant study or production approval. The Python socket guard is a test aid, not an OS sandbox.",
    }
    if passed:
        original = json.loads(
            (ROOT / "audit/v10/companion_runs/RUN_SUMMARY.json").read_text()
        )
        chapter7 = json.loads((ROOT / "audit/v10/companion_runs/ch07.json").read_text())
        timeline = json.loads(
            (ROOT / "audit/case_trace/CH11_CASE_TIMELINE.json").read_text()
        )
        report["original_runner_gates"] = {
            "passed": original["passed"],
            "total": original["checks"],
        }
        report["chapter7_checks"] = {
            "passed": chapter7["passed"],
            "total": chapter7["total"],
        }
        report["chapter7_count_kind"] = chapter7["count_kind"]
        report["chapter7_counts"] = original["chapter7_counts"]
        report["historical_proposal_counts"] = timeline["historical_counts"]
        report["final_revision_recheck_counts"] = timeline[
            "current_revision_recheck_counts"
        ]
    (OUT / "LAB_CHECK_SUMMARY.json").write_text(json.dumps(report, indent=2) + "\n")
    print(
        json.dumps(
            {
                "phases_passed": report["phases_passed"],
                "phases_total": report["phases_total"],
                "passed": passed,
                "report": "audit/current_run/LAB_CHECK_SUMMARY.json",
            },
            indent=2,
        )
    )
    return 0 if passed else 1


if __name__ == "__main__":
    raise SystemExit(main())
