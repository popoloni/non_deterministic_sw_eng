"""Prepare private allocations; no participants or outcomes are generated.

Input: participant_id and optional predeclared stratum. Keep seed, assignments
and linkage private. Fixed A -> B order preserves the unpracticed transfer form.
"""

from __future__ import annotations
import argparse, csv, hashlib, json, random
from pathlib import Path


def allocate(rows: list[dict[str, str]], seed: int) -> tuple[list[dict], list[dict]]:
    ids = [r.get("participant_id", "").strip() for r in rows]
    if not ids or any(not x for x in ids) or len(set(ids)) != len(ids):
        raise ValueError("Require unique nonempty participant IDs")
    groups: dict[str, list[str]] = {}
    for r, pid in zip(rows, ids):
        groups.setdefault(r.get("stratum", "all").strip() or "all", []).append(pid)
    rng = random.Random(seed)
    assignments = []
    for group, members in sorted(groups.items()):
        members = sorted(members)
        rng.shuffle(members)
        arms = ["expert_curated", "unrestricted_ai"] * (len(members) // 2)
        if len(members) % 2:
            arms.append(rng.choice(["expert_curated", "unrestricted_ai"]))
        rng.shuffle(arms)
        for pid, arm in zip(members, arms):
            assignments.append(
                dict(
                    participant_id=pid,
                    stratum=group,
                    condition=arm,
                    baseline_form="A",
                    delayed_form="B",
                )
            )
    # Blind codes do not reveal row parity/condition; this is linkage, not the
    # answer-packet key. One fresh answer_id per response must be assigned privately.
    codes = [f"B-{rng.getrandbits(96):024x}" for _ in ids]
    if len(set(codes)) != len(codes):
        raise RuntimeError("Code collision; choose another private seed")
    links = [
        dict(participant_id=pid, blind_code=code)
        for pid, code in zip(sorted(ids), codes)
    ]
    return sorted(assignments, key=lambda r: r["participant_id"]), links


def write(path: Path, rows: list[dict]) -> None:
    with path.open("x", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0]))
        w.writeheader()
        w.writerows(rows)


def main() -> None:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("participants", type=Path)
    p.add_argument("seed", type=int)
    p.add_argument("assignments", type=Path)
    p.add_argument("linkage", type=Path)
    a = p.parse_args()
    if (
        len({a.participants.resolve(), a.assignments.resolve(), a.linkage.resolve()})
        != 3
    ):
        p.error("Input and output paths must be distinct")
    if a.assignments.exists() or a.linkage.exists():
        p.error("Refusing to overwrite allocation/linkage")
    try:
        with a.participants.open(newline="", encoding="utf-8-sig") as f:
            rows = list(csv.DictReader(f))
        assignments, links = allocate(rows, a.seed)
        write(a.assignments, assignments)
        write(a.linkage, links)
    except (ValueError, OSError) as e:
        p.error(str(e))
    print(
        json.dumps(
            {
                "status": "ALLOCATION_PREPARED_NOT_A_STUDY_RESULT",
                "participants": len(rows),
                "input_sha256": hashlib.sha256(a.participants.read_bytes()).hexdigest(),
                "note": "Private seed/allocations/linkage must not enter rater packets. No scores or effect estimates.",
            },
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
