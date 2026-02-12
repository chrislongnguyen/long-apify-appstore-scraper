# PROJECT HANDOFF STATUS

**Generated:** 2026-02-12  
**Session Focus:** Phase 7.1 Complete; Venture Architect Live; Phase 7.2 Orchestration Done

---

## 1. ACTIVE PHASE & CURRENT TASK ID

**Current Phase:** Phase 7 — The Venture Architect 🚧  
**Current Sprint:** Phase 7.2 (Orchestration) Complete; Phase 7.3 (Reddit) Pending  
**Overall Progress:** Phases 1-6 Complete (32/32 tasks); Phase 7.1 100% (3/3); Phase 7.2 100% (2/2); Phase 7.3 0% (1 task)  
**Next Task:** T-030 (Reddit Scraper Integration) — SHOULD HAVE, not blocking  
**Status:** ✅ Phases 1-6 Complete → ✅ Phase 7.1–7.2 Complete → ⏳ Phase 7.3 Deferred

**Recent Completions (2026-02-12):**
- ✅ **T-031:** Risk Score Recalibration — Severity-First model; Learna_English 2.74 → 60.0; CriticalFloor for Economic>10%
- ✅ **T-025:** AI Client (`src/ai_client.py`) + Pydantic schemas (`src/schemas.py`) — Gemini wrapper, structured JSON output
- ✅ **T-026:** Venture Architect (`src/venture_architect.py`) — 3-stage pipeline (ICP → SysMap → EPS), repair logic for LLM output
- ✅ **T-027:** Blueprint Reporter — Jinja2 template `templates/venture_blueprint.j2`, `Reporter.render_venture_blueprint()`
- ✅ **T-028:** Success Signal Integration — `--venture-architect` CLI flag, raw_reviews + filtered_reviews wired in `main.py`
- ✅ **T-029:** Context Mocking — Architect runs with `reddit_data=[]`; graceful degradation, no Reddit required
- ✅ **Config:** `config/settings.json` `venture_architect.llm_model` / `llm_provider` — switch model (e.g. `gemini-2.5-flash`) without code change
- ✅ **Standardized JSON:** System Map payload uses `app_name`, `generated_at`, `system_dynamics`, `eps_prescription`

---

## 2. SUMMARY: THE GOAL (Requirements)

**Source:** `docs/ai/requirements/apify-appstore-scraper.md`

### Problem Space
- **Core Pain Point:** The "Founder's Guess" - lack of quantitative evidence of app failures, version degradations, or predatory monetization shifts
- **Current Workaround:** Doom-scrolling reviews or expensive, opaque market intelligence tools
- **The Gap:** Need raw, unhallucinated mathematical proof of *where* and *when* an app started failing

### The Actor
- **Primary User:** The "Product Detective" (Founder/Strategist)
- **System Actor:** `long-apify-appstore-scraper` (Python ETL Pipeline)

### Desired User Action
**Verb:** **Extract, Compute & Storytell**

**Acceptance Criteria:**
1. System must ingest App Store URLs and fetch reviews from Last 90 Days only
2. System must output `analysis_report.md` using hard data (counts, slopes, correlations) without using an LLM

### Effectiveness Constraints
- **Deterministically:** Analysis using Pandas/NumPy (no external AI calls)
- **Legally:** Respect Apify actor limits, handle timeouts gracefully
- **Surgically:** Hard filter `date >= (today - 90 days)`
- **Thriftily:** Discard reviews with `< 3 words` unless they contain "Critical Keywords"
- **Comparatively:** Support processing multiple apps for "Winner vs. Loser" comparison

### Functional Logic (Three Layers)
1. **Descriptive Analytics:** Volume of negativity (1-2 star reviews vs total per week)
2. **Predictive Analytics:** "Enshittification" curve (slope of negative reviews over time)
3. **Prescriptive Analytics:** Pain keyword density (categorized by severity: Critical, Scam, Performance, UX)

