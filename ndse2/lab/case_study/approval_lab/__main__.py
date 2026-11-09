"""Offline CLI for the synthetic, versioned approval-routing case study."""

import argparse
import json
from pathlib import Path
from .domain import Transaction, ValidationError, ConflictError
from .policy import Policy
from .service import ApprovalService
from .legacy import legacy_route

ROOT = Path(__file__).resolve().parents[1]


def main():
    ap = argparse.ArgumentParser(
        description="Synthetic approval-policy lab. NOT for production authorization."
    )
    sub = ap.add_subparsers(dest="cmd", required=True)
    de = sub.add_parser("demo", help="Run synthetic v1/v2 comparison")
    ev = sub.add_parser(
        "evaluate", help="Evaluate one synthetic request; persistent sqlite evidence"
    )
    ev.add_argument("--db", default=":memory:")
    ev.add_argument("--policy", choices=["v1", "v2"], default="v1")
    ev.add_argument("--transaction-id", required=True)
    ev.add_argument("--idempotency-key", required=True)
    ev.add_argument("--amount-minor", type=int, required=True)
    ev.add_argument("--department", required=True)
    ev.add_argument("--risk", choices=["LOW", "HIGH"], default="LOW")
    ev.add_argument("--requester", default="synthetic-tester")
    ev.add_argument("--cross-border", action="store_true")
    ver = sub.add_parser("audit-check", help="Verify local demo audit hash-chain")
    ver.add_argument("--db", required=True)
    leg = sub.add_parser(
        "legacy-demo", help="Illustrate old high-risk bug, no external side effects"
    )
    args = ap.parse_args()
    if args.cmd == "legacy-demo":
        t = Transaction("BUG-001", 100, "EUR", "OPS", "HIGH", "demo-user")
        print(
            json.dumps(
                {
                    "legacy_routing": legacy_route(t),
                    "expected_safe_routing": "REVIEW_REQUIRED",
                    "warning": "LEGACY IS INTENTIONALLY UNSAFE",
                }
            )
        )
        return
    if args.cmd == "demo":
        t = Transaction("TEST-001", 400_000, "EUR", "TREASURY", "LOW", "demo-user")
        out = {}
        for version in ["v1", "v2"]:
            policy = Policy.from_file(ROOT / "policies" / f"{version}.json")
            service = ApprovalService(":memory:", policy)
            out[version] = service.evaluate(t, "demo-" + version).as_payload()
            out[version]["audit_valid"] = service.audit_is_contiguous()
            service.close()
        print(json.dumps(out, indent=2))
        return
    policy = Policy.from_file(ROOT / "policies" / f'{getattr(args,"policy","v1")}.json')
    service = ApprovalService(args.db, policy)
    try:
        if args.cmd == "audit-check":
            print(
                json.dumps(
                    {
                        "integrity_check": service.audit_is_contiguous(),
                        "events": service.stored_decisions(),
                        "warning": "hash chain is not tamper-proof without external signatures",
                    }
                )
            )
            return
        tx = Transaction(
            args.transaction_id,
            args.amount_minor,
            "EUR",
            args.department,
            args.risk,
            args.requester,
            args.cross_border,
        )
        d = service.evaluate(tx, args.idempotency_key)
        print(
            json.dumps(
                {
                    "decision": d.as_payload(),
                    "audit_valid": service.audit_is_contiguous(),
                },
                indent=2,
            )
        )
    except (ValidationError, ConflictError) as exc:
        ap.exit(2, f"policy error: {exc}\n")
    finally:
        service.close()


if __name__ == "__main__":
    main()
