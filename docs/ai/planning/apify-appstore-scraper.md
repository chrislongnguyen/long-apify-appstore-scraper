---
phase: planning
title: Execution Plan - App Volatility Analyzer
description: Step-by-step implementation matrix for the Python ETL pipeline (Fetcher -> Analyzer -> Reporter).
last_updated: 2026-02-09
---

# QUICK STATUS SUMMARY

**Current Phase:** Phase 4 (Platinum Layer - The Reporter & Aggregator)  
**Overall Progress:** 79% (19/24 tasks)  
**Next Task:** T-008 - Gen Markdown (Storytelling reports)  
**Status:** ✅ Phases 1, 2 & 3 Complete | ✅ T-011 Complete | ✅ T-012 Complete | ✅ T-010 Complete | ⏳ T-008 Pending

**Recent Achievements:**
- ✅ Apify integration working (100+ reviews fetched successfully)
- ✅ Config-driven filtering implemented
- ✅ Bug fixes: URL format, datetime handling, error responses
- ✅ Knowledge documentation created
- ✅ Analyzer implemented: Pandas/NumPy slope calculation, keyword density, risk scoring
- ✅ schema_app_gap.json generation working
- ✅ Loop robustness: Batch processing with error handling (all 5 apps processed)
- ✅ Aggregate Leaderboard: Market comparison table generated (`data/market_leaderboard.md`)

---

# 1. MACRO ROADMAP (Timeline & Resources)

| Milestone | Target Date | Resource Budget (Est.) | Critical Risk |
| :--- | :--- | :--- | :--- |
| **M1: Bronze (The Skeleton)** | Day 1 | $0.00 | Environment & Config handling fails |
| **M2: Silver (The Fetcher)** | Day 1 | $0.20 (Apify) | API Schema changes or Rate Limits |
| **M3: Gold (The Brain)** | Day 2 | $0.00 (Local) | Math logic (Slope/Scoring) is incorrect |
| **M4: Platinum (The Story & Comparison)** | Day 2 | $0.00 | Report is unreadable/cluttered |

---

# 2. EXECUTION MATRIX (The "Micro" View)

* **Risk Factor:** (Impact 1-10) $\times$ (Prob 0.0 - 1.0). **>6 = Critical.**
* **Outcome:** The specific "Adverb" (Sustainability/Efficiency) we are optimizing for.

## PHASE 1: BRONZE LAYER (Setup & Config)
| ID | Task (Verb) | Target Outcome (Adverb) | Risk Factor | Deps/Blockers | Status |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **T-001** | **Init Python Env** | *Cleanly* (Isolated Venv) | **Low (2)** | None | ✅ Done |
| **T-002** | **Create Configs** | *Explicitly* (JSON Schemas) | **Low (3)** <br> *(Imp:6, Prob:0.5)* | T-001 | ✅ Done |
| **T-003** | **Scaffold Classes** | *Modularly* (Empty Classes) | **Low (1)** | T-002 | ✅ Done |

## PHASE 2: SILVER LAYER (The Fetcher)
| ID | Task (Verb) | Target Outcome (Adverb) | Risk Factor | Deps/Blockers | Status |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **T-004** | **Connect Apify** | *Reliably* (Tenacity Retry) | **Med (5)** <br> *(Imp:10, Prob:0.5)* | T-003 | ✅ Done |
| **T-005** | **Filter & Save** | *Thriftily* (Drop 5-stars) | **Med (4)** | T-004 | ✅ Done |

## PHASE 3: GOLD LAYER (The Analyzer - Critical)
| ID | Task (Verb) | Target Outcome (Adverb) | Risk Factor | Deps/Blockers | Status |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **T-006** | **Calc Logic** | *Deterministically* (Pandas) | **High (8)** <br> *(Imp:10, Prob:0.8)* | T-005 | ✅ Done |
| **T-007** | **Score Risk** | *Accurately* (Formula Check) | **High (7)** | T-006 | ✅ Done |
| **T-009** | **Loop Robustness** | *Resiliently* (Error Handling) | **Low (2)** | T-007 | ✅ Done |