### Forensic Intelligence (T-008)
4. **Timeline of Pain:** Weekly Pain Density + anomaly detection (μ + 2σ)
5. **Semantic Clustering:** N-Gram analysis (2-3 word phrases) on 1-2 star reviews
6. **Competitor Migration:** Churn detection (`switched to X` / `moved to X`) — ignores "better than"
7. **Feature/Fail Matrix:** Niche heatmap with MECE pillars (Functional, Economic, Experience)
8. **White Space Analysis (T-017):** "Gap Found" when Functional & Economic < 30

### Predictive Analytics (Phase 6 — T-020 to T-024, T-031)
9. **Fermi Estimator:** Revenue Leakage = (Churn_Reviews × Multiplier) × Avg_Price (dynamic by niche_category)
10. **Slope Delta:** Trend acceleration (Slope_T1 vs Slope_T2); "Accelerating" / "Decelerating" / "Stabilizing"
11. **Named Spikes:** Link anomaly weeks to app version (e.g., "The Version 4.2 Crash")
12. **Whale Detector:** 3× weight for reviews > 40 words or domain vocabulary
13. **Momentum Labels:** Applied to leaderboard and reports
14. **T-031 Severity-First Risk Score:** Economic×250, Functional×200, Experience×150; CriticalFloor (Economic>10%→60); slope dampens improvement but never erases red flags

### Venture Architect (Phase 7 — T-025 to T-030)
14. **Holographic ICP:** Triangulate Pain (1-2★), Success (5★ whales), Context (Reddit)
15. **7-Node System Dynamics:** UDO, UDS/UBS, UDS.UD, UDS.UB, UBS.UD, UBS.UB
16. **EPS Prescription:** Principles, Environment, Tools, SOP derived from System Map
17. **Venture Blueprint:** `venture_blueprint_{app}.md` + `{app}_system_map.json`

---

## 3. SUMMARY: THE SOLUTION & COST (Design)

**Source:** `docs/ai/design/apify-appstore-scraper.md`

### Feature Definition
**Noun:** `AppVolatilityAnalyzer` (CLI Tool)  
**Core Function:** Python-based ETL pipeline that orchestrates Apify `agents/appstore-reviews` Actor, performs statistical analysis using Pandas/NumPy, and outputs Risk Scorecard + Forensic Reports for target apps.

### Architecture Components
1. **Fetcher:** Apify API integration with retry logic (`tenacity`)
2. **Analyzer:** Deterministic statistical analysis (Pandas/NumPy)
   - Date filtering (90 days)
   - Volatility slope calculation (`np.polyfit`)
   - Keyword density (vectorized regex)
   - **MECE Risk Scoring** (T-012, T-031): Severity-First formula — Economic 2.5×, CriticalFloor
3. **ForensicAnalyzer** (`src/intelligence.py`): T-008 Forensic Intelligence
   - `detect_event_timeline()` — Weekly Pain Density, anomaly detection
   - `extract_semantic_clusters()` — N-Grams (sklearn CountVectorizer / Counter fallback)
   - `map_competitor_migration()` — Churn vs Comparison (T-018 strict regex)
   - `generate_matrix()` — Pillar scores for niche heatmap
4. **Reporter:** Markdown report generation
   - Aggregate Leaderboard (T-010, T-012) — **Phase 6:** sorted by Revenue Leakage, Momentum column
   - Individual Forensic Reports (T-008) — **Phase 6:** Financial Impact section (Leakage, Trend)
   - Niche Battlefield Report (Matrix, Migration Flow, White Space)
   - **Niche subdirectories** (T-016): `data/{niche_name}/`, `reports/{niche_name}/`
   - **Phase 7:** `render_venture_blueprint()` — Jinja2 template for `venture_blueprint_{app}.md`
