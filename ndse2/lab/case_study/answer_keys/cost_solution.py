"""Reproduce fictional Chapter 2 and Chapter 12 arithmetic; not field data."""

from __future__ import annotations


def chapter02() -> dict:
    modes = {
        "human": {"attempts": 10, "accepted": 8, "minutes": (420, 110, 70, 80)},
        "ai": {"attempts": 12, "accepted": 9, "minutes": (360, 175, 140, 105)},
    }
    return {
        k: {
            "minutes": sum(v["minutes"]),
            "minutes_per_accepted": sum(v["minutes"]) / v["accepted"],
            "acceptance_rate": v["accepted"] / v["attempts"],
        }
        for k, v in modes.items()
    }


def chapter12() -> dict:
    modes = {
        "human": (170, 40, 20, 0, 0.95),
        "ai_pair": (120, 65, 35, 8, 0.90),
        "bounded_agent": (75, 100, 60, 18, 0.76),
        "ai_pair_less_review": (120, 35, 35, 8, 0.90),
    }
    result = {}
    for k, (develop, review, rework, tools, p) in modes.items():
        per = 1.25 * (develop + rework) + 1.50 * review + tools
        result[k] = {"per_attempt": round(per, 2), "per_accepted": round(per / p, 2)}
    return result


if __name__ == "__main__":
    print("Chapter 02 synthetic measurement:", chapter02())
    print("Chapter 12 synthetic costs:", chapter12())
    assert chapter02()["human"]["minutes"] == 680
    assert chapter02()["ai"]["minutes"] == 780
    assert chapter12()["human"]["per_accepted"] == 313.16
    assert chapter12()["ai_pair_less_review"]["per_accepted"] == 282.50
