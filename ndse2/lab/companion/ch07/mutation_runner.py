"""Run named case-study faults against the unchanged Chapter 7 behavioral oracle.

Each fault changes one selected syntax location in an isolated copy. Reports retain
the exact diff and source digests. A failed baseline, bad patch, timeout, import
error or malformed report is an infrastructure error, never a killed mutant.
"""

import argparse
import ast
import difflib
import hashlib
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile

from independent_oracle_lab import case_directory

FAULTS = [
    ("M01_ceiling_ge", "approval_lab/policy.py", "Make the ceiling exclusive."),
    ("M02_high_risk_removed", "approval_lab/policy.py", "Remove the high-risk rule."),
    (
        "M03_cross_border_removed",
        "approval_lab/policy.py",
        "Remove the cross-border rule.",
    ),
    (
        "M04_unknown_department_eligible",
        "approval_lab/policy.py",
        "Make an unknown department auto-eligible.",
    ),
    (
        "M05_replay_uses_active_policy",
        "approval_lab/service.py",
        "Re-evaluate historical replay under the active policy.",
    ),
    (
        "M06_changed_payload_accepted",
        "approval_lab/service.py",
        "Accept a changed payload under the same key.",
    ),
    (
        "M07_existing_transaction_new_key_accepted",
        "approval_lab/service.py",
        "Accept an existing transaction ID under a new key.",
    ),
    (
        "M08_v2_stale_threshold",
        "policies/v2.json",
        "Retain the old Treasury threshold in v2.",
    ),
    ("M09_v2_one_cent_low", "policies/v2.json", "Lower the v2 threshold by one cent."),
    (
        "M10_audit_always_true",
        "approval_lab/service.py",
        "Make the audit checker always succeed.",
    ),
    (
        "M11_replay_duplicates_invalid_chain_row",
        "approval_lab/service.py",
        "Replay copies an audit row without continuing the chain.",
    ),
    (
        "M12_replay_appends_valid_chain_row",
        "approval_lab/service.py",
        "Replay appends an extra event with a valid continued chain.",
    ),
]


def file_digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def tree_hashes(root):
    return {
        str(path.relative_to(root)): file_digest(path)
        for path in sorted(root.rglob("*"))
        if path.is_file() and "__pycache__" not in path.parts and path.suffix != ".pyc"
    }


def exactly_one(nodes, predicate):
    found = [node for node in nodes if predicate(node)]
    if len(found) != 1:
        raise ValueError(f"mutation requires one syntax match; found {len(found)}")
    return found[0]


def replace_node(source, node, replacement):
    lines = source.splitlines(keepends=True)
    start = sum(len(line) for line in lines[: node.lineno - 1]) + node.col_offset
    end = sum(len(line) for line in lines[: node.end_lineno - 1]) + node.end_col_offset
    # The selected Python locations are ASCII, so AST byte columns equal columns here.
    before = source[start:end]
    indented = replacement.replace("\n", "\n" + " " * node.col_offset)
    return source[:start] + indented + source[end:], before, indented