5. **Phase 6 (Predictive):** SlopeDeltaCalculator, FermiEstimator, Named Spikes, Whale Detector — all in Analyzer/Forensic
6. **Phase 7 (Venture Architect — Live):**
   - `src/ai_client.py` — Gemini wrapper, Pydantic schemas, model from `settings.json`
   - `src/venture_architect.py` — 3-stage pipeline: ICP → SysMap → EPS
   - `templates/venture_blueprint.j2` — Jinja2 Strategy Doc
   - `src/fetcher_reddit.py` — Deferred (T-030); Architect runs with `reddit_data=[]`

### Effectiveness Attributes
- **Deterministic:** Math-based scoring (no LLM)
- **Fault-Tolerant:** Retry logic, graceful error handling
- **Vectorized:** Pandas operations for performance
- **Thrifty:** In-memory filtering, drop generic 5-stars
- **Config-Driven:** Batch processing via `targets.json` (incl. `niche_name`)
- **Polylingual:** Bilingual keyword support (English/Vietnamese)

### Resource Impact
**Financial Impact (OpEx):**
- Apify API: ~$0.10 per 1,000 reviews
- Current Usage: ~$0.30 (ViralApps, Fasting Trackers, etc.)
- Phase 7 LLM: ~$0.015/niche (Gemini Flash, 3 stages × 5 apps)
- Projected Monthly: < $5.00 (within budget)

**Build Cost:**
- Phases 1-6: 100% complete (32 tasks)
- Phase 7.1–7.2: 100% complete (5 tasks); Phase 7.3 deferred (1 task)

---

## 4. SUMMARY: THE SPRINT BOARD & ACTIVE TASKS (Planning)

**Source:** `docs/ai/planning/apify-appstore-scraper.md`

### Completion Status
- **Phase 1 (Bronze):** 100% (3/3 tasks) ✅
- **Phase 2 (Silver):** 100% (3/3 tasks) ✅
- **Phase 3 (Gold):** 100% (3/3 tasks) ✅
- **Phase 4 (Platinum):** 100% (4/4 tasks) ✅
- **Phase 5 (Diamond):** 100% (4/4 tasks) ✅
- **Phase 6 (Predictive):** 100% (5/5 tasks) ✅
- **Phase 7.1 (Core Intelligence):** 100% — T-025, T-026, T-027 ✅
- **Phase 7.2 (Orchestration):** 100% — T-028, T-029 ✅
- **Phase 7.3 (Context Layer):** 0% — T-030 ⏳ (SHOULD HAVE, deferred)

**Overall Progress:** 37/38 tasks complete (Phases 1–7.2); 1 task deferred (T-030 Reddit)

### Niches Analyzed
| Niche | Apps | Output Location |
|-------|------|-----------------|
| Digital Detox | 5 | `data/digitaldetox/`, `reports/` (legacy) |
| Voice AI | 5 | `data/voicenotesai/` |
| Tattoo AI | 7 | `data/Tattoo_AI/`, `reports/Tattoo_AI/` |
| Fasting Trackers | — | `data/Fasting_Trackers/`, `reports/Fasting_Trackers/` |
| ViralApps | 5 | `data/ViralApps/`, `reports/ViralApps/` |

### Output Structure (T-016)
- **Config:** `targets.json` → `niche_name`
- **Data:** `data/{niche_name}/*_reviews.json`, `*_analysis.json`, `market_leaderboard.md`
- **Reports:** `reports/{niche_name}/report_*.md`, `*_intelligence.json`, `niche_matrix.json`
- **Phase 7 (live):** `reports/{niche_name}/venture_blueprint_{app}.md`, `{app}_system_map.json`

### Phase 7 Status
- **T-025 to T-029:** ✅ Done — AI Client, Venture Architect, Blueprint Template, CLI flag, Graceful Degradation
- **T-030:** ⏳ Deferred — Reddit Scraper (SHOULD HAVE; Architect runs without it)

---

## 5. MODIFIED FILES (Full Implementation)

