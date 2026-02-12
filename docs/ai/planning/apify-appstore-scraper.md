---
phase: planning
title: Execution Plan - App Volatility Analyzer
description: Step-by-step implementation matrix for the Python ETL pipeline (Fetcher -> Analyzer -> Reporter -> Venture Architect).
last_updated: 2026-02-11
---

# QUICK STATUS SUMMARY

**Current Phase:** Phase 7 — The Venture Architect  
**Current Sprint:** Phase 7.2 (Orchestration)  
**Overall Progress:** Phases 1-6 Complete; T-031 Done; Phase 7.1–7.2 Complete  
**Next Task:** T-028 (Success Signal) or T-029 (Context Mocking)  
**Status:** ✅ T-031 Done — Learna_English Risk Score 2.74 → 60.0 (Severity-First validated)

**Recent Achievements (2026-02-11):**
- ✅ Phase 6 Complete: T-020 to T-024 (Fermi, SlopeDelta, Named Spikes, Whale Detector, Reporter Integration)
- ✅ Ran ViralApps niche (5 apps): Revenue Leakage, Momentum labels, Financial Impact in reports
- ✅ Design doc updated with full Phase 7 architecture (3-stage LLM pipeline, 7-Node System Dynamics)
- ✅ Requirements doc updated with "5-Layer Root Cause Analysis" and "EPS Generator" specs
- 🚧 Phase 7 design approved — entering execution

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

## PHASE 6: PREDICTIVE ANALYTICS ✅
| ID | Task (Verb) | Target Outcome (Adverb) | Risk Factor | Status |
| :--- | :--- | :--- | :--- | :--- |
| **T-020** | **Fermi Estimator Module** | *Financially* (Fermi Math & Dynamic Multipliers in Analyzer) | **Med (5)** | ✅ Done |
| **T-021** | **Trend Acceleration (Delta)** | *Mathematically* (Slope T1 vs T2 in Analyzer) | **Med (4)** | ✅ Done |
| **T-022** | **Named Spike Correlation** | *Narratively* (Link anomalies to version metadata) | **Med (4)** | ✅ Done |
| **T-023** | **Whale Detector Logic** | *Surgically* (40-word filter + domain-vocab multiplier) | **Low (2)** | ✅ Done |
| **T-024** | **Predictive Integration** | *Holistically* (New metrics in main.py, Reporter, JSON) | **Med (5)** | ✅ Done |
| **T-031** | **Risk Score Recalibration** | *Severity-First* (Fix false negative: scam/crash signals override improving trend) | **High (7)** | ✅ Done |

## PHASE 7: THE VENTURE ARCHITECT 🚧

**Strategy:** Split into 3 Sub-Phases to manage complexity and risk.  
**Current Sprint:** Phase 7.1 + 7.2 (parallel where possible)

### Phase 7.1: Core Intelligence (Logic Layer) — MUST HAVE
*Goal: Generate the System Map and EPS Prescription from internal review data.*

| ID | Task (Verb) | Target Outcome (Adverb) | Risk Factor | Deps | Status |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **T-025** | **Build AI Client & Schemas** | *Strictly* (Gemini wrapper + Pydantic models for 7-Node output) | **Med (5)** | None | ✅ Done |
| **T-026** | **Venture Architect Module** | *Systematically* (3-stage pipeline: ICP → SysMap → EPS) | **High (8)** | T-025 | ✅ Done |
| **T-027** | **Blueprint Reporter & Template** | *Beautifully* (Jinja2 template → venture_blueprint.md) | **Med (4)** | T-026 | ✅ Done |

### Phase 7.2: Orchestration & Data Plumbing — MUST HAVE
*Goal: Connect the Scraper pipeline to the Architect.*

| ID | Task (Verb) | Target Outcome (Adverb) | Risk Factor | Deps | Status |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **T-028** | **Success Signal Integration** | *Completely* (Pass raw reviews incl. 5★ to Architect) | **Low (2)** | T-026 | ⏳ Blocked |
| **T-029** | **Context Mocking & Graceful Degradation** | *Resiliently* (Run without Reddit; mock Context Signal for testing) | **Low (3)** | T-026 | ⏳ Blocked |

### Phase 7.3: Context Layer (Reddit) — SHOULD HAVE
*Goal: Add external validation signal from Reddit.*

