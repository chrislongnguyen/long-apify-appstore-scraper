---
phase: implementation
title: Knowledge - Fetcher Module
description: High-level overview of the Fetcher class for App Store review retrieval via Apify API
analysis_date: 2026-02-10
entry_point: src/fetcher.py
depth: high-level
files_touched: 1
---

# Knowledge: Fetcher Module

## Overview

The `Fetcher` class is the core data acquisition component of the App Store Volatility Analyzer. It handles reliable fetching of App Store reviews from the Apify cloud platform, implements configurable filtering logic, and manages error handling with retry mechanisms.

**Purpose:** Bridge between the application and Apify's App Store Reviews Scraper actor, providing a fault-tolerant, configurable interface for retrieving and filtering review data.

**Language:** Python 3.9+

**Key Characteristics:**
- **Fault-Tolerant:** Uses Tenacity for automatic retry on network failures
- **Config-Driven:** Filtering behavior and country controlled via `settings.json`
- **Thrifty:** In-memory filtering to reduce storage (drops generic 5-star reviews)
- **Timezone-Aware:** Properly handles UTC datetime comparisons
- **Multi-Region:** Supports fetching from any App Store country or all countries

## Implementation Details

### Core Responsibilities

1. **Apify API Integration**
   - Connects to `agents/appstore-reviews` actor (faster, more reliable)
   - Alternative: `thewolves/appstore-reviews-scraper` (if agents version has issues)
   - Manages API authentication via token (env var or parameter)
   - Extracts App ID from URLs for reliable API calls
   - Supports `appIds` (preferred) or `startUrls` fallback

2. **Reliable Data Fetching**
   - Implements retry logic with exponential backoff (3 attempts, 2-10s wait)
   - Handles connection/timeout errors gracefully
   - Filters out error responses from Apify (`{"error": true}` or `{"noResults": true}` objects)

3. **Multi-Country Support**
   - Configurable via `settings.json` → `filters.country`
   - Options: `"us"` (default), `"gb"`, `"all"` (all countries), or any 2-letter code
   - Use `"all"` for niche apps with limited reviews in specific regions

4. **Date Filtering**
   - Filters reviews to last N days (default: 90)
   - Handles timezone-aware datetime comparisons
   - Falls back to including reviews if date parsing fails

5. **Configurable Review Filtering**
   - Applies `min_star_rating` threshold from settings
   - Drops generic 5-star reviews (configurable via `drop_generic_5_star`)
   - Keeps 5-star reviews with critical keywords (scam, crash, etc.)
   - Enforces minimum review length (configurable)

6. **Data Persistence**
   - Saves filtered reviews to JSON files
   - Creates output directories as needed

### Key Methods

#### `__init__(apify_token, settings)`
- Initializes Apify client with authentication
- Loads filter configuration from settings
- Validates API token presence

#### `_extract_app_id(app_url)`
**Helper method** for parsing App Store URLs.
- Extracts numeric App ID from URL using regex
- Pattern: `/id(\d+)` matches IDs like `6499420042`
- Returns `None` if extraction fails (triggers fallback to URL)

#### `fetch_reviews(app_url, days_back, max_reviews, smoke_test)`
**Main public interface** for fetching reviews.
- Validates URL parameter
- Handles smoke test mode (limits to configured count)
- Calls `_run_apify_actor()` to fetch from Apify
- Applies date filtering (last N days)
- Returns filtered review list

#### `_run_apify_actor(app_url, max_items)`
**Private method** with retry decorator.
- Validates URL is string (not object)
- Extracts App ID from URL via `_extract_app_id()`
- Uses `appIds` parameter (preferred) or falls back to `startUrls`
- Reads country from `settings.json` (default: "us", supports "all")
- Waits for actor completion
- Filters out error responses (`error: true` or `noResults: true`)
- Returns valid reviews only

