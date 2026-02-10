# Market Leaderboard: Screen Time & Focus Apps

**Generated:** 2026-02-10 16:08:11
**Total Apps Analyzed:** 4

## Risk Score Ranking (MECE Methodology)

Apps are ranked by Risk Score (descending). Higher scores indicate more volatility and potential issues.

| Rank | App Name | Risk Score | Vol. Slope | Neg. Ratio (%) | Volume | Primary Pillar | Suspected Version |
|------|----------|------------|------------|----------------|--------|----------------|-------------------|
| 1 | Tattoo AI Design Gen | 48.89 | -0.0238 | 88.9% | 9 | Economic | 1.6.1 |
| 2 | Ai Tattoo Ideas Art | 46.67 | -0.0000 | 66.7% | 3 | Functional | 1.3.1 |
| 3 | Tattoo AI Design | 42.72 | 0.1374 | 56.7% | 127 | Economic | None |
| 4 | Tattoo AI Design HubX | 42.72 | 0.1374 | 56.7% | 127 | Economic | None |

## Interpretation

### MECE Risk Scoring Methodology

**MECE Pillars:** Mutually Exclusive, Collectively Exhaustive risk categories

1. **Functional Risk:** Technical issues affecting app performance
   - Categories: `critical`, `performance`, `privacy`
   - Examples: Crashes, freezes, bugs, slow loading, data leaks

2. **Economic Risk:** Financial concerns and monetization issues
   - Categories: `scam_financial`, `subscription`, `ads`
   - Examples: Unexpected charges, billing problems, deceptive pricing

3. **Experience Risk:** Usability and competitive positioning
   - Categories: `usability`, `competitor_mention`, `generic_pain`
   - Examples: Confusing UI, difficult navigation, preference for alternatives

### Risk Score Calculation

**Formula:** `BaseScore × (1 + max(0, VolatilitySlope))`

- **Base Score:** `(FunctionalDensity + EconomicDensity + ExperienceDensity) × 10.0`
  - Density = Sum of keyword weights / Total reviews analyzed
  - Scaler (10.0) standardizes so ~1 major pain point per user = 100

- **Volatility Boost:** Amplifies score if trend is worsening (positive slope)
  - If slope > 0: Score increases proportionally
  - If slope ≤ 0: Base score remains unchanged

### Column Definitions

- **Risk Score (0-100):** MECE-based composite metric (Pillar + Boost)
- **Vol. Slope (Trend):** Rate of change in pain-keyword reviews per week
  - Positive = increasing problems (worsening)
  - Negative = decreasing problems (improving)
  - Zero = stable (no trend)
- **Neg. Ratio (%):** Percentage of reviews containing pain keywords
- **Volume:** Total number of reviews analyzed (last 90 days)
- **Primary Pillar:** MECE pillar with highest density (Functional/Economic/Experience)
- **Suspected Version:** App version with spike in pain-keyword reviews (if detected)

### Risk Score Ranges
- **0-25:** Low Risk (Stable)
- **26-50:** Moderate Risk (Watch)
- **51-75:** High Risk (Concerning)
- **76-100:** Critical Risk (Urgent Action Needed)
