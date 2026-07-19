# Is Statistics Canada answering Canadians' questions? — Pilot study report

**Date:** 2026-07-18 · **Scope:** 100 real-world queries across three subjects (Labour;
Digital economy and society; Society and community) · **Artifacts:**
`visibility/queries.yaml` (coded query bank), `visibility/results/` (engine audit data),
`docs/visibility.md` (plan of record)

## Executive summary

Statistics Canada **could answer 85 of 100** everyday questions in the pilot subjects
(47 fully, 38 partially). Whether generative AI actually uses it varies sharply by
surface: Bing's AI answer boxes cited StatCan directly on only 3 of 12 sampled queries,
while a consumer chatbot (Duck.ai / GPT-5.4-nano with auto web search) cited it on 8 of
10. But across every surface one structural fact holds: **generative AI cites StatCan's
crawlable article layer (The Daily, analytical pieces) and never its data tables** —
table values render via JavaScript, bulk CSVs are robots.txt-blocked, and there is no
dataset markup, so tables can rank in search yet contribute nothing to answers. The
consequence is that chatbot answers inherit whatever vintage the last crawlable article
carried: 2021 loneliness figures while the 2024 table sits published, 2018 social-media
data, 2013 friendship counts, a 2006–2011-vintage immigrant-unemployment rate served
with two-decimal precision. Where no StatCan artifact exists at all, SEO content farms
(madeinca.ca holds the #1 search result on 10 of 100 queries) and commercial press
releases fill the vacuum — the misinformation exposure StatCan could be countering.

The three hypothesized underutilization mechanisms were all observable in the coding:

1. **Unpublished indicators** — collected-but-not-tabled topics (screen time, social
   media use, cyberbullying, gig work, AI chatbot use) are exactly where commercial
   surveys and press releases dominate the answer space.
2. **Shallow disaggregation** — the Canadian Social Survey tables carry 64
   sociodemographic characteristics but only as one-way national breakdowns: you can
   get loneliness *for immigrants* or *by province*, never both. Users demonstrably
   want the crossings (autocomplete: "by city", "for immigrants", "in seniors").
3. **No integration** — all 5 integration-type queries (e.g. "is screen time linked to
   worse teen mental health") were answerable only partially or via one-off studies.

## 1. What was measured

Three questions, per the study design in `docs/visibility.md`:
(1) do engines cite StatCan? (2) could StatCan have answered? (3) why not?
This pilot completed **goal-2 coding** for all 100 queries against the live WDS cube
list (8,212 cubes; 5,056 current), with dimension-level verification via
`getCubeMetadata` on pivotal tables, plus barrier spot-checks and a 3-query engine
smoke test. The full engine audit (goal 1) is the next phase.

The query bank mixes real Google-autocomplete phrasings (collected 2026-07-18) with
curated probes. Autocomplete itself is demand-side evidence: users natively append
"by province", "by city", "by age", "for immigrants" — and some search for the
*Canadian Social Survey by name*.

## 2. Could StatCan answer? (goal-2 coding, n=100)

| | fully | partially | microdata_only | not_collected |
|---|---|---|---|---|
| **All (100)** | **47** | **38** | **11** | **4** |
| Labour (34) | 20 | 10 | 2 | 2 |
| Digital economy & society (33) | **5** | 17 | 9 | 2 |
| Society & community (33) | 22 | 11 | 0 | 0 |

Coding: *fully* = current published table at the needed granularity; *partially* =
indicator exists but stale, discontinued, wrong granularity, or split across sources;
*microdata_only* = collected but published only in one-off articles; *not_collected* =
another organization owns the indicator (ESDC minimum wage, CRTC broadband, Bank of
Canada crypto, CAFC fraud losses).

**Labour is the strong flank** — LFS/SEPH tables are current, monthly, and
well-disaggregated. **Society is surprisingly strong** thanks to the Canadian Social
Survey's 45-10 table family (loneliness, trust, belonging, discrimination, life
satisfaction — all current to 2024–25). **Digital economy and society is the collapse
zone**: only 5 of 33 fully answerable, in the very subject where internet-native
questions are asked most.

### Probe results (curated queries designed to test each mechanism)

- `unpublished_indicator` (8): 5 microdata_only, 2 partially, 1 refuted (time with
  friends *is* published — TUS 2022). Largely confirmed.
- `shallow_disaggregation` (8): 3 fully, 5 partially. Confirmed with nuance — the CSS
  carries many characteristics but only one-way at national level.
- `no_integration` (5): 4 partially, 1 microdata_only, **0 fully**. Confirmed.

### Notable individual findings

- **"Number of close friends": last table is 2013** (45100021) — a 13-year gap on a
  core social-connectedness indicator during a "loneliness epidemic" news cycle.
- **Retail e-commerce sales table discontinued in 2022** (20100072) — StatCan exited
  the e-commerce measurement story mid-narrative; Statista now owns those answers.
- **The LFS immigrant-status annual table went inactive at end-2024** (14100083) with
  no obvious successor in the cube list.
- **Zero cubes title-match "social media", "cyberbullying", or "broadband."**
- Digital-economy publishing fragments into dozens of one-cycle business-survey cubes
  (33-10-xxxx, each ending the quarter it was collected) rather than continuing series.

## 3. Why engines don't cite StatCan (barriers, verified 2026-07-18)

| Barrier | Verdict | Evidence |
|---|---|---|
| StatCan blocks AI crawlers | **Refuted** | robots.txt names no AI crawlers (GPTBot, ClaudeBot, Google-Extended, CCBot, PerplexityBot all unmentioned) |
| Data invisible to non-JS crawlers | **Confirmed** | t1/tbl1 pages render values client-side; a no-JS crawler sees the filter UI and no numbers (checked PID 1810000401) |
| Bulk files uncrawlable | **Confirmed** | www150 robots.txt disallows `.csv`, `.xls`, `.txt`; 2-second crawl-delay |
| No machine-readable dataset markup | **Confirmed** | No schema.org/Dataset JSON-LD, no meta description on table pages |
| Presence in AI training corpora | Untested | Next: check Common Crawl for t1/tbl1 URLs |
| Terminology mismatch | Partially observed | e.g. users ask "screen time"; StatCan publishes "time spent on various activities" and "sedentary behaviour" |

## 3b. Do engines actually cite StatCan? (goal-1 results, 2026-07-18)

Two engines measured: **DuckDuckGo organic** (all 100 queries, scripted via
`visibility/run_audit_ddg.py`; data in `visibility/results/ddg_2026-07-18.csv`) and
**Bing AI answers** (stratified 12-query sample via browser;
`visibility/results/bing_ai_sample_2026-07-18.csv`). Google and Perplexity were
inaccessible to automation (bot checks); they are future manual work.

### Search layer (DDG organic, n=100)

| StatCan appears at… | All | Labour | Society | Digital |
|---|---|---|---|---|
| Rank 1 | 45% | 58% | 48% | **27%** |
| Top 3 | 69% | 76% | 69% | 60% |
| Top 10 | 89% | 94% | 87% | 84% |

- Visibility tracks answerability: on *fully answerable* queries StatCan is #1 63% of
  the time; on *partially* answerable ones, 28%. When StatCan publishes a current
  table, search finds it; where publishing is weak, the vacuum is filled.
- Who holds #1 when StatCan doesn't: other sites 41 (led by **madeinca.ca, an SEO
  content farm, at 10 of 100 queries** — the second-biggest "publisher" of Canadian
  statistics in this sample), other government 11, republishers 3.
