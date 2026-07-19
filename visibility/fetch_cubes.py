"""Download the StatCan WDS cube list (lite) to visibility/cache/ for offline matching.

Same raw-WDS approach as pipeline/extract.py — the mcp-statcan bulk tools are broken.
"""
from __future__ import annotations

import json
from pathlib import Path

import requests

CACHE_DIR = Path(__file__).parent / "cache"
URL = "https://www150.statcan.gc.ca/t1/wds/rest/getAllCubesListLite"


def main() -> None:
    CACHE_DIR.mkdir(exist_ok=True)
    out = CACHE_DIR / "cubes_lite.json"
    resp = requests.get(URL, timeout=120)
    resp.raise_for_status()
    cubes = resp.json()
    out.write_text(json.dumps(cubes), encoding="utf-8")
    active = sum(1 for c in cubes if c.get("archiveStatusCode") == "2")
    print(f"saved {len(cubes)} cubes ({active} active) -> {out}")


if __name__ == "__main__":
    main()
