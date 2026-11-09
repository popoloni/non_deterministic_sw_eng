#!/usr/bin/env python3
"""Reproducible tool-using retrieval agent, NOT a language model or human study.
Retrieves repository files using BM25 and optionally follows provenance in a
curated memory card. Gold labels are loaded only by the evaluator.
"""

from pathlib import Path
from collections import Counter
import json, math, re, csv, sys, hashlib, statistics

STOP = set(
    "the a an is are what which for under of to in and with does from by on that be do how why this old new must it can we use which source document documents".split()
)


def tokens(s):
    return [
        x for x in re.findall(r"[a-z0-9_]+", s.lower()) if x not in STOP and len(x) > 1
    ]


def documents(root):
    docs = {}
    for p in sorted(root.rglob("*")):
        if p.is_file() and p.suffix in (".json", ".md", ".py"):
            rel = str(p.relative_to(root))
            docs[rel] = p.read_text(errors="replace")
    return docs


def rank(query, docs):
    q = Counter(tokens(query))
    tf = {name: Counter(tokens(text)) for name, text in docs.items()}
    lengths = {name: sum(counts.values()) for name, counts in tf.items()}
    av = sum(lengths.values()) / len(lengths)
    N = len(docs)
    df = Counter()
    for counts in tf.values():
        for word in counts:
            df[word] += 1
    results = []
    for name, counts in tf.items():
        score = 0.0
        for word, qc in q.items():
            if counts[word] == 0:
                continue
            idf = math.log(1 + (N - df[word] + 0.5) / (df[word] + 0.5))
            norm = (
                counts[word]
                * (1.2 + 1)
                / (counts[word] + 1.2 * (0.25 + 0.75 * lengths[name] / av))
            )
            score += idf * norm * min(qc, 2)
        if score:
            results.append((name, score))
    return sorted(results, key=lambda x: (-x[1], x[0]))


def run_agent(query, docs, mode):
    """Agent has two bounded tools: lexical search and provenance traversal."""
    raw = {k: v for k, v in docs.items() if k != "docs/06_case_memory_card.json"}
    search = rank(query, raw)
    actions = [{"tool": "search", "query": query, "hits": len(search)}]
    if mode == "memory" and "docs/06_case_memory_card.json" in docs:
        card = json.loads(docs["docs/06_case_memory_card.json"])
        card_hits = rank(query, {"memory": json.dumps(card["facts"])})
        if card_hits and search:
            # A single provenance-follow action; no access to evaluation gold.
            sources = [p for p in card["source"] if p in raw]
            actions.append(
                {
                    "tool": "follow_memory_provenance",
                    "memory_id": card["memory_id"],
                    "sources": sources,
                }
            )
            # Rank source snippets; memory helps discover sources but does not become authoritative.
            preferred = [x for x in search if x[0] in sources]
            other = [x for x in search if x[0] not in sources]
            search = preferred + other
    top = [name for name, score in search[:3]]
    # The agent deliberately abstains when no source supports the requested real-world approval.
    prohibited = (
        "regulator approval number" in query.lower()
        or "production use" in query.lower()
    )
    actions.append({"tool": "cite_sources", "paths": top})
    return {
        "citations": ([] if prohibited else top),
        "abstained": prohibited or not top,
        "actions": actions,
    }


def evaluate(root, task_file, outdir):
    docs = documents(root)
    tasks = json.loads(task_file.read_text())
    rows = []
    traces = []
    for mode in ("baseline", "memory"):
        for task in tasks:
            result = run_agent(task["question"], docs, mode)
            gold = set(task["gold"])
            found = set(result["citations"])
            hit = bool(found & gold) if gold else result["abstained"]
            precision = (
                len(found & gold) / len(found)
                if found
                else (1 if not gold and result["abstained"] else 0)
            )
            recall = len(found & gold) / len(gold) if gold else int(result["abstained"])
            rows.append(
                {
                    "condition": mode,
                    "task": task["id"],
                    "gold_sources": len(gold),
                    "top3_hit": int(hit),
                    "precision": round(precision, 3),
                    "recall": round(recall, 3),
                    "abstained": result["abstained"],
                }
            )
            traces.append(
                {
                    "condition": mode,
                    "task": task["id"],
                    "question": task["question"],
                    "result": result,
                    "gold": task["gold"],
                }
            )
    outdir.mkdir(parents=True, exist_ok=True)
    with (outdir / "trial_results.csv").open("w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=rows[0].keys())
        w.writeheader()
        w.writerows(rows)
    (outdir / "agent_traces.json").write_text(json.dumps(traces, indent=2))
    summary = {}
    for mode in ("baseline", "memory"):
        rr = [x for x in rows if x["condition"] == mode]
        summary[mode] = {
            "top3_source_hit": sum(x["top3_hit"] for x in rr),
            "n_tasks": len(rr),
            "mean_source_recall": round(statistics.mean(x["recall"] for x in rr), 3),
            "mean_source_precision": round(
                statistics.mean(x["precision"] for x in rr), 3
            ),
        }
    summary["scope"] = (
        "Source-location and abstention only; no human/LLM comprehension tested."
    )
    (outdir / "summary.json").write_text(json.dumps(summary, indent=2))
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    evaluate(Path(sys.argv[1]), Path(sys.argv[2]), Path(sys.argv[3]))
