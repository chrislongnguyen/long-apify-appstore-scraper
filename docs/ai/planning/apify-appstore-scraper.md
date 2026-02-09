---
phase: planning
title: Execution Plan - App Volatility Analyzer
description: Step-by-step implementation matrix for the Python ETL pipeline (Fetcher -> Analyzer -> Reporter).
---

# 1. MACRO ROADMAP (Timeline & Resources)

| Milestone | Target Date | Resource Budget (Est.) | Critical Risk |
| :--- | :--- | :--- | :--- |
| **M1: Bronze (The Skeleton)** | Day 1 | $0.00 | Environment & Config handling fails |
| **M2: Silver (The Fetcher)** | Day 1 | $0.20 (Apify) | API Schema changes or Rate Limits |
| **M3: Gold (The Brain)** | Day 2 | $0.00 (Local) | Math logic (Slope/Scoring) is incorrect |
| **M4: Platinum (The Story)** | Day 2 | $0.00 | Report is unreadable/cluttered |

---

# 2. EXECUTION MATRIX (The "Micro" View)

* **Risk Factor:** (Impact 1-10) $\times$ (Prob 0.0 - 1.0). **>6 = Critical.**
* **Outcome:** The specific "Adverb" (Sustainability/Efficiency) we are optimizing for.

## PHASE 1: BRONZE LAYER (Setup & Config)
| ID | Task (Verb) | Target Outcome (Adverb) | Risk Factor | Deps/Blockers | Status |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **T-001** | **Init Python Env** | *Cleanly* (Isolated Venv) | **Low (2)** | None | 🔴 To Do |
| **T-002** | **Create Configs** | *Explicitly* (JSON Schemas) | **Low (3)** <br> *(Imp:6, Prob:0.5)* | T-001 | 🔴 To Do |
| **T-003** | **Scaffold Classes** | *Modularly* (Empty Classes) | **Low (1)** | T-002 | 🔴 To Do |

## PHASE 2: SILVER LAYER (The Fetcher)
| ID | Task (Verb) | Target Outcome (Adverb) | Risk Factor | Deps/Blockers | Status |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **T-004** | **Connect Apify** | *Reliably* (Tenacity Retry) | **Med (5)** <br> *(Imp:10, Prob:0.5)* | T-003 | 🔴 To Do |
| **T-005** | **Filter & Save** | *Thriftily* (Drop 5-stars) | **Med (4)** | T-004 | 🔴 To Do |

## PHASE 3: GOLD LAYER (The Analyzer - Critical)
| ID | Task (Verb) | Target Outcome (Adverb) | Risk Factor | Deps/Blockers | Status |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **T-006** | **Calc Logic** | *Deterministically* (Pandas) | **High (8)** <br> *(Imp:10, Prob:0.8)* | T-005 | 🔴 To Do |
| **T-007** | **Score Risk** | *Accurately* (Formula Check) | **High (7)** | T-006 | 🔴 To Do |

## PHASE 4: PLATINUM LAYER (The Reporter)
| ID | Task (Verb) | Target Outcome (Adverb) | Risk Factor | Deps/Blockers | Status |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **T-008** | **Gen Markdown** | *Legibly* (Storytelling) | **Low (2)** | T-007 | 🔴 To Do |

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

---

# 4. RESOURCE & BUDGET TRACKER
| Metric | Current Usage | Hard Limit | Status |
| :--- | :--- | :--- | :--- |
| **Financial Cost** | $0.00 | $5.00 | 🟢 Safe |
| **API Calls** | 0 | N/A | 🟢 Safe |