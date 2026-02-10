---
phase: planning
title: Execution Plan - App Volatility Analyzer
description: Step-by-step implementation matrix for the Python ETL pipeline (Fetcher -> Analyzer -> Reporter).
last_updated: 2026-02-10
---

# QUICK STATUS SUMMARY

**Current Phase:** Phase 6 (Predictive Analytics)  
**Overall Progress:** Phases 1-5 Complete; Phase 6 Pending  
**Next Task:** T-020 (Fermi Estimator Module) — no deps  
**Status:** ✅ Phases 1-5 Complete → 🚧 Phase 6 at 0%

**Recent Achievements (2026-02-10):**
- ✅ T-016 to T-019: Niche dirs, White Space, Migration refinement, Forensic tests
- ✅ T-008 Forensic Intelligence: `src/intelligence.py` (ForensicAnalyzer) deployed
- ✅ Generated "Forensic Reports" (Timelines, N-Grams, Quotes) for Voice AI & Tattoo Niches
- ✅ Verified "Version Spike" detection (e.g., Tattoo AI Week 49)
- ✅ Validated "Tattoo AI" Niche (7 apps identified, high volatility confirmed)

---

# 1. MACRO ROADMAP (Timeline & Resources)

| Milestone | Target Date | Resource Budget (Est.) | Critical Risk |
| :--- | :--- | :--- | :--- |
| **M1: Bronze (The Skeleton)** | Day 1 | $0.00 | Environment & Config handling fails |
| **M2: Silver (The Fetcher)** | Day 1 | $0.20 (Apify) | API Schema changes or Rate Limits |
| **M3: Gold (The Brain)** | Day 2 | $0.00 (Local) | Math logic (Slope/Scoring) is incorrect |
| **M4: Platinum (The Story)** | Day 2 | $0.00 | Report is unreadable/cluttered |
| **M5: Diamond (The Polish)** | Day 3 | $0.00 | Code debt / File organization chaos |

---

# 2. EXECUTION MATRIX (The "Micro" View)

## PHASE 1: BRONZE LAYER (Setup & Config) ✅
| ID | Task (Verb) | Target Outcome (Adverb) | Risk Factor | Status |
| :--- | :--- | :--- | :--- | :--- |
| **T-001** | **Init Python Env** | *Cleanly* (Isolated Venv) | **Low (2)** | ✅ Done |
| **T-002** | **Create Configs** | *Explicitly* (JSON Schemas) | **Low (3)** | ✅ Done |
| **T-003** | **Scaffold Classes** | *Modularly* (Empty Classes) | **Low (1)** | ✅ Done |

## PHASE 2: SILVER LAYER (The Fetcher) ✅
| ID | Task (Verb) | Target Outcome (Adverb) | Risk Factor | Status |
| :--- | :--- | :--- | :--- | :--- |
| **T-004** | **Connect Apify** | *Reliably* (Tenacity Retry) | **Med (5)** | ✅ Done |
| **T-005** | **Filter & Save** | *Thriftily* (Drop 5-stars) | **Med (4)** | ✅ Done |
| **T-014** | **Multi-Region Support** | *Globally* (Country: "All") | **Med (4)** | ✅ Done |

## PHASE 3: GOLD LAYER (The Analyzer) ✅
| ID | Task (Verb) | Target Outcome (Adverb) | Risk Factor | Status |
| :--- | :--- | :--- | :--- | :--- |
| **T-006** | **Calc Logic** | *Deterministically* (Pandas) | **High (8)** | ✅ Done |
| **T-007** | **Score Risk** | *Accurately* (Formula Check) | **High (7)** | ✅ Done |
| **T-011** | **Analyzer Calibration** | *Fairly* (Normalize Scores) | **Med (3)** | ✅ Done |

## PHASE 4: PLATINUM LAYER (The Reporter) ✅
| ID | Task (Verb) | Target Outcome (Adverb) | Risk Factor | Status |
| :--- | :--- | :--- | :--- | :--- |
| **T-010** | **Aggregate Leaderboard** | *Holistically* (Ranking) | **Low (2)** | ✅ Done |
| **T-012** | **Metrics 2.0 (MECE)** | *Logically* (Pillars) | **Med (4)** | ✅ Done |
| **T-008** | **Forensic Intelligence** | *Visually* (Charts/Grams) | **High (6)** | ✅ Done |

