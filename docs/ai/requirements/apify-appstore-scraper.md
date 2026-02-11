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

---

---

## 5. PHASE 7: THE VENTURE ARCHITECT (The Anthropologist Engine)

### Problem Space
- **The Gap:** Phase 6 tells us *where* the money is leaking, but not *who* the human is or *how* to build a better system for them.
- **The Need:** A "Full-Spectrum" analysis that understands the User's **Ultimate Desired Outcome (UDO)**, their **Biological/Psychological Constraints**, and the **Principles** required to solve them better than the incumbent.
- **The Pivot:** We must analyze **Success** (Why they stay) as deeply as **Failure** (Why they leave).

### The Actor
- **Primary User:** The "Solo Founder" (Venture Scientist).
- **System Actor:** `VentureArchitect` (Multi-Source Intelligence Agent).

### Expanded Data Sources (MECE & Scrapable)
To draw a full ICP, we require a MECE (Mutually Exclusive, Collectively Exhaustive) view of the user's reality:
1.  **The Pain Signal (1-2 Star Reviews):** *Existing.* Reveals Blockers (UBS) and Symptoms.
2.  **The Success Signal (5-Star "Whale" Reviews):** *New.* Reveals Drivers (UDS), "Aha Moments," and what the incumbent actually gets right.
    * *Filter:* Length > 30 words (ignore "Great app"). Look for "Changed my life because..."
3.  **The Context Signal (Reddit/Forum Scraper):** *New.* Reveals "Alternatives," "Hacks," and "Real-world Context."
    * *Target:* Subreddits related to the Niche (e.g., r/intermittentfasting).
    * *Query:* "Best app for [Niche]", "Alternative to [Competitor]", "How to [Action]".

### Desired User Action
**Verb:** **Construct Holographic ICP & Prescribe EPS System**

**Acceptance Criteria:**
1.  **Draw the Holographic ICP:**
    * **Who:** Demographic & Psychographic inference.
    * **Why:** The **Ultimate Desired Outcome (UDO)** (e.g., "Not weight loss, but social confidence").
    * **What/How:** The actual workflow (Step-by-step).
    * **When:** The trigger context (e.g., "While grocery shopping").
    * **Alternatives:** What do they use when the app fails? (Competitors, Spreadsheets, Pen & Paper).

2.  **5-Layer Root Cause Analysis (Inference Engine):**
    * Map both **Drivers (Success)** and **Blockers (Failure)** across the 5 Layers:
        * *Layer 1 (App):* Interface/Features.
        * *Layer 2 (Behavior):* Habits/Workflows.
        * *Layer 3 (System):* The UDS - Ultimate Driving System / UBS - Ultimate Blocking System Loops.
        * *Layer 4 (Psychology):* Biases (Fear, Ego, Status).
        * *Layer 5 (Biology):* Dopamine, Cortisol, Energy Conservation.

3.  **Derive the EPS Solution (The Prescription):**
    * **Principles:** The strategic rules that *disable* the blockers or *enable* the drivers (e.g., "Rule 1: Never ask for data entry when user is hangry").
    * **Environment:** The context design (e.g., "Home Screen Widget" vs. "Full App").
    * **Tools (The Trojan Horse):**
        * *Desirable Wrapper:* The feature that sells the solution (The Hook).
        * *Effective Core:* The mechanic that solves the Layer 5 Root Cause.

### Functional Logic (The Architecture)

#### 1. The "Success & Failure" Triangulator
* **Input:** 1-Star & 2-Star Reviews (Pain), 5-Star Reviews (Joy), Reddit Threads (Truth).
* **Logic:**
    * *Compare:* If 1-Star says "Too complex" but 5-Star says "Love the depth," the ICP is split (Casual vs. Pro). Identify *which* segment is the "Whale."
    * *Contextualize:* Use Reddit to find *where* the app fits in their life. (e.g., "I use Zero only for the timer, but I use Excel for the data").

#### 2. The 7-Layer Deep Dive (The Analyst)
For the identified ICP, populate the **System Dynamics Map**:
* **UDO (Ultimate Desired Outcome):** The "Adverb" of their life (e.g., *Effortlessly* Lean).
* **UDS (The Driver):** The conscious force pushing them toward UDO (e.g., "Desire for longevity").
    * **UDS.UD (Driver of UDS):** The root cause of the Driver's success (e.g., "Fear of early death/Survival Instinct").
    * **UDS.UB (Blocker of UDS):** The root cause of the Driver's failure (e.g., "Cognitive Dissonance / Forgetfulness").
* **UBS (The Blocker):** The conscious force stopping them (e.g., "Procrastination / Sugar Cravings").
    * **UBS.UD (Driver of UBS):** The root cause of the Blocker's success (e.g., "Bio-Efficiency / System 1 Energy Conservation"). *Why is the problem so good at winning?*
    * **UBS.UB (Blocker of UBS):** The root cause of the Blocker's failure (e.g., "Mindfulness / Acute Pain"). *What naturally kills the problem?*
* **Incumbent Failure:** Why the current market leader fails to address Layers 4-7 (e.g., "Addresses Symptom, ignores Bio-Efficiency").

#### 3. The EPS Generator (The Architect)
Derive the solution **strictly** from the Deep Dive map above.

**A. Principles (The Strategy)**
* *Logic:*
    * **Amplify UDS.UD:** How do we feed the "Survival Instinct"?
    * **Disable UDS.UB:** How do we remove "Forgetfulness"?
    * **Starve UBS.UD:** How do we make "Bio-Efficiency" work *for* us, not against us?
    * **Amplify UBS.UB:** How do we trigger "Acute Pain" or "Mindfulness" automatically?
* *Output Example:* "Principle 1: Zero-Cognitive Load (Aligns with UBS.UD Bio-Efficiency). Principle 2: Immediate Feedback Loop (Amplifies UBS.UB Acute Pain)."

**B. Environment (The Context)**
* *Logic:* Based on the Principles, where *must* the solution live to be effective?
* *Output Example:* "Since Principle 1 is 'Zero-Load', the Environment cannot be an App. It must be a **Lock Screen Widget** or **Background Service**."

**C. Tools (The Mechanism)**
* *Logic:* What specific artifact delivers the Principle in the Environment?
* *Output Example:* "Tool: A 'Passive Calorie Tracker' that syncs via API, with a 'Shock' notification (Red Screen) if limits are exceeded."

**D. SOP (The Workflow)**
* *Logic:* The precise Step-by-Step operation for the user.
* *Output Example:* "User Action: None. System Action: Monitor background. Trigger: Only interrupt when UBS is detected."

### Data Output Schema (`venture_blueprint.md`)
1.  **The System Map:** A hierarchical view of UDO -> UDS/UBS -> Root Drivers/Blockers.
2.  **The Strategic Inversion:** A table showing "Incumbent Method" vs. "New Principle" derived from Root Causes.
3.  **The EPS Prescription:**
    * **Environment** (Where)
    * **Principles** (Why)
    * **SOP & Tools** (How/What)
4.  **The Trojan Horse:** The "Desirable Hook" (Level 1) wrapping the "Effective System" (Level 7).