def apply_fault(case_root, fault):
    name, relative, description = fault
    path = case_root / relative
    source = path.read_text(encoding="utf-8")
    if path.suffix == ".json":
        policy = json.loads(source)
        if policy["departments"]["TREASURY"] != 300000:
            raise ValueError("mutation requires the published v2 Treasury threshold")
        before = "300000"
        after = "500000" if name.startswith("M08") else "299999"
        if source.count(before) != 1:
            raise ValueError("mutation requires one threshold literal")
        changed = source.replace(before, after, 1)
        json.loads(changed)
    else:
        tree = ast.parse(source)
        nodes = list(ast.walk(tree))
        normalized = lambda node: ast.unparse(node)
        if name.startswith("M01"):
            node = exactly_one(
                nodes,
                lambda n: isinstance(n, ast.Compare)
                and normalized(n) == "tx.amount_minor > max_amount",
            )
            replacement = "tx.amount_minor >= max_amount"
        elif name.startswith("M02"):
            node = exactly_one(
                nodes,
                lambda n: isinstance(n, ast.If)
                and normalized(n.test) == "tx.risk == 'HIGH'",
            ).test
            replacement = "False and (" + normalized(node) + ")"
        elif name.startswith("M03"):
            node = exactly_one(
                nodes,
                lambda n: isinstance(n, ast.If)
                and normalized(n.test) == "tx.cross_border",
            ).test
            replacement = "False and tx.cross_border"
        elif name.startswith("M04"):
            call = exactly_one(
                nodes,
                lambda n: isinstance(n, ast.Call)
                and isinstance(n.func, ast.Name)
                and n.func.id == "Decision"
                and any(
                    isinstance(a, ast.Constant) and a.value == "UNRECOGNIZED_DEPARTMENT"
                    for a in n.args
                ),
            )
            node = call.args[1]
            replacement = '"AUTO_APPROVAL_ELIGIBLE"'
        elif name.startswith("M06"):
            node = exactly_one(
                nodes,
                lambda n: isinstance(n, ast.If)
                and normalized(n.test) == "old[0] != payload_hash",
            ).test
            replacement = "False"
        elif name.startswith("M07"):
            node = exactly_one(
                nodes,
                lambda n: isinstance(n, ast.Raise)
                and "transaction_id was already evaluated with a different idempotency key"
                in normalized(n),
            )
            replacement = 'self.db.execute("COMMIT")\nreturn self.policy.evaluate(tx)'
        elif name.startswith("M10"):
            method = exactly_one(
                nodes,
                lambda n: isinstance(n, ast.FunctionDef)
                and n.name == "audit_is_contiguous",
            )
            node = method.body[0]
            replacement = "return True"
        else:
            node = exactly_one(
                nodes,
                lambda n: isinstance(n, ast.Return)
                and normalized(n) == "return Decision(**json.loads(old[1]))",
            )
            if name.startswith("M05"):
                replacement = "return self.policy.evaluate(tx)"
            elif name.startswith("M11"):
                replacement = 'self.db.execute("INSERT INTO audit(event_json,prev_hash,entry_hash) SELECT event_json,prev_hash,entry_hash FROM audit ORDER BY sequence DESC LIMIT 1")\nreturn Decision(**json.loads(old[1]))'
            elif name.startswith("M12"):
                replacement = 'entry = self.db.execute("SELECT event_json,entry_hash FROM audit ORDER BY sequence DESC LIMIT 1").fetchone()\nself.db.execute("INSERT INTO audit(event_json,prev_hash,entry_hash) VALUES(?,?,?)", (entry[0], entry[1], sha(entry[1] + "|" + entry[0])))\nreturn Decision(**json.loads(old[1]))'
            else:
                raise ValueError("unknown mutation")
        changed, before, after = replace_node(source, node, replacement)
        ast.parse(changed)
    path.write_text(changed, encoding="utf-8")
    return {
        "id": name,
        "description": description,
        "mutated_file": relative,
        "before": before,
        "after": after,
        "exact_patch": "".join(
            difflib.unified_diff(
                source.splitlines(True),
                changed.splitlines(True),
                fromfile="a/" + relative,
                tofile="b/" + relative,
            )
        ),
        "source_sha256": hashlib.sha256(source.encode()).hexdigest(),
        "mutated_sha256": file_digest(path),
        "syntactically_valid": True,
    }


