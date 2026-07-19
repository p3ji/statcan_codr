"""Cross the goal-1 DDG results with the goal-2 answerability coding.

Prints the headline stats: StatCan visibility rates (top-1/3/10) overall and
by subject / intent / answerability, rank-1 winners, and the answerable x
visible 2x2.
"""
from __future__ import annotations

import csv
from collections import Counter, defaultdict
from pathlib import Path

import yaml

HERE = Path(__file__).parent
DDG = HERE / "results" / "ddg_2026-07-18.csv"


def main() -> None:
    manifest = yaml.safe_load((HERE / "queries.yaml").read_text(encoding="utf-8"))
    meta = {}
    for subj, qs in manifest["subjects"].items():
        for q in qs:
            meta[q["id"]] = {"subject": subj, "intent": q["intent"], "answerable": q["answerable"]}

    per_query: dict[str, list[dict]] = defaultdict(list)
    with DDG.open(encoding="utf-8") as f:
        for row in csv.DictReader(f):
            per_query[row["id"]].append(row)

    stats = {}
    for qid, rows in per_query.items():
        ranks = [int(r["rank"]) for r in rows if r["source_class"] == "statcan"]
        first = min(ranks) if ranks else None
        rank1_class = next((r["source_class"] for r in rows if int(r["rank"]) == 1), "no_results")
        rank1_domain = next((r["domain"] for r in rows if int(r["rank"]) == 1), "")
        stats[qid] = {"first_statcan": first, "rank1_class": rank1_class, "rank1_domain": rank1_domain}

    n = len(stats)
    print(f"queries with results: {n} (of {len(meta)})")

    def vis_line(label: str, ids: list[str]) -> None:
        k = len(ids)
        if not k:
            return
        top1 = sum(1 for i in ids if stats[i]["first_statcan"] == 1)
        top3 = sum(1 for i in ids if stats[i]["first_statcan"] and stats[i]["first_statcan"] <= 3)
        top10 = sum(1 for i in ids if stats[i]["first_statcan"])
        print(f"  {label:<38} n={k:<3} rank1={top1:>2} ({100*top1//k}%)  top3={top3:>2} ({100*top3//k}%)  top10={top10:>2} ({100*top10//k}%)")

    ids_all = list(stats)
    print("\nStatCan visibility (DDG organic):")
    vis_line("ALL", ids_all)
    for dim in ["subject", "intent", "answerable"]:
        print(f" by {dim}:")
        for val in sorted({meta[i][dim] for i in ids_all}):
            vis_line(f"  {val}", [i for i in ids_all if meta[i][dim] == val])

    print("\nWho holds rank 1 (source class):", dict(Counter(s["rank1_class"] for s in stats.values())))
    print("Top rank-1 domains:", Counter(s["rank1_domain"] for s in stats.values()).most_common(12))

    print("\n2x2 (answerable-fully x statcan-in-top3):")
    for full in [True, False]:
        for vis in [True, False]:
            ids = [
                i for i in ids_all
                if (meta[i]["answerable"] == "fully") == full
                and bool(stats[i]["first_statcan"] and stats[i]["first_statcan"] <= 3) == vis
            ]
            print(f"  answerable_fully={full!s:<5} statcan_top3={vis!s:<5} -> {len(ids)}  {sorted(ids)[:8]}{'...' if len(ids) > 8 else ''}")


if __name__ == "__main__":
    main()
