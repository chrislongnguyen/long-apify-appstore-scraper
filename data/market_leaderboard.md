# Market Leaderboard: Screen Time & Focus Apps

**Generated:** 2026-02-09 23:49:55
**Total Apps Analyzed:** 5

## Risk Score Ranking (MECE Methodology)

Apps are ranked by Risk Score (descending). Higher scores indicate more volatility and potential issues.

| Rank | App Name | Risk Score | Vol. Slope | Neg. Ratio (%) | Volume | Primary Pillar | Suspected Version |
|------|----------|------------|------------|----------------|--------|----------------|-------------------|
| 1 | Forest Focus | 45.77 | -0.4848 | 44.2% | 163 | Economic | 5.1.3 |
| 2 | Opal Screen Time | 42.14 | 0.5440 | 26.3% | 255 | Functional | None |
| 3 | Freedom Blocker | 19.44 | 0.0833 | 17.9% | 39 | Economic | 6.59 |
| 4 | OneSec Mindfulness | 11.08 | 0.0714 | 13.8% | 29 | Functional | 5.1 |
| 5 | StayFree Tracker | 7.50 | 0.0000 | 25.0% | 4 | Experience | 3.2 |

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