def interpret_result(returncode, stdout, stderr):
    try:
        report = json.loads(stdout)
        records = report["tests"]
        valid = (
            report["execution_status"] == "COMPLETE"
            and report["count_kind"] == "behavioral_records"
            and isinstance(records, list)
            and len(records) > 0
            and all(
                type(row["pass"]) is bool and row["kind"] == "behavioral"
                for row in records
            )
            and report["total"] == len(records)
            and report["passed"] == sum(row["pass"] for row in records)
        )
        failed = [row["name"] for row in records if not row["pass"]]
        consistent = returncode == (1 if failed else 0)
    except (ValueError, TypeError, KeyError):
        valid, consistent, failed, report = False, False, [], None
    if not valid or not consistent or stderr:
        return {
            "outcome": "INFRASTRUCTURE_ERROR",
            "returncode": returncode,
            "failed_behavioral_records": [],
            "stderr": stderr,
            "stdout": stdout,
        }
    return {
        "outcome": "BEHAVIORAL_FAILURE" if failed else "PASS",
        "returncode": returncode,
        "failed_behavioral_records": failed,
        "behavioral_passed": report["passed"],
        "behavioral_total": report["total"],
    }


def run_oracle(oracle, case_root):
    env = dict(
        os.environ,
        PYTHONDONTWRITEBYTECODE="1",
        PYTHONNOUSERSITE="1",
        PYTHONHASHSEED="0",
    )
    try:
        completed = subprocess.run(
            [sys.executable, str(oracle), str(case_root)],
            cwd=case_root,
            env=env,
            capture_output=True,
            text=True,
            timeout=30,
        )
    except subprocess.TimeoutExpired:
        return {"outcome": "INFRASTRUCTURE_ERROR", "reason": "oracle timeout"}
    return interpret_result(completed.returncode, completed.stdout, completed.stderr)


def campaign(case_root, selected=None):
    oracle = Path(__file__).with_name("independent_oracle_lab.py").resolve()
    original = tree_hashes(case_root)
    baseline = run_oracle(oracle, case_root)
    report = {
        "schema_version": 1,
        "scope": "Sensitivity to the named synthetic faults, not exhaustive correctness",
        "oracle_sha256": file_digest(oracle),
        "case_source_hashes": original,
        "baseline": baseline,
        "mutants": [],
    }
    if baseline["outcome"] != "PASS":
        report.update(status="INFRASTRUCTURE_ERROR", reason="baseline did not pass")
        return report
    with tempfile.TemporaryDirectory(prefix="ndse-mutations-") as temporary:
        for fault in FAULTS:
            if selected and fault[0] not in selected:
                continue
            target = Path(temporary) / fault[0]
            shutil.copytree(
                case_root,
                target,
                ignore=shutil.ignore_patterns("__pycache__", "*.pyc", ".venv"),
            )
            try:
                detail = apply_fault(target, fault)
                result = run_oracle(oracle, target)
                outcome = {
                    "PASS": "SURVIVED",
                    "BEHAVIORAL_FAILURE": "KILLED",
                    "INFRASTRUCTURE_ERROR": "INFRASTRUCTURE_ERROR",
                }[result["outcome"]]
                report["mutants"].append(
                    {**detail, "outcome": outcome, "oracle_result": result}
                )
            except Exception as error:
                report["mutants"].append(
                    {
                        "id": fault[0],
                        "outcome": "INFRASTRUCTURE_ERROR",
                        "error": f"{type(error).__name__}: {error}",
                    }
                )
    report["source_unchanged"] = original == tree_hashes(case_root)
    report["summary"] = {
        "mutants": len(report["mutants"]),
        **{
            name.lower(): sum(m["outcome"] == name for m in report["mutants"])
            for name in ("KILLED", "SURVIVED", "INFRASTRUCTURE_ERROR")
        },
    }
    report["status"] = (
        "PASS"
        if report["source_unchanged"]
        and all(m["outcome"] == "KILLED" for m in report["mutants"])
        else "FAIL"
    )
    return report


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("case_root", type=case_directory)
    parser.add_argument(
        "--mutant",
        action="append",
        choices=[fault[0] for fault in FAULTS],
        help="run one named fault; repeat for a subset",
    )
    args = parser.parse_args(argv)
    report = campaign(args.case_root, args.mutant)
    print(json.dumps(report, indent=2))
    return 0 if report["status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
