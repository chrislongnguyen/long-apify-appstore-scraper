---
phase: requirements
title: App Store "Pain Refinery" & Volatility Analyzer (Python Edition)
description: Deterministic extraction and statistical analysis of "Enshittification" signals from App Store reviews.
---

# 1. EFFECTIVE REQUIREMENTS (User Actions)

## 1.1 The Problem Space
**What problem are we solving?**
- **Core Pain Point:** The "Founder's Guess." We currently assume we know why incumbent apps are failing, but we lack quantitative evidence of specific feature failures, version degradations, or predatory monetization shifts.
- **Current Workaround:** "Doom-scrolling" reviews or using expensive, opaque market intelligence tools.
- **The Gap:** We need raw, unhallucinated mathematical proof of *where* and *when* an app started failing.

## 1.2 The Actor
- **Primary User:** The "Product Detective" (Founder/Strategist).
- **System Actor:** The `long-apify-appstore-scraper` (Python ETL Pipeline).

## 1.3 Desired User Action (The Goal)
* **Verb (The Core Action):** **Extract, Compute & Storytell**.
    * *Acceptance Criteria 1:* The system must ingest a list of App Store URLs and fetch reviews from the **Last 90 Days** only.
    * *Acceptance Criteria 2:* The system must output Markdown reports (`report_{APP}_{YYYY-MM-DD}.md`) that use hard data (counts, slopes, correlations) to tell the story of the app's decline, without using an LLM.

### Effectiveness Constraints (The "How")
* **Sustainability Adverbs (Safety/Risk):** [Data Integrity]
    * *Constraint:* **Deterministically** (Math > Vibes).
    * *Acceptance Criteria:* Analysis must be performed using standard Python libraries (Pandas, NumPy). No external AI calls for scoring.
    * *Constraint:* **Legally** (Compliance).
    * *Acceptance Criteria:* Respect Apify actor limits. Handle timeouts gracefully.

* **Efficiency Adverbs (Utility/Speed):** [Optimization]
    * *Constraint:* **Surgically** (Time-Bound).
    * *Acceptance Criteria:* Hard filter: `date >= (today - 90 days)`.
    * *Constraint:* **Thriftily** (Noise Reduction).
    * *Acceptance Criteria:* Discard reviews with fewer than N words (configurable via `settings.json` min_review_length_words) unless they contain "Critical Keywords" (e.g., "scam", "crash").

* **Scalability Adverbs (Growth):** [Volume]
    * *Constraint:* **Comparatively** (Benchmarking).
    * *Acceptance Criteria:* Logic must support processing multiple apps in one run to generate a "Winner vs. Loser" comparison table.

## 1.4 Functional Logic (The Data Science Brain)
**The Python script must implement three layers of analytics:**

### Layer 1: Descriptive Analytics (The "What")
* **Signal:** *Volume of Negativity.*
* **Logic:** Count of reviews containing pain keywords (from `pain_keywords.json`) vs Total Reviews per Week. *(T-011: "Negative" redefined as pain-keyword reviews, not just 1-2 star rating — handles "Irony Paradox" where 5-star reviews express pain.)*
* **Output:** "Weekly Complaint Velocity" (e.g., "50 complaints/week").

### Layer 2: Predictive Analytics (The "Trend")
* **Signal:** *The "Enshittification" Curve.*
* **Logic:** Calculate the **Slope (m)** of the 1-Star trendline over the last 12 weeks.
    * If `m > 0.5` (Steep Increase): Flag as "Rapid Degradation".
    * If `m ~ 0` (Flat but High): Flag as "Persistent Pain".
* **Signal:** *Version Impact.*
    * Correlation check: Does a spike in negative volume coincide with a specific `version` string?

### Layer 3: Prescriptive Analytics (The "Score")
* **Signal:** *The Risk Score (0-100).*
* **Formula:** A weighted composite index.
    * $$Score = (W_{recency} \times Recent\_Vol) + (W_{intensity} \times Keyword\_Severity)$$
    * **Recency:** Weight reviews from last 30 days 2x more than days 31-90.
    * **Intensity:** Keyword matching against `pain_keywords.json` (e.g., "fraud" = 10pts, "slow" = 2pts).
* **Output:** A prioritized list of "Kill Metrics" (e.g., "Fix Login Crash to reduce Risk Score by 40 points").

## 1.5 Output Format (The Story)
The Python script must generate Markdown files (`report_{APP}_{YYYY-MM-DD}.md`) containing:
1.  **Executive Summary:** (Computed f-string) "App X is in [CRITICAL/STABLE] condition with a Risk Score of [78/100]."
2.  **The Evidence:**
    * "Primary Pain Cluster: 'Subscription' (mentioned in 60% of negative reviews)."
    * "The 'Cliff' Event: Sentiment dropped 40% after Version 5.2 on [Date]."
3.  **Raw Data Sample:** Top 5 "Most Helpful" 1-star reviews.

## 1.6 Non-Goals
- **Out of Scope:** Sentiment Analysis via LLM (Too slow/costly). Use dictionary-based polarity instead.
- **Out of Scope:** Historic data beyond 90 days (Not actionable).

