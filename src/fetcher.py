"""Fetcher class for retrieving App Store reviews via Apify API."""
import os
import json
import logging
from typing import List, Dict, Any, Optional
from pathlib import Path
from datetime import datetime, timedelta

from apify_client import ApifyClient
from tenacity import retry, stop_after_attempt, wait_exponential, retry_if_exception_type

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class Fetcher:
    """
    Handles reliable fetching of App Store reviews using Apify actor.
    
    Responsibilities:
    - Connect to Apify API with retry logic
    - Fetch reviews for target apps
    - Handle errors gracefully
    - Filter and save reviews (thrifty - drop 5-stars)
    """
    
    # Apify actor ID for App Store Reviews Scraper
    # Using agents/appstore-reviews which is faster (200 reviews/sec) and more reliable
    # Alternative: "thewolves/appstore-reviews-scraper" (if agents version has issues)
    ACTOR_ID = "agents/appstore-reviews"
    
    def __init__(self, apify_token: Optional[str] = None, settings: Optional[Dict[str, Any]] = None):
        """
        Initialize the Fetcher.
        
        Args:
            apify_token: Apify API token (optional, defaults to APIFY_API_KEY env var)
            settings: Settings configuration dictionary (from settings.json)
            
        Raises:
            ValueError: If no API token is provided and APIFY_API_KEY env var is not set
        """
        self.apify_token = apify_token or os.getenv("APIFY_API_KEY")
        if not self.apify_token:
            raise ValueError(
                "Apify API token required. Provide via parameter or set APIFY_API_KEY environment variable."
            )
        
        self.client = ApifyClient(self.apify_token)
        self.settings = settings or {}
        self.filters = self.settings.get("filters", {})
        logger.info("Apify client initialized successfully")
    
    def _extract_app_id(self, app_url: str) -> Optional[str]:
        """
        Extract App Store ID from URL.
        
        Args:
            app_url: App Store URL (e.g., https://apps.apple.com/us/app/voicenotes-ai/id6499420042)
            
        Returns:
            App ID as string (e.g., "6499420042") or None if extraction fails
        """
        import re
        # Pattern: /id followed by digits at the end of the URL
        match = re.search(r'/id(\d+)', app_url)
        if match:
            return match.group(1)
        return None
    
    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=2, max=10),
        retry=retry_if_exception_type((ConnectionError, TimeoutError)),
        reraise=True
    )
    def _run_apify_actor(self, app_url: str, max_items: int) -> List[Dict[str, Any]]:
        """
        Run Apify actor with retry logic.
        
        Args:
            app_url: App Store URL (must be a string)
            max_items: Maximum number of reviews to fetch
            
        Returns:
            List of review dictionaries from Apify dataset
            
        Raises:
            Exception: If API call fails after retries
        """
        # Validate URL is a string
        if not isinstance(app_url, str):
            raise ValueError(f"app_url must be a string, got {type(app_url)}: {app_url}")
        
        # Ensure URL is not empty
        if not app_url or not app_url.strip():
            raise ValueError(f"app_url cannot be empty")
        
        logger.info(f"Fetching reviews from Apify actor: {app_url} (max_items={max_items})")
        
        try:
            # Extract App ID from URL - more reliable than passing full URL
            # The Apify actor documentation states appIds should be "without id"
            app_id = self._extract_app_id(app_url)
            
            # Build run input - prefer appIds over startUrls for reliability
            # App Store reviews are geo-fenced - must explicitly set country
            # Use "all" to search all countries (useful for niche apps with limited US reviews)
            country = self.filters.get("country", "us")
            run_input = {
                "maxItems": max_items,
                "country": country,  # App Store country - "us", "gb", "all", etc.
            }
            logger.info(f"Using country: {country}")
            
            if app_id:
                # Use appIds (more reliable) - array of ID strings without "id" prefix
                run_input["appIds"] = [app_id]
                logger.info(f"Using App ID: {app_id}")
            else:
                # Fallback to startUrls if ID extraction fails
                run_input["startUrls"] = [str(app_url).strip()]
                logger.warning(f"Could not extract App ID, falling back to URL")
            
            logger.debug(f"Apify input: {run_input}")
            
            run = self.client.actor(self.ACTOR_ID).call(run_input=run_input)
            
            # Wait for the run to finish and get results
            dataset_items = list(self.client.dataset(run["defaultDatasetId"]).iterate_items())
            
            # Filter out error responses from Apify
            valid_reviews = []
            for item in dataset_items:
                if item.get("error") or item.get("noResults"):
                    logger.warning(f"Apify returned error: {item.get('message', 'Unknown error')}")
                    continue
                valid_reviews.append(item)
            
            logger.info(f"Successfully fetched {len(valid_reviews)} reviews from Apify (raw: {len(dataset_items)})")
            
            return valid_reviews
            
        except Exception as e:
            logger.error(f"Apify actor call failed: {e}")
            raise
    
    def fetch_reviews(
        self,
        app_url: str,
        days_back: int = 90,
        max_reviews: int = 500,
        smoke_test: bool = False
    ) -> List[Dict[str, Any]]:
        """
        Fetch reviews for a given app URL.
        
        Args:
            app_url: App Store URL (must be a string)
            days_back: Number of days to look back (used for filtering after fetch)
            max_reviews: Maximum number of reviews to fetch from Apify
            smoke_test: If True, limit to configured fetch count for testing
            
        Returns:
            List of review dictionaries
            
        Raises:
            Exception: If API call fails after retries
        """
        # Validate URL parameter
        if not isinstance(app_url, str):
            raise ValueError(f"app_url must be a string, got {type(app_url)}: {app_url}")
        
        # Smoke test mode: limit to configured fetch count or default 10
        if smoke_test:
            force_fetch_count = self.filters.get("force_fetch_count", 10)
            max_reviews = force_fetch_count
            logger.info(f"🔥 SMOKE TEST MODE: Limiting to {max_reviews} reviews")
        
        # Fetch reviews from Apify
        reviews = self._run_apify_actor(app_url, max_reviews)
        
        # Filter by date if needed (Apify may return more than requested)
        # Use timezone-aware datetime for comparison
        from datetime import timezone
        cutoff_date = datetime.now(timezone.utc) - timedelta(days=days_back)
        filtered_reviews = []
        
        for review in reviews:
            # Parse review date (format may vary, handle common formats)
            review_date = self._parse_review_date(review)
            if review_date:
                # Make review_date timezone-aware if it's naive
                if review_date.tzinfo is None:
                    review_date = review_date.replace(tzinfo=timezone.utc)
                
                if review_date >= cutoff_date:
                    filtered_reviews.append(review)
            else:
                # If date parsing fails, include the review (better safe than sorry)
                filtered_reviews.append(review)
        
        logger.info(f"Filtered to {len(filtered_reviews)} reviews within last {days_back} days")
        return filtered_reviews
    
    def _parse_review_date(self, review: Dict[str, Any]) -> Optional[datetime]:
        """
        Parse review date from various possible formats.
        
        Args:
            review: Review dictionary
            
        Returns:
            Parsed datetime or None if parsing fails
        """
        date_fields = ["date", "reviewDate", "createdAt", "updatedAt"]
        
        for field in date_fields:
            if field in review and review[field]:
                try:
                    # Try ISO format first
                    if isinstance(review[field], str):
                        return datetime.fromisoformat(review[field].replace("Z", "+00:00"))
                    elif isinstance(review[field], (int, float)):
                        # Unix timestamp
                        return datetime.fromtimestamp(review[field])
                except (ValueError, TypeError):
                    continue
        
        return None
    
    def filter_reviews(self, reviews: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Filter reviews based on settings.json configuration.
        
        Thrifty filtering: Configurable filtering based on min_star_rating and drop_generic_5_star.
        Keep reviews with:
        - Rating >= min_star_rating (from settings)
        - Or rating == 5 but contains critical keywords (if drop_generic_5_star is true)
        
        Args:
            reviews: Raw review list
            
        Returns:
            Filtered review list
        """
        filtered = []
        dropped_count = 0
        
        # Get filter settings (with defaults for backward compatibility)
        min_star_rating = self.filters.get("min_star_rating", 4)
        drop_generic_5_star = self.filters.get("drop_generic_5_star", True)
        min_review_length = self.filters.get("min_review_length_words", 3)
        
        # Critical keywords that should keep a 5-star review (from pain_keywords.json categories)
        # These are extracted from the critical category keywords
        critical_keywords = ["scam", "crash", "fraud", "broken", "error", "bug", "lừa", "sập", "lỗi"]
        
        for review in reviews:
            rating = self._extract_rating(review)
            review_text = self._extract_review_text(review)
            
            # Skip if rating is missing (better safe than sorry - keep it)
            if rating is None:
                filtered.append(review)
                continue
            
            # Check minimum star rating threshold
            if rating < min_star_rating:
                dropped_count += 1
                continue
            
            # Check minimum review length (unless it contains critical keywords)
            word_count = len(review_text.split())
            has_critical_keyword = any(keyword in review_text.lower() for keyword in critical_keywords)
            
            if word_count < min_review_length and not has_critical_keyword:
                dropped_count += 1
                continue
            
            # Handle 5-star reviews based on drop_generic_5_star setting
            # If min_star_rating <= 3, include ALL reviews (including all 5-stars)
            # Only apply drop_generic_5_star when min_star_rating >= 4 (filtering for high ratings)
            # Special case: if min_star_rating == 5, we want ALL 5-star reviews (don't drop generic ones)
            if rating == 5:
                # If min_star_rating is exactly 5, include ALL 5-star reviews (user wants only 5-stars)
                if min_star_rating == 5:
                    filtered.append(review)
                elif drop_generic_5_star and min_star_rating >= 4:
                    # Only drop generic 5-stars when filtering for high ratings (>=4) but not when min_star_rating == 5
                    # Keep 5-star reviews with critical keywords
                    if has_critical_keyword:
                        filtered.append(review)
                        logger.debug(f"Kept 5-star review with critical keyword: {review_text[:50]}...")
                    else:
                        dropped_count += 1
                else:
                    # Include all 5-star reviews if min_star_rating <= 3 or drop_generic_5_star is False
                    filtered.append(review)
            else:
                # Keep all non-5-star reviews that pass the threshold
                filtered.append(review)
        
        logger.info(
            f"Filtered reviews: {len(filtered)} kept, {dropped_count} dropped "
            f"(min_rating={min_star_rating}, drop_5star={drop_generic_5_star})"
        )
        return filtered
    
    def _extract_rating(self, review: Dict[str, Any]) -> Optional[int]:
        """Extract rating from review dictionary."""
        rating_fields = ["rating", "starRating", "stars", "score"]
        
        for field in rating_fields:
            if field in review:
                try:
                    rating = int(review[field])
                    if 1 <= rating <= 5:
                        return rating
                except (ValueError, TypeError):
                    continue
        
        return None
    
    def _extract_review_text(self, review: Dict[str, Any]) -> str:
        """Extract review text from review dictionary."""
        text_fields = ["text", "reviewText", "content", "body", "comment"]
        
        for field in text_fields:
            if field in review and review[field]:
                return str(review[field])
        
        return ""
    
    def save_reviews(self, reviews: List[Dict[str, Any]], output_path: Path) -> None:
        """
        Save filtered reviews to disk as JSON.
        
        Args:
            reviews: Filtered review list
            output_path: Path to save JSON file
        """
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(reviews, f, indent=2, ensure_ascii=False, default=str)
        
        logger.info(f"Saved {len(reviews)} filtered reviews to {output_path}")
