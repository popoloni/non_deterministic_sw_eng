"""Small trusted-process file broker. NOT an OS sandbox or authentication service.
Test principals and clock are supplied by the harness. No shell/network execution.
Path checks cover this single-process demonstration, not concurrent filesystem attacks.
"""

from __future__ import annotations
from pathlib import Path
from typing import Any


class FileBroker:
    def __init__(self, root: Path, deadline: int = 900):
        self.root = root.resolve()
        self.deadline = deadline
        self.revoked = False
        self.events: list[dict[str, Any]] = []

    def invoke(
        self,
        principal: str,
        action: str,
        target: str = "",
        content: str = "",
        *,
        now: int,
        context: str = "",
    ) -> dict[str, Any]:
        # context is untrusted data. It never enters the authorization predicate.
        reason = None
        if self.revoked:
            reason = "REVOKED"
        elif type(now) is not int or now < 0 or now >= self.deadline:
            reason = "LEASE_EXPIRED_OR_INVALID"
        elif principal not in {"demo-maker", "demo-verifier"}:
            reason = "UNKNOWN_PRINCIPAL"
        elif action not in {"read_data", "write_candidate"}:
            reason = "OPERATION_FORBIDDEN"
        elif action == "write_candidate" and (
            principal != "demo-maker" or target != "candidate/policy_patch.txt"
        ):
            reason = "WRITE_SCOPE"
        elif action == "read_data":
            allowed = (
                {"data/repository.txt"}
                if principal == "demo-maker"
                else {
                    "candidate/policy_patch.txt",
                    "oracle/expected.json",
                    "authority/intent.json",
                }
            )
            if target not in allowed:
                reason = "READ_SCOPE"
        p = self.root / target
        if reason is None:
            parts = Path(target).parts
            if Path(target).is_absolute() or ".." in parts:
                reason = "PATH_SCOPE"
            elif any(
                (self.root.joinpath(*parts[:n])).is_symlink()
                for n in range(1, len(parts) + 1)
            ):
                reason = "SYMLINK_FORBIDDEN"
            elif not p.resolve().is_relative_to(self.root):
                reason = "PATH_SCOPE"
        result = {
            "status": "DENIED" if reason else "OPERATION_ADMITTED_NOT_ACCEPTED",
            "reason": reason or "TASK_ALLOWLIST",
        }
        self.events.append(
            {
                "principal": principal,
                "action": action,
                "target": target,
                "at": now,
                **result,
            }
        )
        if reason:
            return result
        if action == "write_candidate":
            p.parent.mkdir(parents=True, exist_ok=True)
            p.write_text(content, encoding="utf-8")
        else:
            result["data"] = p.read_text(encoding="utf-8")
        return result
