"""Goal-1 engine audit, search-engine layer: DuckDuckGo (html endpoint).

For every query in queries.yaml, fetch the top-10 organic results and record
each result's rank, URL, domain, and source class. Throttled to ~1 request
per 2.5s. Output: visibility/results/ddg_<date>.csv (long format, one row
per query x result).

Bing/Google are NOT scripted: both serve JS shells or bot checks to plain
clients; they are covered manually via the browser sample instead.
"""
from __future__ import annotations

import csv
import re
import time
import urllib.parse
from pathlib import Path

import requests
import yaml

HERE = Path(__file__).parent
RESULTS = HERE / "results"
RUN_DATE = "2026-07-18"

UA = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/126.0 Safari/537.36"
}

# Domains known to primarily republish/derive from StatCan data for Canadian stats.
REPUBLISHERS = {
    "tradingeconomics.com",
    "macrotrends.net",
    "statista.com",
    "wikipedia.org",
    "ycharts.com",
    "worldpopulationreview.com",
    "fred.stlouisfed.org",
    "theglobaleconomy.com",
    "countryeconomy.com",
    "wowa.ca",
}


def classify(domain: str) -> str:
    d = domain.lower().removeprefix("www.")
    if d.endswith("statcan.gc.ca"):
        return "statcan"
    if any(d == r or d.endswith("." + r) for r in REPUBLISHERS):
        return "republisher"
    if d.endswith("gc.ca") or d.endswith("canada.ca"):
        return "other_gov"
    return "other"


def ddg_top10(query: str) -> list[str]:
    r = requests.get(
        "https://html.duckduckgo.com/html/", params={"q": query}, headers=UA, timeout=30
    )
    r.raise_for_status()
    raw = re.findall(r'result__a" href="([^"]+)"', r.text)
    urls = []
    for u in raw:
        if u.startswith("//duckduckgo.com/l/"):
            qs = urllib.parse.parse_qs(urllib.parse.urlparse("https:" + u).query)
            u = qs.get("uddg", [""])[0]
        u = u.replace("&amp;", "&")
        if u:
            urls.append(u)
    return urls[:10]


def main() -> None:
    RESULTS.mkdir(exist_ok=True)
    out_path = RESULTS / f"ddg_{RUN_DATE}.csv"
    manifest = yaml.safe_load((HERE / "queries.yaml").read_text(encoding="utf-8"))

    rows = []
    failures = []
    n_done = 0
    for subject, queries in manifest["subjects"].items():
        for q in queries:
            try:
                urls = ddg_top10(q["query"])
            except Exception as e:  # keep going; log the miss
                failures.append((q["id"], str(e)))
                time.sleep(10)
                continue
            if not urls:
                failures.append((q["id"], "0 results (possible bot check)"))
            for rank, url in enumerate(urls, start=1):
                domain = urllib.parse.urlparse(url).netloc
                rows.append(
                    {
                        "run_date": RUN_DATE,
                        "engine": "duckduckgo",
                        "id": q["id"],
                        "subject": subject,
                        "query": q["query"],
                        "rank": rank,
                        "url": url,
                        "domain": domain,
                        "source_class": classify(domain),
                    }
                )
            n_done += 1
            if n_done % 10 == 0:
                print(f"{n_done} queries done, {len(rows)} rows")
            time.sleep(2.5)

    with out_path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)
    print(f"wrote {len(rows)} rows for {n_done} queries -> {out_path}")
    if failures:
        print("FAILURES:", failures)


if __name__ == "__main__":
    main()
