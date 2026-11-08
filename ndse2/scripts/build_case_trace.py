"""Recheck the recovered NDSE case without modifying its historical sources.

The current-revision results are a new deterministic recheck, separate from the
seven historical gate results. This script does not create a production queue.
"""

from __future__ import annotations
from pathlib import Path
import contextlib
import dataclasses
import hashlib
import io
import json
import runpy
import sys
import tempfile

ROOT = Path(__file__).resolve().parents[1]
HERE = ROOT / "audit/case_trace"
HERE.mkdir(parents=True, exist_ok=True)
RECOVERED = ROOT
sys.dont_write_bytecode = True


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def governance_trace() -> dict:
    path = RECOVERED / "lab/companion/ch11/multi_agent_governance.py"
    captured = io.StringIO()
    previous_argv = sys.argv[:]
    try:
        sys.argv = [str(path)]
        with contextlib.redirect_stdout(captured):
            module = runpy.run_path(str(path))
    finally:
        sys.argv = previous_argv
    original_report = json.loads(captured.getvalue())
    historical = {r["proposal"]: r for r in original_report["scenarios"]}
    final_revision = module["revision"]
    final_ownership = dict(module["lock"])
    rows = []
    for order, proposal in enumerate(module["proposals"], 1):
        current = module["gate"](proposal, final_revision, final_ownership)
        rows.append(
            {
                "candidate_order": order,
                "event_index": order if order <= 2 else order + 1,
                "proposal": dataclasses.asdict(proposal),
                "active_revision_at_original_check": 1 if order <= 2 else 2,
                "historical_gate_result": historical[proposal.ident],
                "current_revision_recheck": current,
            }
        )
    now_ready = sum(
        r["current_revision_recheck"]["state"] == "READY_FOR_HUMAN_REVIEW" for r in rows
    )
    assert original_report["counts"] == {"ready_for_human_review": 3, "rejected": 4}
    assert now_ready == 2
    assert [
        r["proposal"]["ident"]
        for r in rows
        if r["current_revision_recheck"]["state"] == "READY_FOR_HUMAN_REVIEW"
    ] == ["B2", "E2"]
    assert rows[0]["historical_gate_result"]["state"] == "READY_FOR_HUMAN_REVIEW"
    assert rows[0]["current_revision_recheck"]["reasons"] == ["STALE_INTENT_REVISION"]
    return {
        "kind": "DETERMINISTIC_CASE_TRACE_WITH_EXPLICIT_FINAL_REVISION_RECHECK",
        "source": "lab/companion/ch11/multi_agent_governance.py",
        "source_sha256": digest(path),
        "historical_counts": original_report["counts"],
        "intent_change_event": {
            "event_index": 3,
            "from": "INT-001",
            "to": "INT-002",
            "before_proposal": "B2",
            "effect_in_original": "Set revision to 2 and clear the old file-ownership map.",
        },
        "final_revision": final_revision,
        "final_file_ownership": final_ownership,
        "rows": rows,
        "current_revision_recheck_counts": {
            "ready_for_human_review": now_ready,
            "rejected": len(rows) - now_ready,
        },
        "scope": {
            "en": "The seven historical results are preserved. The second column reruns the same gate for all seven proposals at revision 2 with the original final ownership map. It is a new synthetic recheck, not a queue maintained by the historical script and not an operational authorization.",
            "it": "I sette esiti storici restano conservati. La seconda valutazione richiama lo stesso controllo sulle sette proposte con la revisione 2 e la mappa finale originale delle assegnazioni. È un nuovo ricontrollo sintetico, non una coda mantenuta dallo script storico né un'autorizzazione operativa.",
        },
    }