| ID | Task (Verb) | Target Outcome (Adverb) | Risk Factor | Deps | Status |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **T-030** | **Reddit Scraper Integration** | *Broadly* (Fetch threads, wire into ICP construction) | **Med (5)** | T-028, T-029 | ⏳ Blocked |

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

### T-031: Risk Score Recalibration — Severity-First Model ✅ Done

* **User Story:** As a Founder, I need the Risk Score to never hide critical severity (Scams, Crashes) behind an "improving" trend. A negative slope must not erase red flags.
* **Problem:** Smoke test (Learna_English) — Economic density 21.6%, slope -3 → Risk 2.74 (false negative). Scam/deceptive-pricing signals were suppressed.
* **File:** `src/analyzer.py` — rewrite `calculate_risk_score`
* **Formula (Severity-First):**
  * `Risk = min(100.0, max(CalculatedRisk, CriticalFloor))`
  * **BaseScore:** `(Functional×200) + (Economic×250) + (Experience×150)` — Economic weighted 2.5× vs UI
  * **SlopeMultiplier:** If slope>0: `min(2.0, 1.0+slope)`; If slope≤0: `max(0.5, 1.0+(slope×0.1))` — dampen improvement, never erase
  * **CriticalFloor:** Economic>0.1 → 60; Functional>0.15 → 50; else 0
* **Reporter:** Updated `_generate_leaderboard_markdown` — "Layman's Terms" explanation; Critical Floor note.
* **Acceptance Criteria:** ✅ Learna_English Risk Score 2.74 → 60.0 (validated).

---

## 3.2 Phase 7: The Venture Architect (Execution Specs)

### T-025: Build AI Client & Pydantic Schemas (Phase 7.1.1)

* **User Story:** As a Developer, I need a reliable LLM wrapper that forces structured JSON output so the Venture Architect pipeline never saves garbage.
* **Sub-Phase:** 7.1 — Core Intelligence (MUST HAVE)
* **Priority:** CRITICAL PATH — hard blocker for T-026.

* **File:** `src/ai_client.py`

* **Implementation Steps:**
  1. Create `AIClient` class with `generate_structured(system_prompt, user_prompt, response_schema, temperature, max_tokens)`.
  2. **Primary Provider:** Gemini (`google-generativeai` SDK, model `gemini-2.0-flash`).
  3. **Fallback Provider:** OpenAI (`openai` SDK) — config-driven via `settings.json`.
  4. **Structured Output:** Use Gemini's JSON mode (`response_mime_type="application/json"`) to force valid JSON.
  5. **Retry Logic:** Wrap API call in `tenacity` (3 attempts, exponential backoff). If JSON parsing fails after retries, raise `ValueError` loudly.
  6. **`_parse_json_response(raw_text)`:** Strip markdown fences (````json ... ````), parse via `json.loads`, validate against schema.
  7. **Env Vars:** `GEMINI_API_KEY` (loaded via `dotenv`), `OPENAI_API_KEY` (optional).

* **Pydantic Models (strict schemas):**
  Create in `src/schemas.py` (or inline in `venture_architect.py`):

  ```python
  from pydantic import BaseModel, Field
  from typing import List, Optional

  class ICPSegment(BaseModel):
      primary: str
      secondary: str
      whale_segment: str

  class PainSuccessParadox(BaseModel):
      pain_says: str
      success_says: str
      inference: str

  class HolographicICP(BaseModel):
      who: dict              # {demographic, psychographic}
      why_udo: str           # Ultimate Desired Outcome
      what_how_workflow: List[str]
      when_trigger: str
      alternatives: List[str]
      icp_segment: ICPSegment
      pain_success_paradox: PainSuccessParadox

  class SystemNode(BaseModel):
      label: str
      evidence: List[str]
      layer: str
      note: Optional[str] = None

  class UDO(BaseModel):
      statement: str
      adverb: str
      noun: str

  class SystemDynamicsMap(BaseModel):
      udo: UDO
      uds: SystemNode
      uds_ud: SystemNode
      uds_ub: SystemNode
      ubs: SystemNode
      ubs_ud: SystemNode
      ubs_ub: SystemNode
      incumbent_failure: str
      depth_layers: dict     # {layer_1_app, layer_2_behavior, ..., layer_5_biology}

  class Principle(BaseModel):
      id: str
      name: str
      strategy: str          # e.g., "Amplify UDS.UD"
      node_ref: str          # e.g., "uds_ud"
      rationale: str

  class EPSPrescription(BaseModel):
      principles: List[Principle]
      environment: dict      # {form_factor, rationale, anti_pattern}
      tools: dict            # {desirable_wrapper, effective_core}
      sop: List[dict]        # [{step, actor, action}]
      trojan_horse: dict     # {level_1_desirable, level_5_effective}
      strategic_inversion_table: List[dict]
  ```