## PHASE 4: PLATINUM LAYER (The Reporter & Aggregator)
| ID | Task (Verb) | Target Outcome (Adverb) | Risk Factor | Deps/Blockers | Status |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **T-011** | **Analyzer Calibration** | *Accurately* (Normalized & Sensitive) | **Med (3)** | T-009 | ✅ Done |
| **T-012** | **Advanced Reporting (Metrics 2.0)** | *MECE* (Pillar + Boost) | **Med (4)** | T-011 | ✅ Done |
| **T-010** | **Aggregate Leaderboard** | *Holistically* (Ranked Comparison) | **Low (2)** | T-012 | ✅ Done |
| **T-008** | **Gen Markdown** | *Legibly* (Storytelling) | **Low (2)** | T-010 | 🔴 To Do |

---

# 3. DETAILED SPECIFICATIONS (High Risk Tasks)

### T-002: Create Configs (The Foundation)
* **User Story:** As the System, I need valid JSON files to know what to scrape and how to score it.
* **Action:** Create `config/targets.json` (Target Apps) and `config/pain_keywords.json` (Bilingual Dictionary).
* **Validation:** Script must crash gracefully if files are missing or malformed JSON.

### T-006: Calc Logic (The "Enshittification" Engine)
* **User Story:** As a Data Scientist, I want to see the *change* in sentiment, not just the average.
* **Complex Logic (Pandas):**
    1.  **Filter:** `df = df[df['date'] >= (today - 90d)]`
    2.  **Resample:** Group by Week (`df.set_index('date').resample('W').count()`).
    3.  **Slope:** `np.polyfit(x=week_indices, y=negative_review_counts, deg=1)[0]`
    4.  **Keyword Density:** Use `df['text'].str.count(regex)` against the loaded `pain_keywords.json`.
* **Rollback Plan:** If `np.polyfit` fails (not enough data points), default Slope to `0.0` and log a warning.

### T-007: Score Risk (The Formula)
* **Logic:** Implement the LaTeX formula from Design.
    ```python
    risk_score = min(100,
        (20 * slope_score) + 
        (0.5 * vol_score) + 
        (sum(cat_count * cat_weight))
    )
    ```
* **Constraint:** Result must be an `float` rounded to 2 decimal places.

### T-010: Aggregate Leaderboard (The Holistic Comparison)
* **User Story:** As a Strategist, I want to see a ranked comparison of all apps to identify winners vs. losers.
* **Action:** Load all `schema_app_gap.json` files from `data/` folder, rank by risk_score, generate comparison table.
* **Output:** 
  - Ranked list of apps (highest risk_score = most volatile)
  - Comparison metrics: risk_score, volatility_slope, negative_ratio, top_pain_categories
  - Save as `data/leaderboard.json` or `data/comparison_report.md`
* **Validation:** Must handle missing analysis files gracefully (skip apps without analysis).

### T-011: Analyzer Calibration (Fix Math Models)
* **User Story:** As a Data Scientist, I want accurate, normalized metrics that reflect app volatility without volume bias or semantic drift.
* **Action:** Fix three critical data anomalies in `src/analyzer.py`:
  1. **Score Inflation:** Risk Score is unbounded (reached 93.0) due to raw count * weight multiplication. Must normalize by dividing by total reviews to prevent artificial inflation.
  2. **Ghost Ratio:** Negative Ratio is 0.0% because definition is hardcoded to `score.isin([1, 2])` (1-2 star only), ignoring 5-star reviews with pain keywords. Must redefine "negative" as any review containing pain keywords.
  3. **Flatline Slope:** Volatility Slope is 0.0000 across all apps because `np.polyfit` receives zero 1-2 star reviews. Must recalculate slope based on pain-keyword-driven signals instead of traditional negative reviews.
