#!/usr/bin/env python3
"""Offline runnable-scope checks. Synthetic software fixtures are not field evidence."""

from pathlib import Path
import subprocess, sys, json, os, re

R = Path(__file__).resolve().parents[1]
O = R / "audit/v10/companion_runs"
O.mkdir(parents=True, exist_ok=True)
C = R / "lab/case_study"
P = R / "lab/companion"
results = []
guard = R / "scripts/offline_test_guard"
os.environ["PYTHONPATH"] = str(guard) + os.pathsep + os.environ.get("PYTHONPATH", "")


def run(name, args, cwd=R, expected=0):
    p = subprocess.run(
        [sys.executable, str(guard / "offline_exec.py"), *map(str, args)],
        cwd=cwd,
        capture_output=True,
        text=True,
        timeout=90,
    )
    (O / (name + ".log")).write_text(p.stdout + p.stderr)
    assert p.returncode == expected, (name, p.returncode, p.stdout, p.stderr)
    results.append({"check": name, "passed": True, "returncode": p.returncode})
    return p.stdout


run("service_regression_19", ["-m", "unittest", "discover", "-s", "tests", "-q"], C)
run("answer_oracles_4", ["-m", "unittest", "answer_keys.oracle_solution", "-q"], C)
run("economic_calibration_5", [R / "audit/model/test_calibration.py"])
p = subprocess.run(
    [
        sys.executable,
        str(guard / "offline_exec.py"),
        str(R / "audit/model/calibrate_from_pilot.py"),
        str(R / "audit/pilot/real_pilot_template.csv"),
    ],
    capture_output=True,
    text=True,
)
(O / "empty_pilot.log").write_text(p.stdout + p.stderr)
assert p.returncode != 0 and "NO_REAL_PILOT_DATA" in p.stdout + p.stderr
results.append({"check": "empty_pilot_rejected", "passed": True})
s = run(
    "ch03_surrogate",
    [P / "ch03/permission_bounded_surrogate.py", C, O / "permission_trace.jsonl"],
)
assert json.loads(s)["denials"] == 2
lines = (O / "permission_trace.jsonl").read_text().splitlines()
assert len(lines) == 4 and all(json.loads(x) for x in lines)
run(
    "reader_permissions_and_cli", ["-m", "unittest", "discover", "-s", P / "ch03", "-v"]
)
s = run("ch04_intent_gate", [P / "ch04/ccs_native_gate.py", C])
j = json.loads(s)
(O / "ch04.json").write_text(s)
s = run("ch05_fitness", [P / "ch05/architecture_fitness_v2.py", C])
j = json.loads(s)
assert j["passed"] == 19 and j["total"] == 19
(O / "ch05.json").write_text(s)
run(
    "ch06_security_13", ["-m", "unittest", "-q", "test_security_profile.py"], P / "ch06"
)
s = run("ch07_oracles", [P / "ch07/independent_oracle_lab.py", C])
(O / "ch07.json").write_text(s)
s = run("ch07_mutations", [P / "ch07/mutation_runner.py", C])
j = json.loads(s)
assert j["status"] == "PASS" and j["source_unchanged"]
(O / "ch07_mutations.json").write_text(s)
s = run("ch07_relations", [P / "ch07/relation_examples.py", C])
j = json.loads(s)
assert j["status"] == "PASS"
(O / "ch07_relations.json").write_text(s)
run(
    "ch07_runner_infrastructure", ["-m", "unittest", "discover", "-s", P / "ch07", "-v"]
)
run("reader_artifacts", [R / "lab/examples/build_reader_artifacts.py"])
s = run(
    "ch09_retrieval",
    [
        P / "ch09/retrieval_handoff_agent.py",
        C,
        P / "ch09/holdout_questions.json",
        O / "retrieval",
    ],
)
j = json.loads(s)
assert j["baseline"]["top3_source_hit"] == 6 and j["memory"]["top3_source_hit"] == 8
run(
    "ch10_software_tests_14",
    ["-m", "unittest", "-q", "test_study_tools.py"],
    P / "ch10",
)
p = subprocess.run(
    [
        sys.executable,
        str(guard / "offline_exec.py"),
        str(P / "ch10/score.py"),
        str(P / "ch10/BLIND_RATINGS_TEMPLATE.csv"),
        "--key",
        str(P / "ch10/RATING_KEY_TEMPLATE.csv"),
    ],
    capture_output=True,
    text=True,
)
(O / "empty_ratings.log").write_text(p.stdout + p.stderr)
assert p.returncode != 0 and "NO_REAL_RATINGS" in p.stderr
results.append({"check": "empty_ratings_rejected", "passed": True})
s = run("ch11_governance", [P / "ch11/multi_agent_governance.py"])
j = json.loads(s)
assert j["counts"] == {"ready_for_human_review": 3, "rejected": 4}
(O / "ch11.json").write_text(s)
s = run(
    "v10_composed_regressions",
    ["-m", "unittest", "discover", "-s", P / "v10", "-v"],
    P / "v10",
)
run(
    "network_guard",
    ["-c", 'import socket; socket.create_connection(("example.invalid",443))'],
    expected=1,
)
assert "NETWORK_DISABLED_FOR_V10_TESTS" in (O / "network_guard.log").read_text()
chapter7 = json.loads((O / "ch07.json").read_text())
mutations = json.loads((O / "ch07_mutations.json").read_text())
relations = json.loads((O / "ch07_relations.json").read_text())
counts = {
    "behavioral_records": {"passed": chapter7["passed"], "total": chapter7["total"]},
    "mutants": mutations["summary"],
    "metamorphic_sampled_pairs": {
        "passed": relations["metamorphic"]["passed"],
        "total": relations["metamorphic"]["sampled_pairs"],
    },
    "differential_sampled_cases": {
        "passed": relations["differential"]["passed"],
        "total": relations["differential"]["sampled_cases"],
    },
    "relation_identity_controls": {
        "passed": relations["identity_controls"]["passed"],
        "total": relations["identity_controls"]["total"],
    },
}
(O / "RUN_SUMMARY.json").write_text(
    json.dumps(
        {
            "checks": len(results),
            "passed": len(results),
            "results": results,
            "chapter7_counts": counts,
            "scope": "Actual offline software execution only. Python network connections blocked by test guard; this is not an OS sandbox. No live model, human participant, deployment or field pilot.",
        },
        indent=2,
    )
    + "\n"
)
print(
    f"{len(results)}/{len(results)} companion execution gates passed; no study or production results created."
)