* **Acceptance Criteria:**
  * `AIClient.generate_structured()` returns valid Python dict.
  * Invalid JSON from LLM raises `ValueError` after 2 retries (fail loud).
  * Pydantic models validate all three stage outputs; `ValidationError` on schema mismatch.
  * Unit test: mock LLM response, assert Pydantic parse succeeds.

* **New Dependencies:** `google-generativeai>=0.5.0`, `pydantic>=2.0.0` (add to `requirements.txt`).

---

### T-026: Venture Architect Module — Core (Phase 7.1.2)

* **User Story:** As a Venture Architect, I want a 3-stage inference engine that maps User Psychology → System Dynamics → Strategic Principles so I can build a product that solves root causes, not symptoms.
* **Sub-Phase:** 7.1 — Core Intelligence (MUST HAVE)
* **Priority:** HIGH — depends on T-025 (AI Client).

* **File:** `src/venture_architect.py`

* **Class:** `VentureArchitect`

* **Implementation Steps:**

  **Stage 1 — `construct_holographic_icp(pain_reviews, success_reviews, reddit_data, analysis, app_name)`:**
  1. Extract top 10 Pain quotes from `pain_reviews` (prioritize Whales: > 40 words).
  2. Extract top 10 Success quotes from `success_reviews` (5★, > 30 words).
  3. Summarize Reddit themes (if available; empty list if not — see T-029).
  4. Assemble user prompt: Pain quotes + Success quotes + Reddit summary + `analysis.signals` summary.
  5. Call `ai_client.generate_structured(ICP_SYSTEM_PROMPT, user_prompt)`.
  6. Validate response against `HolographicICP` Pydantic model.
  7. Return validated ICP dict.

  **Stage 2 — `map_system_dynamics(icp, pain_reviews, success_reviews, analysis, app_name)`:**
  1. Curate top 15 evidence quotes (mixed Pain + Success, Whale priority).
  2. Assemble user prompt: Full ICP JSON + curated evidence + `analysis.metrics`.
  3. Call `ai_client.generate_structured(SYSTEM_DYNAMICS_PROMPT, user_prompt)`.
  4. Validate response against `SystemDynamicsMap` Pydantic model.
  5. **Depth Validation:** Assert `uds_ud.layer` and `ubs_ud.layer` contain "Layer 5" or "Biology". If not, log warning (LLM stopped too shallow).
  6. Return validated System Map dict.

  **Stage 3 — `generate_eps_prescription(system_map, icp, app_name)`:**
  1. Assemble user prompt: Full ICP JSON + Full System Map JSON.
  2. Call `ai_client.generate_structured(EPS_SYSTEM_PROMPT, user_prompt)`.
  3. Validate response against `EPSPrescription` Pydantic model.
  4. **Inversion Validation:** Assert `len(principles) >= 4` (one per UDS.UD, UDS.UB, UBS.UD, UBS.UB). Log warning if fewer.
  5. Return validated EPS dict.

  **Orchestrator — `generate_blueprint(app_name, raw_reviews, filtered_reviews, analysis, reddit_data, output_dir)`:**
  1. `_extract_pain_reviews(filtered_reviews)` → rating ≤ 2.
  2. `_extract_success_reviews(raw_reviews)` → rating = 5, word count > 30.
  3. Run Stage 1 → `icp`.
  4. Run Stage 2 → `system_map`.
  5. Run Stage 3 → `eps`.
  6. Save `{app}_system_map.json` (all three stage outputs).
  7. Render `venture_blueprint_{app}.md` (via Reporter — see T-027).
  8. Return `(blueprint_path, system_map_json_path)`.

* **System Prompts:** Defined in design doc §4.6 (ICP, SysMap, EPS). Store as constants in `venture_architect.py`.

* **Risk Mitigation — Token Budget:**
  * Evidence is capped at ~3000 tokens per stage via `_curate_evidence(reviews, max_quotes=10)`.
  * Implement a "Cluster Summarizer" step: if > 200 reviews, group by pain category first, then select top quote per category. Prevents feeding 1000 raw reviews to the LLM.

