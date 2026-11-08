"""Score locked, blinded ratings after private-key collation; no causal estimator."""

from __future__ import annotations
import argparse, csv, json, statistics
from pathlib import Path
from collections import defaultdict

D = ("authority", "behavior", "causal", "negative_test", "change_impact")
TIMEPOINTS = {"baseline", "immediate", "day14"}


def kappa_quadratic(a: list[int], b: list[int]) -> float | None:
    n = len(a)
    if n < 2:
        return None
    obs = sum((x - y) ** 2 / 4 for x, y in zip(a, b)) / n
    pa = [a.count(k) / n for k in range(3)]
    pb = [b.count(k) / n for k in range(3)]
    exp = sum(((i - j) ** 2 / 4) * pa[i] * pb[j] for i in range(3) for j in range(3))
    return None if exp == 0 else round(1 - obs / exp, 4)


def analyze(rows: list[dict], keys: list[dict]) -> dict:
    if not rows:
        raise ValueError("NO_REAL_RATINGS: empty dataset; no psychometric result")
    keymap = {}
    sessions = set()
    for k in keys:
        aid = k.get("answer_id", "").strip()
        pid = k.get("participant_id", "").strip()
        form = k.get("form")
        tp = k.get("timepoint")
        if not aid or not pid or form not in {"A", "B"} or tp not in TIMEPOINTS:
            raise ValueError("Invalid private answer key")
        if aid in keymap or (pid, tp) in sessions:
            raise ValueError("Duplicate answer or participant/session in private key")
        keymap[aid] = k
        sessions.add((pid, tp))
    by = defaultdict(dict)
    for r in rows:
        aid = r.get("answer_id", "").strip()
        rid = r.get("rater_id", "").strip()
        if aid not in keymap or not rid:
            raise ValueError("Missing answer key or rater ID")
        if any(str(r.get(d)) not in {"0", "1", "2"} for d in D):
            raise ValueError("Invalid rubric score; require 0,1,2")
        if r.get("unsafe_assumption") not in {"yes", "no"}:
            raise ValueError("Unsafe flag must be yes/no")
        if not r.get("evidence_excerpt", "").strip():
            raise ValueError("Each rating requires supporting evidence")
        if rid in by[aid]:
            raise ValueError("Duplicate rater on same answer")
        by[aid][rid] = r
    if set(keymap) != set(by):
        raise ValueError("Private key and rated answers do not match")
    if any(len(v) != 2 for v in by.values()):
        raise ValueError("Exactly two locked independent ratings per answer required")
    pairs = {tuple(sorted(v)) for v in by.values()}
    if len(pairs) != 1:
        raise ValueError(
            "This simple Cohen-kappa scorer requires the same two raters throughout"
        )
    kappas = {}
    agreement = {}
    for dim in D:
        a = []
        b = []
        for rs in by.values():
            x, y = [rs[r] for r in sorted(rs)]
            a.append(int(x[dim]))
            b.append(int(y[dim]))
        kappas[dim] = kappa_quadratic(a, b)
        agreement[dim] = sum(x == y for x, y in zip(a, b)) / len(a)
    bytime = defaultdict(list)
    for aid, rs in by.items():
        bytime[keymap[aid]["timepoint"]].append(
            sum(sum(int(r[d]) for d in D) for r in rs.values()) / 2
        )
    return dict(
        n_answers=len(by),
        n_participants=len({k["participant_id"] for k in keys}),
        weighted_kappa_by_dimension=kappas,
        exact_agreement_by_dimension=agreement,
        mean_total_score_by_timepoint={
            k: round(statistics.mean(v), 3) for k, v in sorted(bytime.items())
        },
        unsafe_flag_disagreements=sum(
            len({r["unsafe_assumption"] for r in rs.values()}) > 1 for rs in by.values()
        ),
        note="Descriptive scores and rater agreement only. Undefined kappa is null. Repeated answers are not independent participants; no causal effect or validated competence threshold is estimated.",
    )


def main() -> None:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("ratings", type=Path)
    p.add_argument("--key", required=True, type=Path)
    a = p.parse_args()
    try:
        with a.ratings.open(newline="", encoding="utf-8-sig") as f:
            rows = list(csv.DictReader(f))
        with a.key.open(newline="", encoding="utf-8-sig") as f:
            keys = list(csv.DictReader(f))
        print(json.dumps(analyze(rows, keys), indent=2))
    except (ValueError, OSError) as e:
        p.error(str(e))


if __name__ == "__main__":
    main()