## PHASE 5: DIAMOND LAYER (Refactoring & Polish) ✅
| ID | Task (Verb) | Target Outcome (Adverb) | Risk Factor | Status |
| :--- | :--- | :--- | :--- | :--- |
| **T-016** | **Niche Directories** | *Organizedly* (Subfolders) | **Low (1)** | ✅ Done |
| **T-017** | **White Space Analysis** | *Strategically* (Gap Finding) | **Med (3)** | ✅ Done |
| **T-018** | **Refine Migration** | *Accurately* (Strict Regex) | **Low (2)** | ✅ Done |
| **T-019** | **Forensic Unit Tests** | *Robustly* (Pytest) | **Med (3)** | ✅ Done |

## PHASE 6: PREDICTIVE ANALYTICS
| ID | Task (Verb) | Target Outcome (Adverb) | Risk Factor | Deps |
| :--- | :--- | :--- | :--- | :--- |
| **T-020** | **Fermi Estimator Module** | *Financially* (Implement src/analyzer.py logic for Fermi Math and Dynamic Multipliers) | **Med (5)** | None |
| **T-021** | **Trend Acceleration (Delta)** | *Mathematically* (Calculate Slope T1 vs T2 in Analyzer) | **Med (4)** | T-006 |
| **T-022** | **Named Spike Correlation** | *Narratively* (Update ForensicAnalyzer to link anomalies to app version metadata) | **Med (4)** | T-008 |
| **T-023** | **Whale Detector Logic** | *Surgically* (Implement the 40-word filter and domain-vocab multiplier) | **Low (2)** | T-006 |
| **T-024** | **Predictive Integration** | *Holistically* (Update main.py and Reporter to include the new metrics in Markdown/JSON outputs) | **Med (5)** | T-020, T-021, T-022, T-023 |

## PHASE 7: THE ARCHITECT (Generative & Prescriptive) — *DEFERRED / PLANNED*
| ID | Task (Verb) | Target Outcome (Adverb) | Risk Factor | Deps |
| :--- | :--- | :--- | :--- | :--- |
| **T-025** | **Integrate Reddit** | *Broadly* (Fetch Feature Requests) | **Med (5)** | None |
| **T-026** | **Build AI Client** | *Securely* (Gemini/OpenAI Wrapper) | **Med (4)** | None |
| **T-027** | **Gen Anti-Roadmap** | *Creatively* (LLM Prompt Engineering) | **High (8)** | T-025, T-026 |

---

# 3. DETAILED SPECIFICATIONS (Phase 5 Tasks)

### T-016: Dynamic Niche Directories (File Org)
* **User Story:** As a User, I want output files sorted by Niche (e.g., `data/Voice_AI/`) so I don't get overwhelmed by mixed files.
* **Requirements:**
    * Update `targets.json` schema to include root-level `niche_name`.
    * Refactor `main.py` to create `data/{niche_name}` and `reports/{niche_name}` if they don't exist.
    * Save all JSONs and Markdown reports into these subfolders.

### T-017: White Space Analysis (The "Opportunity" Section)
* **User Story:** As a Founder, I want the Niche Report to explicitly tell me if there is a "Low Risk, High Quality" gap in the market.
* **Logic:**
    * Iterate through the Forensic Matrix.
    * Identify apps where `Functional < 30` AND `Economic < 30`.
    * **Output:** Add a "🏳️ White Space Analysis" section to `report_NICHE.md`.
        * *Case A:* "Gap Found: [App Name] is the safe harbor."
        * *Case B:* "No Gap: All apps are risky (High Opportunity)."

### T-018: Migration Logic Refinement
* **User Story:** As a Data Scientist, I need to distinguish between "I came from X" (Past) and "I switched to X" (Churn) to avoid false positives.
* **Logic:**
    * Update `ForensicAnalyzer.map_competitor_migration`.
    * Use strict regex patterns: `(switched|moved|migrated|changed) to {app}`.
    * Ignore "better than {app}" (Comparison).