* **Acceptance Criteria:**
  * All 3 stages produce Pydantic-valid output for a real niche (e.g., Fasting_Trackers).
  * System Map reaches Layer 5 (Biology) for at least `uds_ud` and `ubs_ud`.
  * EPS Principles map 1:1 to system nodes (back-reference check).
  * End-to-end: `generate_blueprint()` produces both `.json` and `.md` artifacts.
  * Smoke test: Run on 1 app with `--venture-architect --smoke-test`.

---

### T-027: Blueprint Reporter & Jinja2 Template (Phase 7.1.3)

* **User Story:** As a Founder, I want the Venture Blueprint rendered as a beautiful, readable Markdown Strategy Doc so I can share it with co-founders and investors.
* **Sub-Phase:** 7.1 — Core Intelligence (MUST HAVE)
* **Priority:** MEDIUM — depends on T-026 (needs JSON structure to render).

* **Implementation Steps:**
  1. **Create `templates/venture_blueprint.j2`:** Jinja2 template that renders the 4-section Markdown:
     * Section 1: The System Map (UDO, Driving Forces table, Blocking Forces table, Incumbent Failure).
     * Section 2: The Strategic Inversion (table: Incumbent Method → Root Cause → New Principle).
     * Section 3: The EPS Prescription (Environment, Principles list, Tools, SOP steps).
     * Section 4: The Trojan Horse (Level 1 vs Level 5).
  2. **Update `src/reporter.py`:** Add `render_venture_blueprint(app_name, icp, system_map, eps, output_dir)` method.
     * Uses `jinja2.Environment` to load and render template.
     * Output: `reports/{niche_name}/venture_blueprint_{app_safe_name}.md`.
  3. **Alternative (if Jinja2 is overkill):** Use f-string builder in Reporter. Decision: Jinja2 preferred for maintainability.

* **New Dependency:** `jinja2>=3.1.0` (add to `requirements.txt`).

* **Acceptance Criteria:**
  * Template renders valid Markdown with tables, bold headers, block quotes.
  * No raw JSON visible in output — everything is human-readable.
  * Verified: Open in VS Code preview → clean formatting.

---

### T-028: Success Signal Integration (Phase 7.2.1)

* **User Story:** As a Developer, I need the pipeline to pass all raw reviews (including 5★) to the Venture Architect so it can extract the Success Signal.
* **Sub-Phase:** 7.2 — Orchestration (MUST HAVE)
* **Priority:** MEDIUM — depends on T-026.

* **Implementation Steps:**
  1. **Verify `main.py` data flow:** Confirm `reviews` (pre-filter) is available in the processing loop. (Already true — `reviews = fetcher.fetch_reviews(...)` exists before `filtered_reviews = fetcher.filter_reviews(reviews)`.)
  2. **Add CLI flag `--venture-architect`:** `parser.add_argument("--venture-architect", action="store_true")`.
  3. **Add Phase 7 block in `main.py`:** After existing Phase 4-6 processing, invoke `VentureArchitect.generate_blueprint(raw_reviews=reviews, ...)`.
  4. **Component initialization:** Import `AIClient`, `RedditFetcher`, `VentureArchitect` conditionally (only when `--venture-architect` is set).
  5. **Reddit cache:** Fetch Reddit data once per niche (not per app). Store in `reddit_cache` variable.

* **Key Design Decision:** `raw_reviews` (the unfiltered list) is passed to `VentureArchitect`. The Architect internally calls `_extract_success_reviews()` to filter 5★ whales. **No changes to `Fetcher` class required.**

* **Acceptance Criteria:**
  * `python main.py --venture-architect --smoke-test` runs full pipeline (Phases 1-7) for first app.
  * Without `--venture-architect` flag, pipeline behaves identically to current (zero LLM cost).
  * Success reviews are logged: "✓ Extracted X success signal reviews (5★, >30 words)".

---

### T-029: Context Mocking & Graceful Degradation (Phase 7.2.2)

* **User Story:** As a Developer, I need the Venture Architect to work with App Store data alone when Reddit data is unavailable, so I can test the core logic without the Reddit scraper.
* **Sub-Phase:** 7.2 — Orchestration (MUST HAVE)
* **Priority:** MEDIUM — risk mitigation for T-030.