#### `filter_reviews(reviews)`
**Configurable filtering logic.**
- Applies `min_star_rating` threshold
- Drops reviews below minimum word count (unless critical keywords present)
- Special handling for 5-star reviews:
  - If `min_star_rating == 5`: Include ALL 5-star reviews
  - If `min_star_rating >= 4` and `drop_generic_5_star`: Drop generic 5-stars, keep critical ones
  - Otherwise: Include all 5-stars
- Returns filtered list with logging

#### Helper Methods
- `_parse_review_date()`: Handles multiple date formats (ISO, Unix timestamp)
- `_extract_rating()`: Extracts rating from various field names
- `_extract_review_text()`: Extracts text from various field names
- `save_reviews()`: Persists reviews to JSON file

### Execution Flow

```mermaid
graph TD
    A[main.py calls fetch_reviews] --> B{Smoke Test?}
    B -->|Yes| C[Limit to force_fetch_count]
    B -->|No| D[Use max_reviews]
    C --> E[_run_apify_actor]
    D --> E
    E --> F[Validate URL string]
    F --> G[Extract App ID from URL]
    G --> H{App ID found?}
    H -->|Yes| I[Use appIds parameter]
    H -->|No| J[Fallback to startUrls]
    I --> K[Add country from settings]
    J --> K
    K --> L[Call Apify API with retry]
    L --> M{Success?}
    M -->|No| N[Retry up to 3 times]
    N --> L
    M -->|Yes| O[Get dataset items]
    O --> P[Filter error responses]
    P --> Q[Return valid reviews]
    Q --> R[Apply date filtering]
    R --> S[Return filtered reviews]
    
    T[filter_reviews called] --> U[Load settings]
    U --> V[Check min_star_rating]
    V --> W[Check review length]
    W --> X{5-star review?}
    X -->|Yes| Y{min_star_rating == 5?}
    Y -->|Yes| Z[Include all 5-stars]
    Y -->|No| AA{Has critical keyword?}
    AA -->|Yes| Z
    AA -->|No| AB{Drop generic?}
    AB -->|Yes| AC[Drop]
    AB -->|No| Z
    X -->|No| AD[Include if >= min_rating]
    Z --> AE[Return filtered]
    AC --> AE
    AD --> AE
```

## Dependencies

### External Packages
- **`apify_client`**: Official Apify Python client for API interactions
- **`tenacity`**: Retry library for fault-tolerant API calls
- **Standard Library**: `os`, `json`, `logging`, `typing`, `pathlib`, `datetime`, `re`

### Internal Dependencies
- **`settings.json`**: Configuration file for filter parameters
  - `filters.min_star_rating`: Minimum rating threshold
  - `filters.drop_generic_5_star`: Whether to drop generic 5-star reviews
  - `filters.min_review_length_words`: Minimum word count
  - `filters.force_fetch_count`: Smoke test limit
  - `filters.country`: App Store country code (`"us"`, `"gb"`, `"all"`, etc.)

### Used By
- **`main.py`**: Main entry point that orchestrates the pipeline
  - Creates Fetcher instance with settings
  - Calls `fetch_reviews()` for each app
  - Calls `filter_reviews()` on fetched data
  - Calls `save_reviews()` to persist results

## Error Handling

### Retry Strategy
- **Decorator:** `@retry` from Tenacity
- **Max Attempts:** 3
- **Wait Strategy:** Exponential backoff (2-10 seconds)
- **Retry On:** `ConnectionError`, `TimeoutError`
- **Behavior:** Reraise exception after all retries exhausted

### Error Response Filtering
- Apify may return error objects: `{"error": true, "code": "C003", ...}`
- These are detected and filtered out before returning results
- Logged as warnings for debugging

### Validation Errors
- **Missing API Token:** Raises `ValueError` with clear message
- **Invalid URL Type:** Raises `ValueError` if not string
- **Empty URL:** Raises `ValueError` if URL is empty

### Graceful Degradation
- **Date Parsing Failure:** Includes review anyway (better safe than sorry)
- **Missing Rating:** Includes review (may be valid data)
- **Missing Text:** Treats as empty string, still processes

## Configuration