### Core Implementation Files
1. **`main.py`**
   - T-008: Forensic pipeline (ForensicAnalyzer, intelligence.json, individual + niche reports)
   - T-016: Niche subdirectories (`data/{niche_name}/`, `reports/{niche_name}/`)
   - **Phase 6:** Passes analysis + forensic to Reporter for Financial Impact
   - **Phase 7:** `--venture-architect` flag; lazy init AIClient + VentureArchitect; `_json_default` for numpy/pandas JSON serialization; passes `raw_reviews`, `niche_name`, `reporter`

2. **`src/ai_client.py`** *(NEW)*
   - Gemini/OpenAI wrapper; `generate_structured()` with tenacity retry; JSON parse + Pydantic validation
   - Model configurable via `settings.json` → `venture_architect.llm_model`

3. **`src/schemas.py`** *(NEW)*
   - Pydantic models: `HolographicICP`, `SystemDynamicsMap`, `EPSPrescription`, `ICPSegment`, etc.

4. **`src/venture_architect.py`** *(NEW)*
   - 3-stage pipeline: `construct_holographic_icp` → `map_system_dynamics` → `generate_eps_prescription`
   - Repair logic for LLM output; `generate_blueprint()` saves JSON + invokes Reporter for blueprint MD

5. **`src/reporter.py`**
   - **Phase 7:** `render_venture_blueprint()` — Jinja2 template for venture_blueprint_{app}.md

6. **`src/intelligence.py`**
   - ForensicAnalyzer: detect_event_timeline, extract_semantic_clusters, map_competitor_migration, generate_matrix
   - T-018: Strict migration regex
   - **T-022:** name_spike() — link anomalies to version metadata
   - **T-023:** Whale multiplier in Pain Density

7. **`src/analyzer.py`**
   - **T-020:** FermiEstimator (Revenue Leakage)
   - **T-021:** SlopeDeltaCalculator (Trend acceleration)
   - **T-023:** Whale Detector in evidence ranking

8. **`src/fetcher.py`**
   - T-014: Multi-Region Support (agents/appstore-reviews)

9. **`src/config_validator.py`**
   - T-016: Optional `niche_name` validation
   - **Phase 7:** Optional `venture_architect` block validation (llm_model, llm_provider)

### Configuration Files
10. **`config/targets.json`**
    - `niche_name`, `niche_category` (Fermi multiplier)
    - **Phase 7.3 (planned):** `venture_architect.subreddits`, `search_queries`

11. **`config/settings.json`**
    - **Phase 7:** `venture_architect.llm_provider`, `venture_architect.llm_model` — configurable LLM (e.g. gemini-2.5-flash)

### Templates
12. **`templates/venture_blueprint.j2`** *(NEW)*
    - Jinja2 template for venture blueprint markdown (4 sections: System Map, Strategic Inversion, EPS, Trojan Horse)

### Test Files
13. **`test_forensic.py`** — Forensic unit tests
14. **`test_t024_integration.py`** — Phase 6 integration smoke test
15. **`test_ai_client.py`** *(NEW)* — AIClient JSON parse, Pydantic validation
16. **`test_venture_architect.py`** *(NEW)* — Blueprint generation, standardized JSON schema

### Dependencies
17. **`requirements.txt`**
    - scikit-learn, apify-client, tenacity, python-dotenv
    - **Phase 7:** google-generativeai, pydantic, jinja2

---

## 6. NEXT ACTIONS (When We Return)

### Optional (Phase 7.3 — Reddit)
1. **T-030 (Reddit Scraper):** Create `src/fetcher_reddit.py`; wire Apify `apify/reddit-scraper`; add `venture_architect.subreddits` to targets.json. NOT blocking — Architect works without Reddit.

### Validation
2. **Run Full Pipeline**
   ```bash
   source venv/bin/activate
   python main.py   # Uses .env for APIFY_API_KEY, GEMINI_API_KEY
   ```

3. **Run with Venture Architect**
   ```bash
   python main.py --venture-architect --smoke-test
   ```

4. **Change LLM Model:** Edit `config/settings.json` → `venture_architect.llm_model` (e.g. `gemini-2.5-flash`)

---

## 7. KEY INSIGHTS & DECISIONS