### T-019: Forensic Unit Tests
* **User Story:** As a Developer, I need to ensure the N-Gram and Timeline logic doesn't break during refactors.
* **Action:** Create `tests/test_forensic.py`.
    * Test `detect_event_timeline` with a mock spike (e.g., 50 reviews, 40 pain).
    * Test `extract_semantic_clusters` with a mock text corpus.
    * Ensure execution time for 500 mock reviews is < 2.0s.

---

## 3.1 Phase 6: Detailed Specifications (Predictive Analytics)

### T-020: Fermi Estimator Module

* **User Story:** As a Venture Architect, I want to quantify monthly revenue leakage from churn signals so I can prioritize high-value opportunities.

* **Fermi Formula:**
  $$Leakage = (Churn\_Reviews \times Multiplier) \times Price$$

* **Inputs:**
  * `Churn_Reviews`: Count of reviews with "Economic" or "Functional" pain pillars (from `schema_app_gap.top_pain_categories`).
  * `Price`: From `targets.json` (app.price) or default $9.99.
  * `Multiplier`: Dynamic ratio from `targets.json` (niche_category): B2B=50, Consumer=100, Games=200+.

* **Output:** `Monthly_Leakage_USD` (float) — add to `schema_app_gap.signals` or forensic intelligence JSON.

* **Acceptance Criteria:**
  * Logic implemented in `src/analyzer.py`.
  * Multiplier configurable via `targets.json`.

### T-021: Trend Acceleration (Delta)

* **User Story:** As a Founder, I want to know if competitor decline is accelerating or stabilizing.

* **Logic:**
  * **Slope_T1:** Linear regression (Last 4 weeks) of negative review volume vs time.
  * **Slope_T2:** Linear regression (Weeks 5–8) of negative review volume vs time.
  * **Δm:** Slope_T1 − Slope_T2.

* **Output:** Δm value + insight string: "Acceleration Detected: +15% week-over-week" or "Stabilizing: -8% week-over-week."

* **Acceptance Criteria:**
  * Implemented in `src/analyzer.py`.
  * Output included in `schema_app_gap.metrics` or `signals`.

### T-022: Named Spike Correlation

* **User Story:** As a Founder, I want anomaly weeks linked to specific app versions so I can create marketing headlines (e.g., "The Version 4.2 Crash").

* **Correlation Logic:**
  * **Input:** Week_Anomaly (PainDensity > μ + 2σ) + `reviews_df` with `version` metadata.
  * **Logic:** Correlate anomaly week with version strings present in that week's reviews. Assign narrative label.
  * **Fallback:** If no version data, use dominant topic cluster from N-Grams.

* **Output:** `{week: "2023-42", label: "The Version 4.2 Crash", version: "4.2"}` — append to `reports/{niche}/{app}_intelligence.json` timeline events.

* **Acceptance Criteria:**
  * Update `ForensicAnalyzer` with `name_spike(anomaly_week, reviews_df)` method.
  * Named spikes appear in forensic intelligence JSON and report Markdown.

### T-023: Whale Detector Logic

* **User Story:** As a Product Detective, I want high-value reviews (long, domain-specific) weighted more heavily for opportunity signals.

* **Logic:**
  * **Filter:** Reviews with length > 40 words OR domain vocabulary match.
  * **Multiplier:** 3x–5x weight for evidence prioritization.

* **Acceptance Criteria:**
  * Implement 40-word filter and domain-vocab heuristic.
  * Whale-boosted evidence used in evidence ranking and future Architect prompts.

### T-024: Predictive Integration

* **User Story:** As a User, I want all new Predictive metrics (Fermi, Δm, Named Spikes) visible in reports and JSON outputs.

* **Requirements:**
  * Update `main.py` to invoke FermiEstimator, SlopeDeltaCalculator, and pass Named Spikes to Reporter.
  * Update `Reporter` to include Δm, Monthly_Leakage_USD, and Named Spike labels in Markdown reports.
  * Ensure `schema_app_gap` and forensic intelligence JSON include all new fields.

* **Acceptance Criteria:**
  * Individual and Niche reports show new metrics.
  * JSON artifacts are schema-complete.

---

## 3.2 Phase 7: The Architect (Deferred / Planned)

