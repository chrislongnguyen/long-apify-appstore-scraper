# Configuration Files

## targets.json
Contains the list of apps to analyze and scraping parameters.

**Schema:**
- `apps`: Array of app objects with `name` and `url` fields
- `params`: Object with `days_back` (number of days to look back) and `max_reviews` (maximum reviews to fetch)

## pain_keywords.json
Bilingual dictionary of pain keywords organized by category with weights for scoring.

**Schema:**
- `categories`: Object where each key is a category name
  - Each category has:
    - `keywords`: Array of strings (supports English and Vietnamese)
    - `weight`: Number representing the severity weight (higher = more critical)

## settings.json
System-wide settings for filtering and scoring logic. **This file controls behavior without code changes.**

**Schema:**
- `filters`: Filtering configuration
  - `min_star_rating`: Minimum star rating to include (1-5). Set to 1 to include all reviews including 5-stars.
  - `min_review_length_words`: Minimum word count for reviews (reviews with critical keywords bypass this)
  - `drop_generic_5_star`: If true and `min_star_rating >= 4`, drops generic 5-star reviews (keeps those with critical keywords)
  - `force_fetch_count`: Number of reviews to fetch in smoke test mode
- `weights`: Risk scoring weights
  - `slope_impact`: Weight for trend slope impact (default: 20.0)
  - `volume_impact`: Weight for volume impact (default: 0.5)
  - `critical_keyword`: Weight for critical keywords (default: 10.0)
  - `scam_keyword`: Weight for scam-related keywords (default: 8.0)
  - `performance_keyword`: Weight for performance keywords (default: 5.0)
  - `ux_keyword`: Weight for UX keywords (default: 2.0)
- `processing`: Processing configuration
  - `enable_smoke_test`: Enable smoke test mode by default
  - `days_back_default`: Default days to look back (default: 90)

**Example: To include 5-star reviews in output:**
```json
{
  "filters": {
    "min_star_rating": 1,
    ...
  }
}
```

## Validation
The system will crash gracefully if these files are missing or contain malformed JSON.