* **Implementation Steps:**
  1. **Graceful empty:** `VentureArchitect.generate_blueprint()` accepts `reddit_data=[]` (empty list).
  2. **Prompt adaptation:** When `reddit_data` is empty, the ICP system prompt omits the "Context Signal" section and adds: "Note: No Reddit data available. Infer context from review text only."
  3. **Mock fixture (for testing):** Create `tests/fixtures/mock_reddit_fasting.json` with 5-10 sample Reddit posts to test Context Signal integration without Apify calls.
  4. **Logging:** When Reddit data is missing, log: "⚠ No Reddit data — running Architect on App Store signals only."

* **Acceptance Criteria:**
  * Full pipeline runs successfully with `reddit_data=[]`.
  * Output quality is acceptable (ICP + SysMap + EPS generated) even without Reddit.
  * When mock Reddit data is provided, it appears in ICP output under `alternatives` and `when_trigger`.

---

### T-030: Reddit Scraper Integration (Phase 7.3.1)

* **User Story:** As a Venture Architect, I want real Reddit threads about the niche to provide the "Context Signal" — how users talk about the problem outside the App Store.
* **Sub-Phase:** 7.3 — Context Layer (SHOULD HAVE)
* **Priority:** NICE-TO-HAVE — enhances quality but not blocking.

* **File:** `src/fetcher_reddit.py`

* **Implementation Steps:**
  1. **Create `RedditFetcher` class:** Wrapper for Apify `apify/reddit-scraper` actor.
     * `fetch_threads(subreddits, search_queries, max_posts=50, sort="relevance")` → `List[Dict]`.
     * `extract_context_themes(threads)` → `Dict` with `alternatives_mentioned`, `user_workflows`, `pain_contexts`.
  2. **Update `config/targets.json` schema:** Add optional `venture_architect` block with `subreddits` and `search_queries` arrays.
  3. **Wire into `main.py`:** Before the per-app loop, fetch Reddit data once and cache. Pass to `VentureArchitect.generate_blueprint()`.
  4. **Update `config_validator.py`:** Validate `venture_architect` block (optional, skip if missing).

* **Acceptance Criteria:**
  * Reddit threads fetched for configured subreddits.
  * `extract_context_themes()` identifies at least 2 competitor alternatives from Reddit text.
  * Cost: < $0.05 per Reddit fetch (monitor Apify usage).

---

### Risk Register (Phase 7)

| # | Risk | Impact | Likelihood | Mitigation | Owner |
| :--- | :--- | :--- | :--- | :--- | :--- |
| R1 | **LLM Hallucination** — System Map contains invented evidence | High | Medium | Strict Pydantic schemas (T-025). Fail loud on validation error. Every node must cite an evidence quote. | T-025, T-026 |
| R2 | **Token Cost Overrun** — 1000 reviews → huge prompt | Medium | Medium | "Cluster Summarizer" in T-026: group by category, select top quote per category. Cap at ~3000 tokens/stage. | T-026 |
| R3 | **Shallow Analysis** — LLM stops at Layer 3 (System) instead of Layer 5 (Biology) | Medium | High | Depth Validation in T-026: assert `uds_ud.layer` contains "Layer 5". Re-prompt once if shallow. | T-026 |
| R4 | **Reddit Scraper Delay** — Actor rate-limited or schema changes | Low | Medium | T-029 graceful degradation: Architect works without Reddit. Reddit is SHOULD HAVE, not blocker. | T-029, T-030 |
| R5 | **API Key Exposure** — Gemini key committed to git | High | Low | `.env` in `.gitignore` (already). `ai_client.py` loads via `os.getenv()` / `dotenv`. | T-025 |

### Dependency Graph

```
T-025 (AI Client + Schemas) ←── HARD BLOCKER
  │
  ├── T-026 (Venture Architect Core)
  │     │
  │     ├── T-027 (Blueprint Reporter)
  │     ├── T-028 (Success Signal Integration / main.py wiring)
  │     └── T-029 (Context Mocking / Graceful Degradation)
  │           │
  │           └── T-030 (Reddit Scraper) ←── SHOULD HAVE, not blocking
  │
  └── (No other deps — T-025 can start immediately)
```

---

