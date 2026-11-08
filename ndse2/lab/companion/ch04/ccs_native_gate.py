"""Check the teaching intent structure, separately from authority and acceptance."""

import argparse
import json
from pathlib import Path


def case_directory(value):
    path = Path(value).resolve()
    for relative in ("docs/01_intent_contract.json", "docs/02_late_intent_delta.json"):
        if not (path / relative).is_file():
            raise argparse.ArgumentTypeError(f"case_root is missing {relative}")
    return path


def check_intent(root):
    intent = json.loads((root / "docs/01_intent_contract.json").read_text())
    delta = json.loads((root / "docs/02_late_intent_delta.json").read_text())
    checks = {
        "I1_intent_identity": intent.get("intent_id") == "INT-001"
        and intent.get("revision") == 1,
        "I1_authority_field": bool(intent.get("authority", {}).get("role")),
        "I1_observable_criteria": len(intent.get("acceptance", [])) >= 6,
        "I1_negative_requirements": len(intent.get("invariants", [])) >= 4,
        "I2_linked_delta": delta.get("base_intent") == intent.get("intent_id"),
        "I2_exact_change": delta.get("changed_rule", {}).get("old_ceiling_minor")
        == 500000
        and delta.get("changed_rule", {}).get("new_ceiling_minor") == 300000,
        "D0_architecture_record": (root / "docs/03_architecture_decisions.md").exists(),
        "V0_independent_test_files": all(
            (root / "tests" / p).exists()
            for p in ("test_domain_policy.py", "test_service.py")
        ),
    }
    return {
        "profile": "ccs-native/1.0",
        "checks": checks,
        "structural_status": "PASS" if all(checks.values()) else "FAIL",
        "authority_status": "HUMAN_APPROVAL_UNVERIFIED",
        "acceptance_status": "NOT_ACCEPTED",
    }


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("case_root", type=case_directory)
    args = parser.parse_args(argv)
    result = check_intent(args.case_root)
    print(json.dumps(result, indent=2))
    return 0 if all(result["checks"].values()) else 1


if __name__ == "__main__":
    raise SystemExit(main())
