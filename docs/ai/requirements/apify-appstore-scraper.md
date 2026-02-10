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
    * *Acceptance Criteria 2:* The system must output a `analysis_report.md` that uses hard data (counts, slopes, correlations) to tell the story of the app's decline, without using an LLM.

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
    * *Acceptance Criteria:* Discard reviews with `< 3 words` unless they contain "Critical Keywords" (e.g., "scam", "crash").

* **Scalability Adverbs (Growth):** [Volume]
    * *Constraint:* **Comparatively** (Benchmarking).
    * *Acceptance Criteria:* Logic must support processing multiple apps in one run to generate a "Winner vs. Loser" comparison table.

## 1.4 Functional Logic (The Data Science Brain)
**The Python script must implement three layers of analytics:**

### Layer 1: Descriptive Analytics (The "What")
* **Signal:** *Volume of Negativity.*
* **Logic:** Count of 1-Star & 2-Star reviews vs Total Reviews per Week.
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
The Python script must generate a Markdown file (`report_APPNAME.md`) containing:
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
    * **Formula:** $PainDensity = \frac{\text{Count of Reviews with Pain Keywords}}{\text{Total Reviews in Week}}$
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
    * `reports/niche_matrix.json` (The Comparative Heatmap).
    * `reports/intelligence.json` (The Intermediate Forensic Data).