* **Implementation Details:**
  - Line 233: Change `category_score += count * weight` to `category_score += (count / total_reviews) * weight * 100` for normalization
  - Lines 310-312: Redefine negative_count as reviews with any pain keyword match, not just `score.isin([1, 2])`
  - Lines 114-131: Recalculate slope using keyword density trend per week instead of low-star review counts
* **Dependencies:** ✅ T-009 (Loop Robustness complete)
* **Risk:** Medium (3) - Critical for valid insights; incorrect metrics invalidate all downstream decisions
* **Validation:** Rerun leaderboard; verify Risk Scores normalize to 0-100 range, negative_ratio > 0%, and slopes show trend direction
* **Status:** ✅ Done

### T-012: Advanced Reporting (Metrics 2.0 - MECE Risk Scoring)
* **User Story:** As a Strategist, I want MECE (Mutually Exclusive, Collectively Exhaustive) risk scoring with educational reporting that groups pain points into actionable pillars.
* **Action:** Implement Pillar + Boost formula and enhance leaderboard with pillar-based insights.
* **Implementation Details:**
  1. **Refactor `src/analyzer.py` (MECE Logic):**
     - **Step A:** Map categories to MECE Pillars:
       - Functional Risk: `critical`, `performance`, `privacy`
       - Economic Risk: `scam_financial`, `subscription`, `ads`
       - Experience Risk: `usability`, `competitor_mention`, `generic_pain`
     - **Step B:** Calculate Pillar Density: $Density = \frac{\sum \text{Weights of Matching Keywords}}{\text{Total Reviews Analyzed}}$
     - **Step C:** Calculate Base Risk: $BaseScore = (\text{FunctionalDensity} + \text{EconomicDensity} + \text{ExperienceDensity}) \times 10.0$
     - **Step D:** Apply Volatility Boost: $FinalRisk = \min(100.0, BaseScore \times (1 + \max(0, VolatilitySlope)))$
  2. **Refactor `src/reporter.py` (Enhanced Leaderboard):**
     - Update `aggregate_leaderboard()` to include columns: Rank, App Name, Risk Score, Vol. Slope, Neg. Ratio, Volume, Primary Pillar, Suspected Version
     - Add detailed footer explaining MECE pillars and risk interpretation
* **Dependencies:** ✅ T-011 (Analyzer Calibration complete)
* **Risk:** Medium (4) - Formula complexity and pillar mapping accuracy
* **Validation:** Verify Risk Scores use MECE formula, leaderboard shows all columns, and pillar assignments are logical

---

# 4. RESOURCE & BUDGET TRACKER
| Metric | Current Usage | Hard Limit | Status |
| :--- | :--- | :--- | :--- |
| **Financial Cost** | ~$0.01-0.02 | $5.00 | 🟢 Safe |
| **API Calls** | ~3 successful runs | N/A | 🟢 Safe |
| **Reviews Fetched** | ~100+ reviews | N/A | 🟢 Safe |

**Note:** Actual API usage from smoke tests. Cost estimate based on Apify pricing ($0.10 per 1,000 reviews).

---

# 5. ADDITIONAL WORK COMPLETED (Not in Original Plan)

## T-009: Loop Robustness (The Resilient Pipeline)
* **User Story:** As the System, I need to process all apps even if one fails, providing a complete summary.
* **Action:** Improved error handling in `main.py` loop with try/except blocks, progress tracking, and success/failure summary.
* **Impact:** Enables batch processing of multiple apps without stopping on individual failures.
* **Status:** ✅ Done

## T-010: Config Externalization ✅
* **Discovered:** Need to externalize hardcoded logic for scalability
* **Action:** Created `config/settings.json` with filters, weights, and processing settings
* **Impact:** Enables runtime configuration without code changes
* **Status:** ✅ Done

