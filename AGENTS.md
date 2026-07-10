# statcan_codr — Agent Guide

> Single source of truth for *how to work on this repo*. Claude and Antigravity both read this (`CLAUDE.md` → `@AGENTS.md`; `GEMINI.md` → pointer). Keep it short.

**Brain note (goals, backlog, full context):** `H:\My Drive\Brain2\Projects\statcan_codr.md`
**GitHub:** `https://github.com/p3ji/statcan_codr`
**Live site:** `https://p3ji.github.io/statcan_codr/`
**Plan of record:** `docs/phaseone.md`
**Stack:** Python (pipeline) + plain HTML/JS + DuckDB-Wasm (site, no build step)

## Run / build / test
- Refresh benchmark data: `python pipeline/extract.py` — pulls all `status: confirmed` cells in `pipeline/indicators.yaml` from live APIs, validates, writes `public/data/global_cities.parquet`. Requires `pip install -r pipeline/requirements.txt`.
- Preview the site locally: `python -m http.server 8081` from the repo root (or use the `dashboard` config in `.claude/launch.json`), then open `http://localhost:8081/`.
- No build step for the site — `index.html`/`app.js`/`style.css` are served as-is.

## Conventions & gotchas
- **`index.html` must stay at repo root**, not a subfolder — GitHub Pages' "Deploy from a branch" source only supports the repo root or `/docs`. `pipeline/extract.py`'s `OUTPUT_PATH` and `.github/workflows/deploy.yml`'s artifact `path` assume this.
- **`mcp-statcan`'s bulk-fetch tools are broken** (`get_bulk_vector_data_by_range`, `get_changed_series_data_from_vector` throw HTTP 404/406 on valid vectors). `extract.py` bypasses the MCP entirely and calls StatCan WDS / FRED / ABS SDMX / Statistics Finland PxWeb directly via `requests`.
- **`mcp-statcan` needs one-time interactive approval** in a terminal `claude` session before its tools are usable — non-terminal Claude Code clients (this includes most embedded/desktop UIs) can't render that approval prompt, so MCP-dependent discovery work has to happen in an actual terminal.
- Series-level detail (exact vector/series IDs, comparability caveats, unresolved cells) lives in `pipeline/indicators.yaml`, not here — it's the manifest, not documentation to duplicate.
- Keep this file short; put goals/backlog/status/rationale in the linked Brain note, not here.

## Do NOT
- Commit secrets (`.env`) or large build artifacts.
- Add a FRED API key to code or commit it — the FRED fetcher deliberately uses the keyless `fredgraph.csv` endpoint instead.
