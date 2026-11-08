"""Offline control-plane demonstration. No provider, credentials or release API.

Inputs named current_* and now must come from a trusted controller in a real system.
JSON persistence here is not authenticated or an OS sandbox.
"""

from dataclasses import asdict, dataclass, replace
from pathlib import Path
import json


def nonnegative_int(value: int, name: str) -> None:
    if type(value) is not int or value < 0:
        raise ValueError(f"{name} must be a nonnegative integer")


@dataclass(frozen=True)
class LoopState:
    intent: str = "INT-002"
    contract_digest: str = "synthetic-contract-v2"
    used_minor: int = 0
    cap_minor: int = 200
    calls_used: int = 0
    max_calls: int = 4
    attempts_used: int = 0
    max_attempts: int = 2
    deadline: int = 900
    revoked: bool = False
    last_signature: str = ""
    repeated_signature: int = 0

    def validate(self) -> None:
        for name in (
            "used_minor",
            "cap_minor",
            "calls_used",
            "max_calls",
            "attempts_used",
            "max_attempts",
            "deadline",
            "repeated_signature",
        ):
            nonnegative_int(getattr(self, name), name)
        if (
            not self.intent
            or not self.contract_digest
            or type(self.revoked) is not bool
        ):
            raise ValueError("invalid identity or revocation flag")

    def save(self, path: Path) -> None:
        self.validate()
        path.write_text(json.dumps(asdict(self), sort_keys=True))

    @classmethod
    def load(cls, path: Path) -> "LoopState":
        obj = cls(**json.loads(path.read_text()))
        obj.validate()
        return obj


def admit(
    state: LoopState,
    *,
    current_intent: str,
    current_contract_digest: str,
    now: int,
    next_upper_bound_minor: int | None,
    new_candidate: bool = False,
) -> tuple[str, LoopState]:
    state.validate()
    nonnegative_int(now, "now")
    if type(new_candidate) is not bool:
        raise ValueError("new_candidate must be bool")
    if state.revoked:
        return "STOP_REVOKED", state
    if (state.intent, state.contract_digest) != (
        current_intent,
        current_contract_digest,
    ):
        return "STOP_STALE_INTENT", state
    if now >= state.deadline:
        return "STOP_DEADLINE", state
    if state.repeated_signature >= 2:
        return "ESCALATE_REPEATED_DIAGNOSTIC", state
    if next_upper_bound_minor is None:
        return "STOP_UNBOUNDED_COST", state
    nonnegative_int(next_upper_bound_minor, "next_upper_bound_minor")
    if (
        state.calls_used >= state.max_calls
        or state.used_minor + next_upper_bound_minor > state.cap_minor
    ):
        return "STOP_BUDGET", state
    if new_candidate and state.attempts_used >= state.max_attempts:
        return "STOP_ATTEMPTS", state
    return "ACTION_ADMITTED_NOT_ACCEPTED", replace(
        state,
        used_minor=state.used_minor + next_upper_bound_minor,
        calls_used=state.calls_used + 1,
        attempts_used=state.attempts_used + int(new_candidate),
    )


def record_diagnostic(state: LoopState, signature: str) -> LoopState:
    if not signature:
        raise ValueError("a diagnostic signature must name the failure")
    return replace(
        state,
        last_signature=signature,
        repeated_signature=(
            state.repeated_signature + 1 if state.last_signature == signature else 1
        ),
    )