---

---

# 2. FORENSIC INTELLIGENCE SPECIFICATION (T-008)

To achieve "Irrefutable Evidence" in reporting, the system must implement the following advanced analytical modules beyond basic descriptive statistics.

## 2.1 The "Timeline of Pain" (Event Detection)
* **Goal:** Correlate Review Volume/Sentiment with time to identify "Bad Updates."
* **Logic:**
    * Group reviews by `week` (ISO Calendar).
    * **Formula:** $PainDensity = \frac{\text{Weighted Pain Count}}{\text{Total Reviews in Week}}$ where Whale reviews (T-023) contribute 3x.
    * **Anomaly Detection:** Flag any week where $Density > (\mu_{rolling} + 2\sigma)$.
* **Acceptance Criteria:**
    * Must correctly identify known spikes (e.g., Version 2.0 launch).
    * Must ignore/flag weeks with < 5 reviews (Noise Filter).
    * Output must be a time-series list: `[{week: "2023-42", density: 0.85, event: "Critical Spike"}]`.
* **Assumptions:** "Date" in reviews is localized to UTC.

## 2.2 Semantic Clustering (N-Gram Analysis)
* **Goal:** Discover *unknown* pain points that are not in `pain_keywords.json`.
* **Library:** Use `sklearn.feature_extraction.text.CountVectorizer` or `collections.Counter`.
* **Configuration:**
    * `ngram_range=(2, 3)` (Look for 2-3 word phrases like "login failed", "lost data").
    * **Universe:** Only analyze reviews with `rating <= 2` (The "Cluster of Hate").
    * **Stop Words:** Standard English + App Name.
* **Acceptance Criteria:**
    * Must output at least 3 unique, non-generic phrases (e.g., "sync failed" is valid; "good app" is invalid).
    * Must process 500 reviews in < 2 seconds.