## T-011: Bug Fixes & Improvements ✅
* **Issues Fixed:**
  - Apify URL format: Changed from `[{"url": "..."}]` to `["..."]` (array of strings)
  - Datetime comparison: Fixed timezone-aware vs naive datetime comparison
  - Error response handling: Added filtering for Apify error objects
  - URL validation: Added type checking to prevent object/string confusion
* **Status:** ✅ Done

## T-012: Knowledge Documentation ✅
* **Action:** Created `docs/ai/implementation/knowledge-fetcher.md`
* **Purpose:** Comprehensive documentation of Fetcher module for onboarding and reference
* **Status:** ✅ Done

## T-013: Test Infrastructure ✅
* **Created:**
  - `test_smoke.py` - Smoke test verification
  - `test_config_change.py` - Config change validation
  - `test_url_validation.py` - URL format testing
  - `test_apify_format.py` - Apify format verification
* **Status:** ✅ Done

---

# 6. CURRENT STATUS SUMMARY

## Completed Phases

### ✅ Phase 1: Bronze Layer (Setup & Config) - COMPLETE
- All tasks (T-001, T-002, T-003) completed
- Python environment, configs, and class scaffolding in place
- **Deliverables:** Virtual environment, config files, empty class structure

### ✅ Phase 2: Silver Layer (The Fetcher) - COMPLETE
- All tasks (T-004, T-005) completed
- Apify integration working with retry logic
- Configurable filtering implemented
- **Deliverables:** Working fetcher with smoke test mode, filtered review data

### Additional Work Completed
- Loop robustness (T-009) - Moved to Phase 3
- Config externalization (T-010)
- Bug fixes and improvements (T-011)
- Knowledge documentation (T-012)
- Test infrastructure (T-013)

## Completed Phases

### ✅ Phase 3: Gold Layer (The Analyzer) - COMPLETE
- **T-006:** Calc Logic - ✅ Done
- **T-007:** Score Risk - ✅ Done
- **T-009:** Loop Robustness - ✅ Done

**Implementation Details:**
- ✅ `load_pain_keywords()` - Loads pain_keywords.json with error handling
- ✅ `filter_by_date()` - Vectorized pandas date filtering (timezone-aware)
- ✅ `calculate_slope()` - np.polyfit for trend analysis with rollback (returns 0.0 if insufficient data)
- ✅ `calculate_keyword_density()` - Vectorized regex keyword matching across all categories
- ✅ `calculate_risk_score()` - Weighted formula from settings.json (slope_impact, volume_impact, category weights)
- ✅ `analyze()` - Full pipeline generating schema_app_gap.json with all metrics
- ✅ `save_analysis()` - Saves analysis results to JSON files

**Key Features:**
- Deterministic analysis using Pandas/NumPy (no LLM)
- Handles edge cases (insufficient data, missing fields)
- Version impact detection (broken update detection)
- Top pain categories sorted by impact
- Evidence extraction (sample negative reviews)

**Deliverables:** Working analyzer generating `schema_app_gap.json` files in `data/` folder

**T-009: Loop Robustness - COMPLETE**
- ✅ Improved error handling in main.py loop
- ✅ Progress tracking ([1/5], [2/5], etc.)
- ✅ Success/failure tracking and summary
- ✅ Continues processing even if individual apps fail
- ✅ Final summary shows all results

**Deliverables:** Robust batch processing capable of handling multiple apps with error recovery

## In Progress

### ⏳ Phase 4: Platinum Layer (The Reporter & Aggregator) - NOT STARTED
- **T-010:** Aggregate Leaderboard - ✅ Complete
- **T-008:** Gen Markdown - Ready to start (dependencies met)

## Pending

### ⏳ Phase 4: Platinum Layer (The Reporter & Aggregator) - IN PROGRESS
- **T-011:** Analyzer Calibration - 🔴 To Do (Critical math model fixes)
- **T-010:** Aggregate Leaderboard - ✅ Complete (Generates `data/market_leaderboard.md` with ranked comparison)
- **T-008:** Gen Markdown - Ready to start after T-011

