# PROJECT HANDOFF STATUS

**Generated:** 2026-02-10  
**Session Focus:** T-008 Forensic Intelligence, T-016 to T-019 (Phase 5 Complete)

---

## 1. ACTIVE PHASE & CURRENT TASK ID

**Current Phase:** Phase 5 (Diamond Layer - Refactoring & Polish) ✅ **COMPLETE**  
**Overall Progress:** 100% (27/27 tasks)  
**Current Task:** None - All tasks complete  
**Status:** ✅ Phases 1-5 Complete

**Recent Completions (2026-02-10):**
- ✅ T-008: Forensic Intelligence - `src/intelligence.py` (ForensicAnalyzer) deployed
- ✅ T-016: Dynamic Niche Directories - `data/{niche_name}/`, `reports/{niche_name}/`
- ✅ T-017: White Space Analysis - "Gap Found" / "No Gap" in Niche Reports
- ✅ T-018: Refine Migration - Strict regex `(switched|moved|migrated|changed) to {app}`
- ✅ T-019: Forensic Unit Tests - `test_forensic.py` (timeline, clusters, migration, matrix, perf)
- ✅ Tattoo AI Niche - 7 apps analyzed with forensic reports and leaderboard

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
   - **MECE Risk Scoring** (T-012): Pillar + Boost formula
3. **ForensicAnalyzer** (`src/intelligence.py`): T-008 Forensic Intelligence
   - `detect_event_timeline()` — Weekly Pain Density, anomaly detection
   - `extract_semantic_clusters()` — N-Grams (sklearn CountVectorizer / Counter fallback)
   - `map_competitor_migration()` — Churn vs Comparison (T-018 strict regex)
   - `generate_matrix()` — Pillar scores for niche heatmap
4. **Reporter:** Markdown report generation
   - Aggregate Leaderboard (T-010, T-012)
   - Individual Forensic Reports (T-008)
   - Niche Battlefield Report (Matrix, Migration Flow, White Space)
   - **Niche subdirectories** (T-016): `data/{niche_name}/`, `reports/{niche_name}/`

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
- Current Usage: ~$0.05 per run
- Projected Monthly: < $5.00 (within budget)

**Build Cost (One-Time):**
- Time to Build: Complete (5 phases, 27 tasks)
- Complexity Risk: Medium (statistical analysis, API integration, forensic modules)
- Status: 100% complete

---

## 4. SUMMARY: THE SPRINT BOARD & ACTIVE TASKS (Planning)

**Source:** `docs/ai/planning/apify-appstore-scraper.md`

### Completion Status
- **Phase 1 (Bronze):** 100% (3/3 tasks) ✅
- **Phase 2 (Silver):** 100% (3/3 tasks) ✅
- **Phase 3 (Gold):** 100% (3/3 tasks) ✅
- **Phase 4 (Platinum):** 100% (4/4 tasks) ✅
- **Phase 5 (Diamond):** 100% (4/4 tasks) ✅

**Overall Progress:** 100% (27/27 tasks)

### Niches Analyzed
| Niche | Apps | Output Location |
|-------|------|-----------------|
| Digital Detox | 5 | `data/digitaldetox/`, `reports/` (legacy) |
| Voice AI | 5 | `data/voicenotesai/` |
| Tattoo AI | 7 | `data/Tattoo_AI/`, `reports/Tattoo_AI/` |

### Output Structure (T-016)
- **Config:** `targets.json` → `niche_name` (e.g., "Tattoo_AI")
- **Data:** `data/{niche_name}/*_reviews.json`, `*_analysis.json`, `market_leaderboard.md`
- **Reports:** `reports/{niche_name}/report_*.md`, `*_intelligence.json`, `niche_matrix.json`

### All Tasks Complete
- No active tasks; pipeline fully operational

---

## 5. MODIFIED FILES (Full Implementation)

### Core Implementation Files
1. **`main.py`**
   - T-008: Forensic pipeline (ForensicAnalyzer, intelligence.json, individual + niche reports)
   - T-016: Niche subdirectories (`data/{niche_name}/`, `reports/{niche_name}/`)