- Of StatCan's 45 #1 results: 21 publications/articles, 8 Daily releases, 14 data
  tables. Tables *can* rank — titles and metadata are indexed — which sharpens the
  mechanism: **discoverability is partial, but machine-readability of the values is
  the binding constraint.** A ranked table is a dead end for an answer engine that
  cannot read its numbers.
- The pure underutilization-gap cell (fully answerable, yet StatCan not in top 3)
  contains 9 queries, including "average salary by age/by province" (LFS wage tables
  exist), "do canadians trust the government" (Confidence in Institutions, 2024), and
  "volunteering in canada statistics" (GSS-GVP 2023).

### Chatbot layer (Duck.ai / GPT-5.4-nano with auto web search, n=10 stratified)

This is the closest measurement to goal 1 proper: a consumer chatbot session, fresh
chat per query, query asked naturally plus "What's the source?"
(`visibility/results/duckai_sample_2026-07-18.csv`). Note: in 2026 consumer chatbots
auto-invoke web search on statistical questions — the parametric-only arm barely
exists at the default settings; what matters is what the retrieval layer feeds them.

**8 of 10 answers cited StatCan directly**, 1 indirectly, 1 not at all — far better
than Bing's answer boxes on the same queries. The chatbot resisted traps Bing fell
into: it rejected the SEO gig-work number in favour of StatCan's measured 871k with
definitional caveats, and on screen time explicitly said no single Canadian average
exists rather than quoting commercial surveys. But the wins hide the deeper pattern:

- **Chatbots cite StatCan's article layer, never its tables.** Every direct citation
  resolved to a Daily release or analytical article. Table 45100048 (loneliness,
  updated Feb 2025) never surfaced in any answer — the chatbot cited the 2021 Daily
  article instead, serving a 3-year-stale number while the current one sat published.
