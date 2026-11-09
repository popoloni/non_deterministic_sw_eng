"""Local, synthetic decision evidence store with SQLite transactional idempotency.

The audit hash chain detects unsophisticated accidental modification but is NOT a
secure immutable audit log: no digital signature, external anchor, or key custody.
"""

import sqlite3
import hashlib
import json
from pathlib import Path
from .domain import Transaction, Decision, ConflictError, ValidationError
from .policy import Policy


def canonical(obj: dict) -> str:
    return json.dumps(obj, sort_keys=True, separators=(",", ":"), ensure_ascii=False)


def sha(s: str) -> str:
    return hashlib.sha256(s.encode("utf-8")).hexdigest()


class ApprovalService:
    def __init__(self, db_path: str | Path, policy: Policy):
        self.policy = policy
        self.db = sqlite3.connect(str(db_path), timeout=10, isolation_level=None)
        self.db.execute("PRAGMA busy_timeout=10000")
        self.db.execute("""CREATE TABLE IF NOT EXISTS decisions(
            idempotency_key TEXT PRIMARY KEY,
            transaction_id TEXT NOT NULL UNIQUE,
            payload_hash TEXT NOT NULL,
            payload_json TEXT NOT NULL,
            response_json TEXT NOT NULL,
            policy_version TEXT NOT NULL)""")
        self.db.execute("""CREATE TABLE IF NOT EXISTS audit(
            sequence INTEGER PRIMARY KEY AUTOINCREMENT,
            event_json TEXT NOT NULL,
            prev_hash TEXT NOT NULL,
            entry_hash TEXT NOT NULL)""")

    def close(self):
        self.db.close()

    def evaluate(self, tx: Transaction, idempotency_key: str) -> Decision:
        if (
            not isinstance(idempotency_key, str)
            or not 1 <= len(idempotency_key) <= 64
            or any(c.isspace() for c in idempotency_key)
        ):
            raise ValidationError("invalid idempotency key")
        payload = canonical(tx.as_payload())
        payload_hash = sha(payload)
        self.db.execute("BEGIN IMMEDIATE")
        try:
            old = self.db.execute(
                "SELECT payload_hash,response_json FROM decisions WHERE idempotency_key=?",
                (idempotency_key,),
            ).fetchone()
            if old:
                if old[0] != payload_hash:
                    raise ConflictError(
                        "idempotency key reused with different transaction payload"
                    )
                self.db.execute("COMMIT")
                return Decision(**json.loads(old[1]))
            prior = self.db.execute(
                "SELECT idempotency_key FROM decisions WHERE transaction_id=?",
                (tx.transaction_id,),
            ).fetchone()
            if prior:
                raise ConflictError(
                    "transaction_id was already evaluated with a different idempotency key"
                )
            decision = self.policy.evaluate(tx)
            output = canonical(decision.as_payload())
            self.db.execute(
                """INSERT INTO decisions(idempotency_key,transaction_id,payload_hash,payload_json,response_json,policy_version)
                            VALUES(?,?,?,?,?,?)""",
                (
                    idempotency_key,
                    tx.transaction_id,
                    payload_hash,
                    payload,
                    output,
                    self.policy.version,
                ),
            )
            event = canonical(
                {
                    "transaction_id": tx.transaction_id,
                    "decision": decision.as_payload(),
                    "idempotency_key": idempotency_key,
                    "request_sha256": payload_hash,
                }
            )
            row = self.db.execute(
                "SELECT entry_hash FROM audit ORDER BY sequence DESC LIMIT 1"
            ).fetchone()
            prev = row[0] if row else "GENESIS"
            self.db.execute(
                "INSERT INTO audit(event_json,prev_hash,entry_hash) VALUES(?,?,?)",
                (event, prev, sha(prev + "|" + event)),
            )
            self.db.execute("COMMIT")
            return decision
        except Exception:
            self.db.execute("ROLLBACK")
            raise

    def audit_is_contiguous(self) -> bool:
        rows = self.db.execute(
            "SELECT sequence,event_json,prev_hash,entry_hash FROM audit ORDER BY sequence"
        ).fetchall()
        prev = "GENESIS"
        for _seq, event, p, h in rows:
            if p != prev or h != sha(prev + "|" + event):
                return False
            prev = h
        return True

    def stored_decisions(self) -> int:
        return self.db.execute("SELECT COUNT(*) FROM decisions").fetchone()[0]
