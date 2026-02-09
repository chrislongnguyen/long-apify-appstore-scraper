# Config Externalization Summary

## Overview
All hardcoded logic has been externalized to `config/settings.json` to improve scalability and fix the "Empty JSON" issue.

## Changes Made

### 1. Created `config/settings.json`
Based on the schema defined in `docs/ai/design/apify-appstore-scraper.md`:
- **filters**: `min_star_rating`, `min_review_length_words`, `drop_generic_5_star`, `force_fetch_count`
- **weights**: `slope_impact`, `volume_impact`, `critical_keyword`, `scam_keyword`, `performance_keyword`, `ux_keyword`
- **processing**: `enable_smoke_test`, `days_back_default`

### 2. Updated `src/config_validator.py`
- Added `validate_settings_config()` function
- Validates all required fields and types
- Integrated into main validation flow

### 3. Refactored `src/fetcher.py`
**Before:** Hardcoded `if rating < 5` and hardcoded critical keywords
**After:** 
- Accepts `settings` parameter in `__init__`
- Uses `filters.min_star_rating` for rating threshold
- Uses `filters.drop_generic_5_star` for 5-star filtering logic
- Uses `filters.force_fetch_count` for smoke test mode
- Logic: When `min_star_rating <= 3`, includes ALL reviews (including all 5-stars)
- Logic: When `min_star_rating >= 4`, applies `drop_generic_5_star` filtering

### 4. Refactored `src/analyzer.py`
**Before:** Hardcoded formula `(20 * slope_score) + (0.5 * vol_score)`
**After:**
- Accepts `settings` parameter in `__init__`
- Uses `weights.slope_impact` (default: 20.0)
- Uses `weights.volume_impact` (default: 0.5)
- Uses category weights from `pain_keywords.json` for category scoring

### 5. Updated `main.py`
- Loads `settings.json` at startup
- Validates settings configuration
- Passes settings to both `Fetcher` and `Analyzer` instances

## Testing

### Test Scripts Created
1. **`test_config_change.py`**: Verifies that changing `min_star_rating` to 1 includes 5-star reviews
   - ✅ Test passed: `min_star_rating = 1` includes all reviews including 5-stars
   - ✅ Test passed: `min_star_rating = 4` filters out low ratings

2. **`test_smoke.py`**: Updated to use settings configuration

### Verification
```bash
# Test config validation
python src/config_validator.py
# ✓ All configs validated

# Test config change behavior
python test_config_change.py
# ✓ Config change test passed
```

## Usage Example

### To include 5-star reviews in output:
1. Edit `config/settings.json`:
   ```json
   {
     "filters": {
       "min_star_rating": 1,
       ...
     }
   }
   ```

2. Run smoke test:
   ```bash
   python main.py --smoke-test
   ```

3. Check output: `data/*_reviews.json` will include 5-star reviews

### To adjust risk scoring weights:
Edit `config/settings.json`:
```json
{
  "weights": {
    "slope_impact": 25.0,  // Increased from 20.0
    "volume_impact": 0.75,  // Increased from 0.5
    ...
  }
}
```

## Benefits

1. **Scalability**: No code changes needed to adjust filtering/scoring
2. **Fix Empty JSON Issue**: Can set `min_star_rating = 1` to include all reviews
3. **Testability**: Easy to test different configurations
4. **Maintainability**: All configuration in one place
5. **Flexibility**: Users can adjust behavior without touching code

## Files Modified

- ✅ `config/settings.json` (created)
- ✅ `src/config_validator.py` (updated)
- ✅ `src/fetcher.py` (refactored)
- ✅ `src/analyzer.py` (refactored)
- ✅ `main.py` (updated)
- ✅ `test_smoke.py` (updated)
- ✅ `test_config_change.py` (created)

## Next Steps

- [ ] Document settings.json schema in README
- [ ] Add example configurations for common use cases
- [ ] Consider adding CLI flags to override settings.json values