---

# 7. NEXT STEPS & PRIORITIES

## Immediate Next Steps (Priority Order)

1. **T-011: Analyzer Calibration** 🔴 CRITICAL (BLOCKING T-010 & T-008)
   - **Why:** Three critical data anomalies invalidate current leaderboard rankings:
     - Risk Score inflation (no volume normalization): Opal reached 93.0 with inflated counts
     - Ghost Ratio (0.0% negative): Hardcoded to low-star reviews, ignores pain-keyword 5-stars
     - Flatline Slope (0.0000): np.polyfit receives zero qualifying reviews
   - **Dependencies:** ✅ T-009 (Loop Robustness complete)
   - **Estimated Effort:** 2-3 hours for fixes + 1 hour testing
   - **Key Tasks:**
     - Fix normalize formula in `calculate_risk_score()` (line 233)
     - Redefine negative_count to include pain-keyword matches (lines 310-312)
     - Recalculate slope using keyword density trend instead of low-star counts (lines 114-131)
   - **Blockers:** None - ready to start immediately
   - **Validation:** Regenerate leaderboard and verify metrics are in valid ranges

2. **T-010: Aggregate Leaderboard** ✅ Complete (Awaiting T-011 Validation)
   - **Status:** Already implemented, will need re-run after T-011 fixes
   - **Dependencies:** T-011 (math calibration)
   - **Output:** `data/market_leaderboard.md` with corrected rankings

3. **T-008: Generate Markdown Reports** 🟡 Medium Priority (Next after T-011)
   - **Why:** Final deliverable for end-to-end pipeline (individual app reports)
   - **Dependencies:** T-011 (corrected metrics), T-010 (leaderboard)
   - **Estimated Effort:** 2-3 hours

## Risks & Blockers

### CRITICAL ISSUE: Math Model Mismatch (T-011 Required)
- **Issue:** Three interconnected logic anomalies in `src/analyzer.py` invalidate current metrics
  1. **Score Inflation (Lines 228-233):** Risk scores unbounded due to lack of normalization
  2. **Ghost Ratio (Lines 310-312):** Negative ratio always 0.0% because definition excludes pain-keyword 5-stars
  3. **Flatline Slope (Lines 114-131):** Volatility always 0.0000 because polyfit receives zero qualifying reviews
- **Root Cause:** Semantic mismatch between fetcher (5-star + pain keywords) and analyzer (traditional 1-2 star negatives)
- **Blocker Status:** Blocks validation of T-010 output; must fix before T-008
- **Mitigation:** T-011 task created to systematically fix all three issues
- **Timeline Impact:** +1-2 hours to project timeline for fixes + validation

## Coordination Needed

- **None** - Single developer project, no external dependencies

---

# 8. PROGRESS METRICS

## Completion Status
- **Phase 1:** 100% (3/3 tasks) ✅
- **Phase 2:** 100% (2/2 tasks) ✅
- **Phase 3:** 100% (3/3 tasks) ✅
- **Phase 4:** 75% (3/4 tasks) 🟡 (T-011, T-012 & T-010 Complete, T-008 Pending)
- **Additional Work:** 100% (4/4 tasks) ✅

**Overall Progress:** 79% (19/24 tasks including additional work)

**Status:** T-012 (MECE Risk Scoring) complete - Pillar + Boost formula implemented, enhanced leaderboard with pillar insights

## Timeline Status
- **M1 (Bronze):** ✅ Complete (Day 1 target met)
- **M2 (Silver):** ✅ Complete (Day 1 target met)
- **M3 (Gold):** ✅ Complete (Day 2 target met)
- **M4 (Platinum):** ⏳ Pending (Day 2 target)

**Status:** Ahead of schedule! Phase 3 complete. Ready for Phase 4 (Report generation).