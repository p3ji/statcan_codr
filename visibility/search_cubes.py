"""Keyword search over the cached WDS cube list. Usage:

    python visibility/search_cubes.py "wages occupation" "union coverage" ...

Each argument is one search: all terms must appear (case-insensitive) in the
English cube title. Prints PID, current/archived flag, end year, and title.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

CACHE = Path(__file__).parent / "cache" / "cubes_lite.json"


def main() -> None:
    cubes = json.loads(CACHE.read_text(encoding="utf-8"))
    for arg in sys.argv[1:]:
        terms = [t.lower() for t in arg.split()]
        print(f"\n=== {arg} ===")
        hits = []
        for c in cubes:
            title = c["cubeTitleEn"].lower()
            if all(t in title for t in terms):
                hits.append(c)
        # WDS archive codes (verified empirically): "2" = current, "1" = archived/inactive
        hits.sort(key=lambda c: (c["archived"] != "2", c.get("cubeEndDate") or ""))
        for c in hits[:12]:
            flag = "CUR" if c["archived"] == "2" else "ARC"
            end = (c.get("cubeEndDate") or "?")[:4]
            print(f"  {c['productId']} [{flag} end={end}] {c['cubeTitleEn'][:110]}")
        if len(hits) > 12:
            print(f"  ... {len(hits) - 12} more")
        if not hits:
            print("  (no matches)")


if __name__ == "__main__":
    main()