## 2.3 Competitor Migration Graphing
* **Goal:** Identify which competitors are "stealing" users.
* **Logic:**
    * Load the list of `app_names` from `targets.json`.
    * Scan the *text body* of App A's reviews for mentions of App B, C, D.
    * **Sentiment Check:** Distinguish "Churn" (I'm leaving for X) from "Comparison" (This is better than X).
* **Acceptance Criteria:**
    * Correctly tags "I switched to Opal" as a Migration Event.
    * Correctly ignores "Better than Forest" (Positive Comparison).

## 2.4 The "Feature/Fail" Matrix (Output Artifact)
* **Goal:** Comparative Heatmap for Niche Reports.
* **Output Artifact:** `reports/niche_matrix.json`
* **Schema Definition:**
  ```json
  {
    "App Name A": {
      "Functional": 85.5,
      "Economic": 20.0,
      "Experience": 15.0
    },
    "App Name B": {
      "Functional": 10.0,
      "Economic": 95.0,
      "Experience": 40.0
    }
  }
* **Acceptance Criteria:**
    * Keys must match valid App Names from targets.json.
    * Values must be Normalized Risk Scores (0-100).
    * Must visually flag scores > 50 with 🔴 in the generated Markdown report.

## 2.5 Data Flow Requirements
* **Input:** The `ForensicAnalyzer` must receive the full **Raw Reviews DataFrame** (`reviews_df`), not just the calculated metrics.
* **Reasoning:** N-Gram analysis requires the raw `text` column to detect phrases like "sync failed".
* **Privacy:** No PII is retained; only aggregate stats and anonymized quotes are saved to Markdown.
* **Output Artifacts:**
    * `reports/{niche_name}/niche_matrix.json` (The Comparative Heatmap).
    * `reports/{niche_name}/{app}_intelligence.json` (The Intermediate Forensic Data).

## 2.6 White Space / Safe Harbor (T-017)
* **Goal:** Identify "Low Risk, High Quality" gaps in the niche for positioning.
* **Logic:** An app qualifies as a **Safe Harbor** only if ALL of the following hold:
    * Functional pillar score < 30 AND Economic pillar score < 30 (from niche_matrix).
    * **AND** `risk_score < 50` (from schema_app_gap). High risk_score disqualifies even if pillars are low.
* **Output:** "Gap Found" or "No Gap" section in the Niche Report (`report_NICHE_{NAME}_{YYYY-MM-DD}.md`).

---

## 3. IMPLEMENTATION & ASSUMPTIONS

* **Assumptions:** "Date" in reviews is localized to UTC; Apify output schema is stable; `targets.json` and `pain_keywords.json` are valid.
* **Config:** Filter thresholds (min_review_length_words, min_star_rating) are configurable via `settings.json`; defaults may vary by deployment.

---

## 4. PHASE 6: PREDICTIVE ANALYTICS (The Oracle)

### Problem Space
- **Core Pain Point:** "Magnitude Blindness" - Founders know competitors are failing (Diagnostic), but don't know *how fast* they are crashing or *how much money* is bleeding.
- **The Gap:** A chart showing "more bad reviews" is interesting. A headline saying "Competitor X lost $45k in November due to Version 4.0" is actionable.
- **The Shift:** Move from "Static Analysis" to "Dynamic Forecasting" (Trend Acceleration & Revenue Estimation).

### The Actor
- **Primary User:** The "Venture Architect" (Founder/Investor)
- **System Actor:** `PredictiveModel` (Python Stats Engine)

### Desired User Action
**Verb:** **Quantify, Forecast & Name**

**Acceptance Criteria:**
1. System must calculate the **Slope Delta** (Acceleration) to highlight if enshittification is speeding up or slowing down.
2. System must **"Name the Spike"**: Automatically link statistical anomalies to specific Version Numbers (e.g., "The Version 4.0 Disaster").
3. System must estimate **Revenue Leakage** using a Fermi Model with dynamic multipliers based on app category (B2B/Consumer/Game).

### Effectiveness Constraints
- **Financially (Fermi Logic):** Use the "Iceberg Theory" to estimate silent churners from visible complaints.
- **Contextually (Causality):** Every spike must be treated as a "Marketing Headline" opportunity, not just a data point.
- **Triangulated (Accuracy):** Combine App Store (Floor), Reddit (Intensity), and Pricing (Value) to bounds-check estimates.

### Functional Logic (Predictive Layer)

#### 1. Deterministic Trend Analysis (The Slope & Delta)
* **Metric:** `Volatility Slope` ($m$) via Linear Regression (Review Volume vs Time).
* **New Metric:** **Slope Delta** ($\Delta m$).
    * *Logic:* Compare Slope(Last 4 Weeks) vs Slope(Previous 4 Weeks).
    * *Insight:* "Is the bleeding accelerating?" (Positive $\Delta$) or "Is it stabilizing?" (Negative $\Delta$).
    * *Output:* "Acceleration Detected: +15% week-over-week."

#### 2. Statistical Anomaly Detection (The Named Spike)
* **Principle:** Event Causality. "Random" bad weeks don't exist; they are caused by decisions.
* **Logic:**
    * Identify Anomaly: $PainDensity > \mu + 2\sigma$.
    * Identify Culprit: Correlate anomaly week with `version_history` (if available) or dominant topic cluster.
* **Output:** Transform "Week 42 Spike" $\to$ "**The Version 4.2 Crash**" (Narrative Label).
* **Founder Lesson:** Use this for marketing copy (e.g., "Did you lose data in Nov? We built an importer.").

#### 3. Fermi Estimation (The Revenue Engine)
* **Goal:** Quantify the financial opportunity ($ Monthly Leakage).
* **Formula:** $Leakage = (Churn\_Reviews \times Multiplier) \times Avg\_Price$
* **Variables:**
    * `Churn_Reviews`: Count of reviews with "Economic" or "Functional" pain pillars.
    * `Avg_Price`: Extracted from "In-App Purchases" list (or default $9.99).
    * `Multiplier`: **Dynamic Ratio** based on Niche Category (Configurable in `targets.json`):
        * **B2B SaaS:** 1:50 (High friction to complain).
        * **Consumer Utility:** 1:100 (Standard).
        * **Games/Viral:** 1:200+ (Low friction, high churn).
* **Triangulation (Confidence Check):**
    * *App Store:* Provides the "Floor" (Verified Paying Users).
    * *Reddit:* Provides the "Intensity" (If sentiment is "Vitriolic", increase Multiplier by 1.5x).

### 4.1 Whale Detector (T-023)
* **Goal:** Prioritize high-value reviews (long, domain-specific) for evidence and Pain Density.
* **Logic:** A review is a "Whale" if it has > 40 words OR contains domain vocabulary (e.g., "latency", "vector", "workflow", "sync", "export").
* **Multiplier:** 3.0x for Pain Density (Whale reviews contribute 3x to weekly pain count) and for evidence ranking.

### 4.2 Predictive Integration (T-024)
* **Goal:** Surface predictive metrics in reports and leaderboard.
* **Individual Report:** Financial Impact section ("Estimated Monthly Revenue Leakage: $X", "Trend Acceleration: [insight]").
* **Timeline Exhibit:** Named Spike used for exhibit title when available (e.g., "Exhibit A: The Version X.X Crisis").
* **Leaderboard:** Primary sort by `monthly_leakage_usd` (descending); Revenue Leakage ($/mo) column; Momentum column.
* **Momentum Labels (T-021 Refined):**
    * `volatility_slope > 0.1` + `slope_delta > 0` → "Accelerating Pain"
    * `volatility_slope > 0.1` + `slope_delta < 0` → "Decelerating Pain"
    * `-0.05 ≤ volatility_slope ≤ 0.05` → "Stabilizing"
    * `volatility_slope < -0.05` → "Improving"

---

## 5. PHASE 7: PRESCRIPTIVE ANALYTICS (The Architect) - *DEFERRED*
* **Goal:** Generate "Anti-Roadmap" and User Stories using GenAI.
* **Status:** De-prioritized until Predictive Layer (Phase 6) is validated.