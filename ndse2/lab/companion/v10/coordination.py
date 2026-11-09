"""Sequential synthetic target leases and queue admission, not distributed locks."""

from __future__ import annotations
from dataclasses import dataclass


@dataclass(frozen=True)
class Lease:
    owner: str
    intent: str
    expiry: int
    generation: int


class Coordinator:
    def __init__(self, intent: str = "INT-002", capacity: int = 8):
        if type(capacity) is not int or capacity < 1:
            raise ValueError("positive capacity")
        self.intent = intent
        self.capacity = capacity
        self.leases = {}
        self.pending = {}
        self.events = {}
        self.generation = 0

    def grant(
        self, owner: str, target: str, *, now: int, expiry: int
    ) -> tuple[str, int | None]:
        if (
            not owner
            or not target
            or type(now) is not int
            or type(expiry) is not int
            or expiry <= now
        ):
            raise ValueError("invalid lease")
        old = self.leases.get(target)
        if old and old.expiry > now:
            return "HOLD_TARGET_ALREADY_LEASED", None
        self.generation += 1
        self.leases[target] = Lease(owner, self.intent, expiry, self.generation)
        return "LEASE_GRANTED_NOT_MERGE_AUTHORITY", self.generation

    def submit(
        self,
        event_id: str,
        owner: str,
        target: str,
        intent: str,
        generation: int,
        *,
        now: int,
    ) -> str:
        if not event_id or type(now) is not int or type(generation) is not int:
            raise ValueError("invalid event")
        payload = (owner, target, intent, generation)
        if event_id in self.events:
            return (
                "DUPLICATE_NO_NEW_SUBMISSION"
                if self.events[event_id] == payload
                else "HOLD_EVENT_ID_CONFLICT"
            )
        if intent != self.intent:
            return "HOLD_STALE_INTENT"
        lease = self.leases.get(target)
        if (
            not lease
            or lease.owner != owner
            or lease.generation != generation
            or lease.intent != intent
        ):
            return "HOLD_WRONG_LEASE"
        if now >= lease.expiry:
            return "HOLD_EXPIRED_LEASE"
        if len(self.pending) >= self.capacity:
            return "HOLD_REVIEW_CAPACITY"
        self.events[event_id] = payload
        self.pending[event_id] = payload
        return "ADMITTED_TO_REVIEW_QUEUE_NOT_ACCEPTED"

    def change_intent(self, new_intent: str) -> None:
        if not new_intent:
            raise ValueError("intent required")
        self.intent = new_intent
        # Retain old leases/events for history; submissions must match the current revision.

    def withdraw(self, event_id: str, reason: str) -> None:
        if not reason:
            raise ValueError("reason required")
        self.pending.pop(event_id, None)

    def revoke(self, target: str, reason: str) -> None:
        if not reason:
            raise ValueError("reason required")
        self.leases.pop(target, None)