### Forensic Intelligence (T-008)
- **Timeline:** Pain Density = (reviews with pain keywords) / (total reviews per week); anomaly = μ + 2σ
- **N-Grams:** sklearn CountVectorizer (ngram_range 2–3) with Counter fallback
- **Migration:** T-018 strict regex — only `(switched|moved|migrated|changed) to {app}` counts as churn
- **Matrix:** Pillar densities × 10, capped at 100; 🔴 for scores > 50

### Phase 6 (Predictive Analytics)
- **Fermi:** Leakage = (Churn_Reviews × Multiplier) × Price; Multiplier by niche_category (B2B 50, Consumer 100, Games 200)
- **Slope Delta:** Slope(Last 4 weeks) vs Slope(Weeks 5–8); positive Δ = accelerating decline
- **Momentum:** volatility_slope + slope_delta → Accelerating / Decelerating / Stabilizing / Improving
- **Whale:** > 40 words or domain vocab → 3× weight in Pain Density and evidence ranking

### Phase 7 (Venture Architect)
- **3 Data Signals:** Pain (1-2★), Success (5★ whales > 30 words), Context (Reddit)
- **Success Signal:** `raw_reviews` (pre-filter) passed to Architect; Fetcher unchanged
- **7-Node Map:** UDO → UDS/UBS → UDS.UD, UDS.UB, UBS.UD, UBS.UB (Biology = Layer 5)
- **Graceful Degradation:** Architect runs with `reddit_data=[]`; Reddit is SHOULD HAVE

### Environment
- **python-dotenv:** `.env` loads `APIFY_API_KEY`, `GEMINI_API_KEY` at startup; no manual export needed

---

## 8. BLOCKERS & RISKS

### Current Blockers
- None. Phase 7.1–7.2 complete; T-030 (Reddit) is deferred.

### Resolved Issues
- **ERROR C003 "Got no reviews"** ✅ RESOLVED (T-014)
- **T-008 Forensic Reporting** ✅ COMPLETE
- **Hardcoded niche name** ✅ RESOLVED (T-016)
- **Migration false positives** ✅ RESOLVED (T-018)
- **APIFY_API_KEY not loading** ✅ RESOLVED (python-dotenv)
- **T-025 Phase 7 blocker** ✅ RESOLVED (AI Client + Schemas implemented)

### Phase 7 Risks (Mitigation)
- **R1 Hallucination:** Strict Pydantic schemas; fail loud on validation error
- **R2 Token Cost:** Cluster Summarizer caps evidence at ~3000 tokens/stage
- **R3 Shallow Analysis:** Depth validation — assert UDS.UD/UBS.UD reach Layer 5

---

## 9. METRICS & VALIDATION

### Test Results
- **test_forensic.py:** Forensic unit tests pass ✅
- **test_t024_integration.py:** Phase 6 integration smoke test ✅
- **test_ai_client.py:** AIClient + Pydantic validation ✅
- **test_venture_architect.py:** Blueprint generation, standardized JSON schema ✅
- **Config validation:** targets.json, pain_keywords.json, settings.json valid ✅
- **Smoke test:** `python main.py --smoke-test` ✅
- **Venture Architect smoke:** `python main.py --venture-architect --smoke-test` ✅

### Recent Niche Runs
- **ViralApps:** 5 apps — Revenue Leakage, Momentum labels, Financial Impact in reports; Venture Blueprint + System Map (Learna_English)
- **Fasting Trackers:** Leaderboard with monthly_leakage_usd sort

### Docs
- **Requirements:** `docs/ai/requirements/` — Phase 7 "7-Layer System Dynamics" + EPS Generator
- **Design:** `docs/ai/design/` — Full Phase 7 architecture (1200+ lines)
- **Planning:** `docs/ai/planning/` — T-025 to T-030 with specs

---

**Status:** Phases 1-6 production-ready. Phase 7.1–7.2 production-ready (Venture Architect live). Next: T-030 (Reddit) optional.
