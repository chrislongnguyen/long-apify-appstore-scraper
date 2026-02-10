---
phase: planning
title: Execution Plan - App Volatility Analyzer
description: Step-by-step implementation matrix for the Python ETL pipeline (Fetcher -> Analyzer -> Reporter).
last_updated: 2026-02-10
---

# QUICK STATUS SUMMARY

**Current Phase:** Phase 5 (Refactoring & Optimization)  
**Overall Progress:** 100% (27/27 tasks)  
**Next Task:** None - All tasks complete  
**Status:** ✅ Phases 1-5 Complete

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

# 4. RESOURCE & BUDGET TRACKER
| Metric | Current Usage | Hard Limit | Status |
| :--- | :--- | :--- | :--- |
| **Financial Cost** | ~$0.05 | $5.00 | 🟢 Safe |
| **API Calls** | ~8 successful runs | N/A | 🟢 Safe |
| **Reviews Fetched** | ~300+ reviews | N/A | 🟢 Safe |

---

# 5. NEXT ACTIONS (Phase 5 Execution)

1.  **Execute T-016 (File Org):** Update `targets.json` and `main.py` to support `niche_name` subdirectories.
2.  **Execute T-017 (White Space):** Add the analysis logic to `Reporter`.
3.  **Execute T-018 (Migration):** tighten the Regex in `Intelligence`.
4.  **Execute T-019 (Tests):** Write the `pytest` suite.

---

# 6. PROGRESS METRICS

## Completion Status
- **Phase 1-3:** 100% ✅
- **Phase 4:** 100% ✅ (T-008 Complete)
- **Phase 5:** 100% ✅ (T-016 to T-019 Complete)