2. **`src/intelligence.py`** (NEW)
   - ForensicAnalyzer class
   - detect_event_timeline, extract_semantic_clusters, map_competitor_migration, generate_matrix
   - T-018: Strict migration regex

3. **`src/reporter.py`**
   - generate_report() — Executive Verdict, Exhibits A–C (Timeline, Clusters, Quotes)
   - generate_niche_report() — Matrix, Migration Flow
   - T-017: White Space Analysis section

4. **`src/fetcher.py`**
   - T-014: Multi-Region Support (agents/appstore-reviews, country config)

5. **`src/config_validator.py`**
   - T-016: Optional `niche_name` validation

### Configuration Files
6. **`config/targets.json`**
   - Added `niche_name` (e.g., "Tattoo_AI")

7. **`config/README.md`**
   - Documented `niche_name` schema

### Test Files
8. **`test_forensic.py`** (NEW)
   - T-019: Forensic unit tests (timeline, clusters, migration, matrix, perf < 2s)

### Dependencies
9. **`requirements.txt`**
   - Added scikit-learn (N-Gram analysis)

---

## 6. NEXT ACTIONS (When We Return)

### Maintenance & Enhancement
1. **Design Doc Update**
   - Add `niche_name` to targets.json schema in `docs/ai/design/apify-appstore-scraper.md`
   - Document subfolder layout (`data/{niche}/`, `reports/{niche}/`)

2. **Optional Improvements**
   - Configurable pillar mapping (move from code to config)
   - Export options (CSV, JSON) for leaderboard
   - Parallel processing for multiple apps

### Validation
3. **Run Full Pipeline**
   ```bash
   export APIFY_API_KEY=your_token
   python main.py
   ```

4. **Run Forensic Tests**
   ```bash
   python test_forensic.py
   ```

---

## 7. KEY INSIGHTS & DECISIONS

### Forensic Intelligence (T-008)
- **Timeline:** Pain Density = (reviews with pain keywords) / (total reviews per week); anomaly = μ + 2σ
- **N-Grams:** sklearn CountVectorizer (ngram_range 2–3) with Counter fallback; filters generic phrases
- **Migration:** T-018 strict regex — only `(switched|moved|migrated|changed) to {app}` counts as churn; "better than" ignored
- **Matrix:** Pillar densities × 10, capped at 100; 🔴 for scores > 50

### White Space (T-017)
- **Logic:** Apps with Functional < 30 AND Economic < 30 = "safe harbor"
- **Output:** "Gap Found: [App Name] — safe harbor(s)" or "No Gap: All apps risky"

### Niche Directories (T-016)
- **Config:** `targets.json` → `niche_name` (optional; default "default")
- **Paths:** All outputs under `data/{niche_name}/` and `reports/{niche_name}/`

---

## 8. BLOCKERS & RISKS

### Current Blockers
- **None** — All phases complete

### Resolved Issues
- **ERROR C003 "Got no reviews"** ✅ RESOLVED (T-014)
- **T-008 Forensic Reporting** ✅ COMPLETE
- **Hardcoded niche name** ✅ RESOLVED (T-016)
- **Missing White Space Analysis** ✅ RESOLVED (T-017)
- **Migration false positives** ✅ RESOLVED (T-018)
- **No Forensic tests** ✅ RESOLVED (T-019)

### Technical Debt
- Pillar mapping hardcoded in Analyzer (could move to config)
- Evidence selection uses text length as proxy
- Critical keywords in fetcher hardcoded (could load from pain_keywords.json)

---

## 9. METRICS & VALIDATION

### Test Results
- **test_forensic.py:** All 5 tests pass ✅
- **Config validation:** targets.json, pain_keywords.json, settings.json valid ✅
- **Smoke test:** Available via `python main.py --smoke-test`

### Tattoo AI Niche (Sample Output)
- **Reports:** `reports/Tattoo_AI/report_*.md`
- **White Space:** "Gap Found: Tattoo AI Design, Tattoo AI Design HubX — safe harbor(s)"
- **Matrix:** Functional, Economic, Experience scores with 🔴/🟢 indicators

---

**Status:** Project complete. Pipeline operational with Forensic Intelligence, niche organization, and unit tests. Ready for maintenance or enhancement.