def routing_trace() -> dict:
    case = RECOVERED / "lab/case_study"
    sys.path.insert(0, str(case))
    from approval_lab.domain import Transaction, ConflictError
    from approval_lab.policy import Policy
    from approval_lab.service import ApprovalService

    v1 = Policy.from_file(case / "policies/v1.json")
    v2 = Policy.from_file(case / "policies/v2.json")

    def tx(
        ident: str,
        amount: int = 400000,
        risk: str = "LOW",
        cross_border: bool = False,
        department: str = "TREASURY",
    ) -> Transaction:
        return Transaction(
            transaction_id=ident,
            amount_minor=amount,
            currency="EUR",
            department=department,
            risk=risk,
            requester="case-reader",
            cross_border=cross_border,
        )

    decisions = []
    inputs = [
        ("treasury_3000", 300000, "LOW", False, "TREASURY"),
        ("treasury_4000", 400000, "LOW", False, "TREASURY"),
        ("treasury_5000", 500000, "LOW", False, "TREASURY"),
        ("treasury_3000_plus_cent", 300001, "LOW", False, "TREASURY"),
        ("high_risk", 10000, "HIGH", False, "TREASURY"),
        ("cross_border", 10000, "LOW", True, "TREASURY"),
        ("unknown_department", 10000, "LOW", False, "UNKNOWN"),
        ("ops_10000", 1000000, "LOW", False, "OPS"),
    ]
    for name, amount, risk, cross_border, department in inputs:
        transaction = tx(name, amount, risk, cross_border, department)
        decisions.append(
            {
                "scenario": name,
                "transaction": dataclasses.asdict(transaction),
                "v1": dataclasses.asdict(v1.evaluate(transaction)),
                "v2": dataclasses.asdict(v2.evaluate(transaction)),
            }
        )
    temporary_root = HERE / "verification" / "tmp"
    temporary_root.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(dir=temporary_root) as directory:
        db = Path(directory) / "synthetic.sqlite"
        before = ApprovalService(db, v1)
        original = before.evaluate(tx("T-HISTORY"), "idem-history")
        before.close()
        after = ApprovalService(db, v2)
        replay = after.evaluate(tx("T-HISTORY"), "idem-history")
        fresh = after.evaluate(tx("T-NEW"), "idem-new")
        conflicts = {}
        for name, transaction, key in [
            ("same_key_changed_payload", tx("T-HISTORY", 300000), "idem-history"),
            ("same_transaction_new_key", tx("T-HISTORY"), "different-key"),
        ]:
            try:
                after.evaluate(transaction, key)
            except ConflictError:
                conflicts[name] = "ConflictError"
            else:
                raise AssertionError(name + " did not conflict")
        preserved = after.evaluate(tx("T-HISTORY"), "idem-history")
        audit_events = after.db.execute("SELECT COUNT(*) FROM audit").fetchone()[0]
        audit_valid = after.audit_is_contiguous()
        after.close()
    assert original == replay == preserved
    assert original.policy_version == "approval-eur-v1"
    assert original.status == "AUTO_APPROVAL_ELIGIBLE"
    assert (
        fresh.policy_version == "approval-eur-v2" and fresh.status == "REVIEW_REQUIRED"
    )
    assert audit_events == 2 and audit_valid
    return {
        "kind": "CURRENT_SYNTHETIC_ROUTING_AND_REPLAY_TRACE",
        "currency": "EUR",
        "minor_unit": "cent",
        "decisions": decisions,
        "replay": {
            "historical_id": "T-HISTORY",
            "historical_key": "idem-history",
            "original": dataclasses.asdict(original),
            "repeated_after_v2": dataclasses.asdict(replay),
            "new_id": "T-NEW",
            "new_key": "idem-new",
            "new_decision": dataclasses.asdict(fresh),
            "conflicts": conflicts,
            "historical_record_unchanged_after_conflicts": original == preserved,
            "audit_event_count": audit_events,
            "audit_is_contiguous": audit_valid,
        },
        "scope": "Local synthetic decisions only; no funds movement, authenticated policy approval or production transaction.",
    }


if __name__ == "__main__":
    (HERE / "CH11_CASE_TIMELINE.json").write_text(
        json.dumps(governance_trace(), ensure_ascii=False, indent=2) + "\n"
    )
    (HERE / "CANONICAL_CASE_TRACE.json").write_text(
        json.dumps(routing_trace(), ensure_ascii=False, indent=2) + "\n"
    )
    print(
        "Historical decisions 3 ready / 4 rejected; final-revision recheck 2 ready / 5 rejected. Canonical replay and conflict checks passed."
    )