### Settings Integration
The Fetcher reads from `settings.json` filters section:

```json
{
  "filters": {
    "min_star_rating": 1,
    "min_review_length_words": 3,
    "drop_generic_5_star": true,
    "force_fetch_count": 500,
    "country": "all"
  }
}
```

### Country Options
| Value | Description |
|-------|-------------|
| `"us"` | US App Store only (default) |
| `"gb"` | UK App Store |
| `"all"` | All countries (useful for niche apps) |
| Any 2-letter code | Specific country (see Apify docs) |

### Behavior Examples

**Example 1: Include all 5-star reviews**
```json
{"min_star_rating": 5, "drop_generic_5_star": true}
```
Result: ALL 5-star reviews included (special case logic)

**Example 2: Only critical reviews**
```json
{"min_star_rating": 4, "drop_generic_5_star": true}
```
Result: Ratings 4-5 included, but generic 5-stars dropped (keeps critical 5-stars)

**Example 3: All reviews**
```json
{"min_star_rating": 1, "drop_generic_5_star": false}
```
Result: All reviews included regardless of rating

## Performance Considerations

### Efficiency
- **In-Memory Filtering:** All filtering happens before disk write (thrifty)
- **Early Validation:** URL validation happens before API call
- **Error Filtering:** Removes invalid responses immediately

### Scalability
- **Batch Processing:** Can process multiple apps sequentially
- **Configurable Limits:** `max_reviews` parameter controls API usage
- **Smoke Test Mode:** Limits fetch count for testing

### Resource Usage
- **API Costs:** ~$0.10-0.20 per 1,000 reviews (Apify pricing)
- **Memory:** Minimal (processes reviews one at a time)
- **Network:** Retry logic may increase API calls on failures

## Security Notes

### API Token Management
- Token can be provided via:
  1. Constructor parameter
  2. `APIFY_API_KEY` environment variable
- Token is never logged or exposed in error messages

### Input Validation
- URL type checking prevents injection attacks
- String validation ensures proper formatting

## Known Issues & Limitations

