## 🧠 Intelligence Legend & Formulas

### 1. Risk Score (0-100)
**The Formula:** $Risk = (PillarDensity \times 10) \times (1 + PositiveSlope)$
- **What it means:** A normalized measure of "Pain Intensity."
- **Interpretation:**
  - **0-20:** Stable. Users are generally content.
  - **80-100:** Critical. Users are reporting ~1 major failure *every single review*, and the trend is worsening.
- **Example:** A score of **65** means the app has significant issues (e.g., a buggy update), but it hasn't reached "Scam" levels of toxicity yet.

### 2. Volatility Slope (Trend)
**The Formula:** Linear Regression of "Pain Density" over the last 90 days.
- **Positive (+):** **WARNING.** The app is getting worse. New bugs or aggressive monetization are driving recent hate.
- **Negative (-):** The app is stabilizing. The "event" (bad update) is in the past, and angry users are leaving.
- **Example:** A slope of **+0.5** means pain density is increasing by 50% every week—an active collapse.

### 3. Negative Ratio (%)
**The Formula:** $\frac{\text{Reviews with Pain Keywords}}{\text{Total Analyzed Reviews}}$
- **Context:** This is based on the *specific batch* of reviews fetched (e.g., the last 500), not the lifetime history.
- **Why it matters:**
  - **High Ratio + High Risk:** The app is universally hated.
  - **Low Ratio + High Risk:** "The Silent Killer." Most users are quiet, but the few who speak are reporting dangerous scams or data loss.

### 4. MECE Pillars (Primary Pain)
- **Functional:** "It doesn't work." (Crashes, Bugs, Logins)
- **Economic:** "It costs too much." (Scams, Price Hikes, Paywalls)
- **Experience:** "It's annoying." (Bad UI, Ads, Confusion)

---

### 📉 Combined Signal Example: "The Opportunity Target"
**Data Profile:**
- **Risk Score:** 92.0
- **Slope:** +0.45
- **Primary Pillar:** Economic
- **Negative Ratio:** 35%

**The Story:**
"This app (Score 92) has aggressively changed its pricing model (Economic Pillar). The move is recent and disastrous, as pain is accelerating week-over-week (Slope +0.45). While only 35% of users have reviewed it negatively so far, the intensity of their anger is maximum. **Strike Opportunity: High.**"