### T-025: Integrate Reddit
* **User Story:** As a Venture Architect, I want Feature Requests and Alternatives from Reddit to complement App Store pain signals.
* **Action:** Create `src/fetcher_reddit.py`; adapter for `apify/reddit-scraper`. Subreddit derived from `niche_name`.

### T-026: Build AI Client
* **User Story:** As a Developer, I need a secure LLM wrapper for text synthesis (User Stories only).
* **Action:** Create `src/ai_client.py`; Gemini/OpenAI wrapper. Config-driven via `settings.json` or env vars.

### T-027: Generate Anti-Roadmap (Invert Pain → User Stories)

* **User Story:** As a Venture Architect, I want pain clusters from App Store reviews (and Reddit) inverted into actionable User Stories so I can build a prioritized MVP roadmap without bias.

* **Prompt Strategy:**

1. **Input Context Assembly:**
   * **Negative Clusters:** `top_pain_categories` from `schema_app_gap` (e.g., "critical", "scam_financial", "subscription").
   * **N-Gram Phrases:** `extract_semantic_clusters` output (e.g., "sync failed", "premium locked").
   * **Reddit Feature Requests:** Titles and body of "Feature Requests" / "Alternatives" threads from `apify/reddit-scraper`.
   * **Whale Evidence:** Quotes from reviews with length > 40 words or domain vocabulary (3x-5x weighted).

2. **Inversion Rule (Prompt Template):**
   * **Rule:** For each pain cluster, ask the LLM to output *exactly one* User Story in the format: *"As a [User], I want [Feature] so that [Benefit]."*
   * **Example:** Pain Cluster `"Crash on Export"` → *"As a Pro User, I want 4K video export to complete reliably so that I can deliver client work without data loss."*
   * **Constraint:** Do not invent features not implied by the pain cluster. Stay grounded in the source evidence.

3. **Output Format:**
   * **Artifact:** `reports/{niche_name}/roadmap_mvp.md`
   * **Structure:**
     * Executive Summary (1–2 sentences: niche focus, high-priority gaps).
     * Prioritized User Stories (ranked by evidence volume + Whale multiplier).
     * Revenue Leakage Estimate (if available from T-020).
     * Reddit-Informed Additions (feature requests from Reddit not in App Store data).

4. **LLM Provider:** Gemini (primary) or OpenAI (fallback). Use `ai_client.py` wrapper; no math/stats in LLM.

5. **Acceptance Criteria:**
   * At least 3 User Stories per niche from pain clusters.
   * Each User Story must be traceable to at least one pain cluster or N-Gram phrase.
   * Reddit data must be explicitly labeled when used as source.

---

# 4. RESOURCE & BUDGET TRACKER
| Metric | Current Usage | Hard Limit | Status |
| :--- | :--- | :--- | :--- |
| **Financial Cost (Apify)** | ~$0.05 | $5.00 | 🟢 Safe |
| **LLM API Costs** | TBD (Phase 7) | $5.00 | ⏳ Placeholder |
| **API Calls** | ~8 successful runs | N/A | 🟢 Safe |
| **Reviews Fetched** | ~300+ reviews | N/A | 🟢 Safe |

---

# 5. NEXT ACTIONS (Phase 6 Execution)

1.  **Execute T-020 (Fermi Estimator Module):** Implement Fermi formula and dynamic multipliers in `src/analyzer.py`.
2.  **Execute T-021 (Trend Acceleration):** Add SlopeDeltaCalculator (Slope T1 vs T2) in Analyzer.
3.  **Execute T-022 (Named Spike Correlation):** Update ForensicAnalyzer with `name_spike()` to link anomalies to version metadata.
4.  **Execute T-023 (Whale Detector Logic):** Implement 40-word filter and domain-vocab multiplier.
5.  **Execute T-024 (Predictive Integration):** Wire new metrics into main.py and Reporter; update Markdown/JSON outputs.

---

# 6. PROGRESS METRICS

## Completion Status
- **Phase 1-3:** 100% ✅
- **Phase 4:** 100% ✅ (T-008 Complete)
- **Phase 5:** 100% ✅ (T-016 to T-019 Complete)
- **Phase 6 (Predictive Analytics):** 0% 🚧 (T-020 to T-024 pending)
- **Phase 7 (The Architect):** Deferred / Planned (T-025 to T-027)

