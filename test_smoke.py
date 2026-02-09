#!/usr/bin/env python3
"""Smoke test script to verify Apify connection and filtering logic."""
import sys
import json
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent / "src"))

from src.fetcher import Fetcher
from src.config_validator import load_json_config, validate_settings_config


def test_smoke_mode():
    """Test smoke test mode with mock data."""
    print("=" * 60)
    print("SMOKE TEST: Verifying Fetcher Logic")
    print("=" * 60)
    
    # Test 1: Filter logic (drop 5-stars)
    print("\n1. Testing filter_reviews() logic...")
    
    # Create mock reviews
    mock_reviews = [
        {"rating": 5, "text": "Great app!"},
        {"rating": 5, "text": "Love it! Perfect!"},
        {"rating": 5, "text": "Scam! This app crashes constantly!"},  # Should keep (critical keyword)
        {"rating": 4, "text": "Good but could be better"},
        {"rating": 3, "text": "Average"},
        {"rating": 2, "text": "Not great"},
        {"rating": 1, "text": "Terrible"},
    ]
    
    # Load settings for testing
    config_dir = Path(__file__).parent / "config"
    try:
        settings = load_json_config(config_dir / "settings.json")
        validate_settings_config(settings)
    except Exception as e:
        print(f"   ✗ FAIL: Could not load settings.json: {e}")
        return False
    
    # Initialize fetcher with settings (won't actually connect without token)
    try:
        fetcher = Fetcher(apify_token="test_token", settings=settings)
    except Exception as e:
        print(f"   ⚠ WARNING: Could not initialize Fetcher (expected in test): {e}")
        # Fallback: test with mock settings
        class TestFetcher:
            def __init__(self, settings):
                self.settings = settings
                self.filters = settings.get("filters", {})
            
            def filter_reviews(self, reviews):
                from src.fetcher import Fetcher
                # Use actual filter logic with settings
                fetcher = Fetcher.__new__(Fetcher)
                fetcher.settings = self.settings
                fetcher.filters = self.filters
                return fetcher.filter_reviews(reviews)
        
        fetcher = TestFetcher(settings)
    
    filtered = fetcher.filter_reviews(mock_reviews)
    
    print(f"   Input: {len(mock_reviews)} reviews")
    print(f"   Output: {len(filtered)} reviews (dropped {len(mock_reviews) - len(filtered)} 5-star reviews)")
    
    # Verify: Should keep 5 reviews (4, 3, 2, 1 stars + 1 critical 5-star)
    expected_count = 5
    if len(filtered) == expected_count:
        print(f"   ✓ PASS: Correctly filtered to {expected_count} reviews")
    else:
        print(f"   ✗ FAIL: Expected {expected_count} reviews, got {len(filtered)}")
        return False
    
    # Verify: No generic 5-star reviews
    generic_5_stars = [r for r in filtered if r.get("rating") == 5 and "scam" not in r.get("text", "").lower()]
    if len(generic_5_stars) == 0:
        print("   ✓ PASS: No generic 5-star reviews in filtered output")
    else:
        print(f"   ✗ FAIL: Found {len(generic_5_stars)} generic 5-star reviews")
        return False
    
    # Test 2: Config loading
    print("\n2. Testing config loading...")
    try:
        config_dir = Path(__file__).parent / "config"
        targets = load_json_config(config_dir / "targets.json")
        print(f"   ✓ PASS: Loaded {len(targets['apps'])} app(s) from targets.json")
        
        pain_keywords = load_json_config(config_dir / "pain_keywords.json")
        print(f"   ✓ PASS: Loaded {len(pain_keywords['categories'])} categories from pain_keywords.json")
        
        settings = load_json_config(config_dir / "settings.json")
        validate_settings_config(settings)
        print(f"   ✓ PASS: Loaded settings.json (min_star_rating={settings['filters']['min_star_rating']})")
    except Exception as e:
        print(f"   ✗ FAIL: Config loading error: {e}")
        return False
    
    print("\n" + "=" * 60)
    print("✓ ALL SMOKE TESTS PASSED")
    print("=" * 60)
    print("\nNext step: Run with --smoke-test flag to test Apify connection:")
    print("  python main.py --smoke-test")
    print("\nMake sure APIFY_API_KEY is set in your environment.")
    
    return True


if __name__ == "__main__":
    success = test_smoke_mode()
    sys.exit(0 if success else 1)