### Current Limitations
1. **Critical Keywords:** Hardcoded list (should come from `pain_keywords.json`)
2. **Date Fields:** Assumes specific field names (may need expansion)
3. **Max 500 Reviews/Country:** Apple API limitation (not Apify's fault)

### Recent Fixes (2026-02-10)
1. **Actor Change:** Switched from `thewolves/appstore-reviews-scraper` to `agents/appstore-reviews` (faster, more reliable)
2. **App ID Extraction:** Added `_extract_app_id()` method to parse numeric IDs from URLs
3. **appIds Parameter:** Now uses `appIds` array (more reliable than `startUrls`)
4. **Country Config:** Made country configurable via `settings.json` → `filters.country`
5. **Multi-Country Support:** Added support for `"all"` country option

### Previous Fixes (2026-02-09)
1. **URL Format:** Fixed from `[{"url": "..."}]` to `["..."]` (Apify requirement)
2. **Timezone:** Fixed datetime comparison to use UTC-aware datetimes
3. **Error Responses:** Added filtering for Apify error objects (`{"error": true}`, `{"noResults": true}`)

## Visual Diagrams

### Component Interaction

```mermaid
graph LR
    A[main.py] -->|1. Create| B[Fetcher]
    B -->|2. Load| C[settings.json]
    C -->|country| B
    B -->|3. Extract App ID| D[URL Parser]
    D -->|4. appIds| E[Apify API]
    E -->|5. Return| F[Raw Reviews]
    B -->|6. Filter| F
    F -->|7. Filtered| G[Valid Reviews]
    B -->|8. Save| H[data/*.json]
    
    style B fill:#e1f5ff
    style E fill:#fff4e1
    style G fill:#e8f5e9
```

### Apify Actor Selection

```mermaid
graph TD
    A[ACTOR_ID] --> B{agents/appstore-reviews}
    B -->|Primary| C[200 reviews/sec]
    B -->|Features| D[appIds + country support]
    B -->|Fallback| E[thewolves/appstore-reviews-scraper]
    
    style B fill:#e8f5e9
    style E fill:#fff4e1
```

### Filter Logic Flow

```mermaid
flowchart TD
    Start[Review] --> CheckRating{Rating exists?}
    CheckRating -->|No| Include[Include Review]
    CheckRating -->|Yes| CheckMin{Rating >= min_star_rating?}
    CheckMin -->|No| Drop1[Drop Review]
    CheckMin -->|Yes| CheckLength{Length >= min_words?}
    CheckLength -->|No| CheckCritical{Has critical keyword?}
    CheckCritical -->|Yes| Include
    CheckCritical -->|No| Drop2[Drop Review]
    CheckLength -->|Yes| Check5Star{Rating == 5?}
    Check5Star -->|No| Include
    Check5Star -->|Yes| CheckMin5{min_star_rating == 5?}
    CheckMin5 -->|Yes| Include
    CheckMin5 -->|No| CheckDrop{drop_generic_5_star?}
    CheckDrop -->|No| Include
    CheckDrop -->|Yes| CheckCritical2{Has critical keyword?}
    CheckCritical2 -->|Yes| Include
    CheckCritical2 -->|No| Drop3[Drop Generic 5-Star]
    
    style Include fill:#c8e6c9
    style Drop1 fill:#ffcdd2
    style Drop2 fill:#ffcdd2
    style Drop3 fill:#ffcdd2
```

## Additional Insights

### Design Patterns
- **Retry Pattern:** Tenacity decorator for fault tolerance
- **Strategy Pattern:** Configurable filtering via settings
- **Template Method:** `fetch_reviews()` orchestrates sub-methods

### Code Quality
- **Type Hints:** Full type annotations for better IDE support
- **Docstrings:** Comprehensive documentation for all public methods
- **Logging:** Structured logging at INFO/DEBUG/WARNING levels
- **Error Messages:** Clear, actionable error messages

### Testing Considerations
- **Mockable:** Apify client can be mocked for unit tests
- **Testable Logic:** Filter logic is pure function (easy to test)
- **Smoke Test Mode:** Built-in testing support via `force_fetch_count`

## Metadata

- **File:** `src/fetcher.py`
- **Lines of Code:** ~350
- **Classes:** 1 (`Fetcher`)
- **Class Constant:** `ACTOR_ID = "agents/appstore-reviews"`
- **Public Methods:** 3 (`fetch_reviews`, `filter_reviews`, `save_reviews`)
- **Private Methods:** 5 (`_extract_app_id`, `_run_apify_actor`, `_parse_review_date`, `_extract_rating`, `_extract_review_text`)
- **Dependencies:** 2 external packages (`apify_client`, `tenacity`), standard library
- **Last Updated:** 2026-02-10 (switched to agents/appstore-reviews, added country config)

## Next Steps

### Potential Improvements
1. **Extract Critical Keywords:** Load from `pain_keywords.json` instead of hardcoding
2. ~~**Country Code Config:** Make country code configurable via settings~~ ✅ Done
3. **Date Field Expansion:** Support more date field variations from Apify
4. **Caching:** Add optional caching layer for repeated fetches
5. **Parallel Processing:** Support concurrent fetching for multiple apps
6. **Actor Fallback:** Auto-switch to alternative actor if primary fails

### Related Knowledge
- **`main.py`**: Entry point that uses Fetcher → `knowledge-main.md`
- **`src/analyzer.py`**: Next step in pipeline → `knowledge-analyzer.md`
- **`src/reporter.py`**: Report generation → `knowledge-reporter.md`
- **`config/settings.json`**: Configuration schema
- **`docs/ai/design/apify-appstore-scraper.md`**: Design documentation

### Follow-up Actions
- Monitor `agents/appstore-reviews` reliability vs `thewolves` actor
- Document Apify actor input schema differences for future reference
- Create integration test examples using mock Apify responses
- Consider adding retry fallback to alternative actor on repeated failures
