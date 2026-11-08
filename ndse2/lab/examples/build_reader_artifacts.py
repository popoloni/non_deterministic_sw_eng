"""Generate actual, small artifacts for the printed laboratory excerpts.

Run from the companion root. Default output is audit/reader_artifacts; the
edition reference copies live in lab/reader_artifacts and are explicitly named
with --output only when preparing a new edition.
"""

import argparse
import hashlib
import json
from pathlib import Path
import platform
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[2]
CASE = ROOT / "lab/case_study"


def write_json(path, value):
    path.write_text(
        json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )


def generate(output):
    output.mkdir(parents=True, exist_ok=True)
    for chapter in ("ch03", "ch05", "v10"):
        sys.path.insert(0, str(ROOT / "lab/companion" / chapter))
    from permission_bounded_surrogate import run_demo
    from architecture_fitness_v2 import run_fitness
    from evidence_manifest import make_manifest, verify_manifest
    from memory_scope import check_threshold_card

    intention_versions = []
    for filename, contract_path, intent_field in (
        ("v1", "docs/01_intent_contract.json", "intent_id"),
        ("v2", "docs/02_late_intent_delta.json", "delta_id"),
    ):
        policy = json.loads((CASE / f"policies/{filename}.json").read_text())
        contract = json.loads((CASE / contract_path).read_text())
        intention_versions.append(
            {
                "intent_id": contract[intent_field],
                "policy_version": policy["policy_version"],
                "ceiling_minor": policy["departments"]["TREASURY"],
                "policy_fixture": f"lab/case_study/policies/{filename}.json",
                "intent_record": f"lab/case_study/{contract_path}",
            }
        )
    write_json(
        output / "intention_bundle.json",
        {
            "authority_status": "SYNTHETIC_EXAMPLE_NOT_PRODUCTION_AUTHORIZATION",
            "scope": {
                "currency": "EUR",
                "department": "TREASURY",
                "risk": "LOW",
                "cross_border": False,
                "decision_kind": "fresh",
            },
            "versions": intention_versions,
            "historical_replay_preserved": True,
            "historical_replay_adds_audit_row": False,
        },
    )

    permission = run_demo(CASE, output / "ch03_permission_trace.jsonl")
    permission["trace"] = "ch03_permission_trace.jsonl"
    write_json(output / "ch03_permission_envelope.json", permission)

    fitness = run_fitness(CASE)
    selected = {
        "A_v2_boundary_is_detected_as_defect",
        "B_v2_boundary",
        "replay_preserves_v1_provenance",
        "service_has_no_treasury_literal",
    }
    fitness_excerpt = {
        "source": "lab/companion/ch05/architecture_fitness_v2.py",
        "full_run_passed": fitness["passed"],
        "full_run_total": fitness["total"],
        "checks": [row for row in fitness["checks"] if row["check"] in selected],
    }
    write_json(output / "ch05_fitness_excerpt.json", fitness_excerpt)

    environment = {
        "python": platform.python_version(),
        "implementation": platform.python_implementation(),
        "platform": platform.system(),
        "execution": "local synthetic offline laboratory",
        "dependencies": "Python standard library",
    }
    environment_path = output / "environment_profile.json"
    write_json(environment_path, environment)
    command = [
        sys.executable,
        "lab/companion/ch07/independent_oracle_lab.py",
        "lab/case_study",
    ]
    completed = subprocess.run(
        command, cwd=ROOT, capture_output=True, text=True, timeout=30
    )
    if completed.returncode or completed.stderr:
        raise RuntimeError(
            f"oracle did not complete successfully: {completed.stderr or completed.stdout}"
        )
    oracle = json.loads(completed.stdout)
    paths = {
        "candidate": CASE / "approval_lab/policy.py",
        "intent": CASE / "docs/02_late_intent_delta.json",
        "oracle": ROOT / "lab/companion/ch07/independent_oracle_lab.py",
        "environment": environment_path,
    }
    manifest = make_manifest(
        paths,
        "INT-002",
        command,
        completed.returncode,
        ["real approval authority", "production deployment", "external validity"],
        0,
    )
    for role, path in paths.items():
        manifest["artifacts"][role]["path"] = (
            str(path.relative_to(ROOT)) if path.is_relative_to(ROOT) else path.name
        )
    manifest["command"][0] = "python"
    manifest["clock_basis"] = (
        "Synthetic sequence origin; created_at=0 is not a wall-clock timestamp."
    )
    manifest["result"] = {
        "passed": oracle["passed"],
        "total": oracle["total"],
        "count_kind": oracle["count_kind"],
    }
    manifest["verification"] = verify_manifest(manifest, paths, "INT-002")
    write_json(output / "ch07_evidence_record.json", manifest)

    cards = []
    for version, state in (("v1", "SUPERSEDED"), ("v2", "CURRENT")):
        source = CASE / f"policies/{version}.json"
        policy = json.loads(source.read_text())
        card = {
            "policy_version": policy["policy_version"],
            "department": "TREASURY",
            "ceiling_minor": policy["departments"]["TREASURY"],
            "source_sha256": hashlib.sha256(source.read_bytes()).hexdigest(),
            "source": str(source.relative_to(ROOT)),
            "owner": "illustrative policy steward",
            "state": state,
        }
        checks = {
            purpose: check_threshold_card(card, source, "approval-eur-v2", purpose)
            for purpose in ("new_decision", "historical_explanation")
        }
        cards.append({"card": card, "checks": checks})
    write_json(
        output / "ch09_threshold_cards.json",
        {"active_policy": "approval-eur-v2", "cards": cards},
    )
    assert fitness["passed"] == fitness["total"]
    assert permission["events"] == 4 and permission["denials"] == 2
    assert (
        manifest["verification"]["status"]
        == "READY_FOR_HUMAN_REVIEW_AUTHORITY_UNVERIFIED"
    )
    assert cards[0]["checks"]["new_decision"] == "HOLD_STALE_FOR_NEW"
    assert (
        cards[1]["checks"]["new_decision"] == "CURRENT_SOURCE_MATCH_NOT_AUTHORIZATION"
    )
    return {
        "status": "PASS",
        "artifacts": len(list(output.glob("*.json")))
        + len(list(output.glob("*.jsonl"))),
        "oracle_behavioral_records": oracle["total"],
        "output": str(output),
    }


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, default=ROOT / "audit/reader_artifacts")
    args = parser.parse_args(argv)
    print(json.dumps(generate(args.output.resolve()), indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