# 4. RESOURCE & BUDGET TRACKER
| Metric | Current Usage | Hard Limit | Status |
| :--- | :--- | :--- | :--- |
| **Financial Cost (Apify)** | ~$0.30 | $5.00 | 🟢 Safe |
| **LLM API Costs (Phase 7)** | $0.00 (not started) | $5.00 | ⏳ Est. ~$0.003/app (Gemini Flash) |
| **API Calls** | ~15+ successful runs | N/A | 🟢 Safe |
| **Reviews Fetched** | ~2500+ reviews | N/A | 🟢 Safe |
| **Niches Analyzed** | 4 (Voice AI, Tattoo AI, Fasting Trackers, ViralApps) | N/A | 🟢 |

**Phase 7 Cost Estimate:**
* Gemini 2.0 Flash: ~$0.001/call × 3 stages/app × 5 apps/niche = **~$0.015/niche**.
* Reddit Scraper (T-030): ~$0.05/niche.
* **Total per niche:** ~$0.07. Well within $5.00 limit.

---

# 5. NEXT ACTIONS (Phase 7 Sprint)

### Immediate (Phase 7.1 + 7.2 — This Sprint)

1.  **T-025 (AI Client & Schemas):** Create `src/ai_client.py` + Pydantic models. This is the **hard blocker** — build first.
    * Add `google-generativeai`, `pydantic` to `requirements.txt`.
    * Unit test with mock LLM response.

2.  **T-026 (Venture Architect Core):** Create `src/venture_architect.py` with 3-stage pipeline.
    * Implement `construct_holographic_icp()`, `map_system_dynamics()`, `generate_eps_prescription()`.
    * Implement `_curate_evidence()` cluster summarizer (token budget control).
    * Smoke test on Fasting_Trackers niche.

3.  **T-027 (Blueprint Reporter):** ✅ Completed — Jinja2 template + `Reporter.render_venture_blueprint()` implemented.
    * Added `jinja2` to `requirements.txt`.
    * Verified generated Markdown blueprint artifacts render correctly.

4.  **T-028 (Success Signal Integration):** Add `--venture-architect` CLI flag to `main.py`. Wire orchestration.

5.  **T-029 (Context Mocking):** Ensure pipeline works with `reddit_data=[]`. Create mock fixture.

### Deferred (Phase 7.3 — Next Sprint)

6.  **T-030 (Reddit Scraper):** Create `src/fetcher_reddit.py`. Wire Reddit → ICP. Update `targets.json` schema.

### Suggested Execution Order

```
Day 1:  T-025 (AI Client)  →  T-026 Stage 1 (ICP)
Day 2:  T-026 Stage 2+3 (SysMap + EPS)  →  T-029 (Graceful Degradation)
Day 3:  T-027 (Template)  →  T-028 (main.py wiring)  →  Smoke Test
Day 4:  T-030 (Reddit — if time permits)
```

---

# 6. PROGRESS METRICS

## Completion Status
- **Phase 1-3:** 100% ✅
- **Phase 4:** 100% ✅ (T-008 Complete)
- **Phase 5:** 100% ✅ (T-016 to T-019 Complete)
- **Phase 6 (Predictive Analytics):** 100% ✅ (T-020 to T-024, T-031 Severity-First Complete)
- **Phase 7.1 (Core Intelligence):** 100% ✅ (T-025 ✅, T-026 ✅, T-027 ✅)
- **Phase 7.2 (Orchestration):** 0% 🚧 (T-028, T-029 pending)
- **Phase 7.3 (Context Layer):** 0% ⏳ (T-030 — SHOULD HAVE, deferred to next sprint)

## Module Inventory
| Module | Phase | Status |
| :--- | :--- | :--- |
| `src/fetcher.py` | Phase 2 | ✅ Production |
| `src/analyzer.py` | Phase 3 + 6 | ✅ Production (incl. Fermi, SlopeDelta, Whale) |
| `src/intelligence.py` | Phase 4 | ✅ Production (ForensicAnalyzer) |
| `src/reporter.py` | Phase 5 | ✅ Production (reports + leaderboard) |
| `src/config_validator.py` | Phase 1 | ✅ Production |
| `src/ai_client.py` | Phase 7.1 | ✅ Done (T-025) |
| `src/schemas.py` | Phase 7.1 | ✅ Done (T-025) |
| `src/venture_architect.py` | Phase 7.1 | ✅ Done (T-026) |
| `src/fetcher_reddit.py` | Phase 7.3 | ⏳ Deferred |
| `templates/venture_blueprint.j2` | Phase 7.1 | ✅ Done (T-027) |

