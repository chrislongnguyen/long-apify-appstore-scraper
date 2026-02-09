#!/usr/bin/env python3
"""Test script to verify config changes work (e.g., min_star_rating = 1 shows 5-star reviews)."""
import sys
import json
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent / "src"))

from src.fetcher import Fetcher
from src.config_validator import load_json_config, validate_settings_config


def test_config_change():
    """Test that changing min_star_rating to 1 includes 5-star reviews."""
    print("=" * 60)
    print("CONFIG CHANGE TEST: min_star_rating = 1")
    print("=" * 60)
    
    config_dir = Path(__file__).parent / "config"
    
    # Load current settings
    settings = load_json_config(config_dir / "settings.json")
    original_min_rating = settings["filters"]["min_star_rating"]
    
    print(f"\nCurrent min_star_rating: {original_min_rating}")
    
    # Create test reviews with various ratings (using longer text to pass min_review_length check)
    mock_reviews = [
        {"rating": 5, "text": "Great app! I love using it every day."},
        {"rating": 5, "text": "Love it! Perfect for my needs and works great."},
        {"rating": 4, "text": "Good but could be better in some areas."},
        {"rating": 3, "text": "Average app with some good features."},
        {"rating": 2, "text": "Not great, has some issues that need fixing."},
        {"rating": 1, "text": "Terrible experience, would not recommend to anyone."},
    ]
    
    # Test 1: With min_star_rating = 4 (default)
    print("\n1. Testing with min_star_rating = 4 (default)...")
    settings_test1 = settings.copy()
    settings_test1["filters"] = settings["filters"].copy()
    settings_test1["filters"]["min_star_rating"] = 4
    
    try:
        fetcher1 = Fetcher(apify_token="test_token", settings=settings_test1)
        filtered1 = fetcher1.filter_reviews(mock_reviews)
        print(f"   Input: {len(mock_reviews)} reviews")
        print(f"   Output: {len(filtered1)} reviews")
        print(f"   5-star reviews in output: {sum(1 for r in filtered1 if r.get('rating') == 5)}")
    except Exception as e:
        print(f"   ⚠ Could not test (expected): {e}")
        # Manual test
        filtered1 = [r for r in mock_reviews if r.get("rating", 0) >= 4]
        print(f"   Manual test: {len(filtered1)} reviews (should include 5-stars)")
    
    # Test 2: With min_star_rating = 1 (should include all)
    print("\n2. Testing with min_star_rating = 1...")
    settings_test2 = settings.copy()
    settings_test2["filters"] = settings["filters"].copy()
    settings_test2["filters"]["min_star_rating"] = 1
    
    try:
        fetcher2 = Fetcher(apify_token="test_token", settings=settings_test2)
        filtered2 = fetcher2.filter_reviews(mock_reviews)
        print(f"   Input: {len(mock_reviews)} reviews")
        print(f"   Output: {len(filtered2)} reviews")
        print(f"   5-star reviews in output: {sum(1 for r in filtered2 if r.get('rating') == 5)}")
        
        if len(filtered2) == len(mock_reviews):
            print("   ✓ PASS: All reviews included when min_star_rating = 1")
        else:
            print(f"   ✗ FAIL: Expected {len(mock_reviews)} reviews, got {len(filtered2)}")
            return False
        
        if sum(1 for r in filtered2 if r.get("rating") == 5) == 2:
            print("   ✓ PASS: Both 5-star reviews included")
        else:
            print("   ✗ FAIL: Expected 2 five-star reviews")
            return False
            
    except Exception as e:
        print(f"   ✗ FAIL: Error testing: {e}")
        import traceback
        traceback.print_exc()
        return False
    
    print("\n" + "=" * 60)
    print("✓ CONFIG CHANGE TEST PASSED")
    print("=" * 60)
    print("\nTo test in production:")
    print("1. Edit config/settings.json: set 'min_star_rating' to 1")
    print("2. Run: python main.py --smoke-test")
    print("3. Check data/*_reviews.json - should include 5-star reviews")
    
    return True


if __name__ == "__main__":
    success = test_config_change()
    sys.exit(0 if success else 1)
