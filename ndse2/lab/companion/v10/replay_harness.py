"""Synthetic replay mutation: candidates and oracle have explicit separate roles."""

from __future__ import annotations
from copy import deepcopy


def candidate_replay(mode: str, stored: dict, current_evaluation: dict) -> dict:
    if mode == "reference":
        return deepcopy(stored)
    if mode == "reevaluate_mutant":
        return deepcopy(current_evaluation)
    raise ValueError("unknown candidate")


def circular_self_test(actual: dict, current_evaluation: dict) -> bool:
    """Deliberately wrong oracle, retained only as a negative control."""
    return actual == current_evaluation


def independent_replay_check(actual: dict, stored: dict) -> bool:
    """Authorized replay invariant: original key/payload returns exact stored response."""
    return actual == stored