- **Where the newest article is old, the answer is old**: social media use by age →
  direct StatCan citation, 2018 data (the June 2024 article's vintage); close friends
  → 2013. The article layer is a snapshot cache of the database with no refresh
  policy; whatever vintage the last crawlable article carried is what Canada's
  chatbots now say.
- **The granularity gap produces confident zombie numbers**: recent immigrants in
  Toronto → "10.92%", from a TRIEC factsheet built on 2006–2011 LFS data, served with
  two-decimal precision. Nothing current exists at that crossing, so a 15-year-old
  intermediary wins.
- **Trust in government**: StatCan absent again (OECD country note cited) — the same
  query where it lost the SERP; its current 2024 table is invisible at every layer.

Method caveats: one model (GPT-5.4-nano) on one aggregator whose retrieval backend
(DDG/Bing-derived) we separately measured as relatively StatCan-friendly; the
"What's the source?" phrasing elicits citations more than natural usage would; n=10.
Claude, ChatGPT, Gemini, Copilot chat and Perplexity require accounts or API keys —
next round.

### AI-answer layer (Bing answer boxes, n=12 stratified)

Of 12 queries, 11 produced an AI answer. Citations: **3 direct** StatCan, 2 indirect
(orgs re-using StatCan data), 1 republisher (Trading Economics), 5 with no StatCan
lineage in the answer. Failure modes observed, each tied to a coded barrier:

- **Displacement** (LAB-005): the unemployment-rate answer's number is attributed to
  Trading Economics while StatCan's tables rank directly below.
- **Vacuum-filling** (LAB-020, DIG-009, DIG-012): where StatCan has no standing table
  (gig work, social media use, e-commerce), answers are built from SEO farms and
  commercial surveys — including a gig-work figure ~8× StatCan's measured estimate and
  internally incoherent social-media percentages.
- **Staleness despite direct citation** (DIG-014, SOC-022): Bing cited StatCan and
  still served Q2-2025 AI-adoption data while the Q2-2026 release ranked #2 on the
  same page, and presented 2013 close-friends data as current fact.
- **Granularity substitution** (LAB-024): asked about recent immigrants *in Toronto*,
  the answer served the national immigrant rate as if it were Toronto's; Bing's own
  snippet flagged StatCan's table "Missing: toronto".
- **Total absence** (SOC-010): on trust in government, private pollsters (Ekos,
  Edelman) own the entire result set despite StatCan's current 2024 table.

Incidental but relevant: a Global News story (2026-07-13) reports internal polling
that only 62% of Canadians consider StatCan data reliable — the trust stakes of this
visibility gap are already in the news cycle.

**Smoke test** (one query per subject through web search):

- *"unemployment rate canada"* → the answer's number came from **Trading Economics**
  (a commercial re-publisher of StatCan data); StatCan's own tables ranked 2nd and 7th.
  StatCan is the ultimate source and loses the citation.
- *"loneliness in canada statistics"* → StatCan ranked **first** — via a 2021 Daily
  article and infographic PDF, i.e. its *crawlable static* products, not the current
  2024 table. Where StatCan publishes crawlable HTML, it wins; the surfaced content
  was 5 years stale while table 45100048 sat current and invisible.
- *"average screen time canada"* → the answer blended 3.2, 11, and 13.1 hours/day from
  Statista, an **Alcon press release**, and a 2019 poll — mutually contradictory
  self-report numbers presented as fact. The misinformation-counter case in miniature.

The pattern across all three: **engines cite what they can crawl.** StatCan's Daily
articles and PDFs surface; its tables — the current, authoritative, disaggregated
layer — do not.

## 4. Interpretation

The pilot reframes the underutilization problem as a **last-mile visibility problem
compounded by publishing choices**:

1. Where StatCan has current tables (labour), it loses citations to aggregators
   because the tables themselves are uncrawlable and unmarked-up. This is a fixable
   engineering gap (server-side rendering or static snapshots of default table views;
   schema.org/Dataset JSON-LD; allowing CSV crawling; an llms.txt/data API surface).
2. Where StatCan collects but publishes only articles (digital society), the vacuum is
   filled by commercial surveys of far lower quality — precisely the misinformation
   exposure the agency could counter.
3. Where users want crossings (immigrant × city, age × province), the one-way table
   structure means even a perfect retrieval engine could not answer from published
   products — only microdata access could.

## 5. Limitations

- Goal-2 coding is pilot-grade: title-based matching against the cube list by a single
  coder, with dimension verification on only three tables (45100049, 45100095,
  45100104). Some `candidate_table` entries are flagged for verification.
- The smoke test used one general-purpose search backend (US-based), not the six
  target engines; n=3. It illustrates, not measures.
- Autocomplete phrasings were collected without geo-pinning to Canada, and curated
  queries reflect the author's framing.
- "Answerable by another organization" (not_collected) still leaves a discovery role
  StatCan could play but doesn't.

## 6. Next steps

1. **Extend the engine audit:** Google AI Overview, Perplexity (API key needed —
   anonymous access is bot-checked), ChatGPT, Claude, Gemini; grow the Bing AI sample
   from 12 toward all 100. Add answer-correctness coding against actual StatCan values.
2. **Common Crawl check:** are t1/tbl1 URLs in AI training corpora at all?
3. **Dashboard:** DuckDB-Wasm "StatCan visibility index" page in this repo, fed by
   `visibility/results/`.
4. **Second coder pass** on the goal-2 answerability codings (single-coder pilot).

### Limitations added by the goal-1 phase

- DDG is one engine with its own index (Bing-derived); Google may differ.
- The Bing AI sample is n=12 and hand-coded from answer boxes on one day.
- `source_class` uses a fixed republisher domain list; "other" sites may also carry
  StatCan-derived numbers (the indirect share is understated).
