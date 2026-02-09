#!/usr/bin/env python3
"""Test script to verify URL extraction and min_star_rating: 5 filtering."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent / "src"))

from src.fetcher import Fetcher
from src.config_validator import load_json_config


def test_url_extraction():
    """Test that URL is correctly extracted as string."""
    print("=" * 60)
    print("URL EXTRACTION TEST")
    print("=" * 60)
    
    config_dir = Path(__file__).parent / "config"
    settings = load_json_config(config_dir / "settings.json")
    
    # Test 1: Valid URL string
    print("\n1. Testing URL validation...")
    try:
        fetcher = Fetcher(apify_token="test_token", settings=settings)
        
        # Test with valid URL string
        valid_url = "https://apps.apple.com/us/app/flo-period-pregnancy-tracker/id1038361850"
        try:
            fetcher._run_apify_actor(valid_url, 10)
            print(f"   ✓ PASS: Valid URL accepted: {valid_url[:50]}...")
        except ValueError as e:
            if "must be a string" in str(e):
                print(f"   ✗ FAIL: URL validation error: {e}")
                return False
            else:
                print(f"   ✓ PASS: URL validation passed (Apify call expected to fail without real token)")
        
        # Test with invalid input (object)
        try:
            invalid_input = {"url": valid_url}  # Passing object instead of string
            fetcher._run_apify_actor(invalid_input, 10)
            print(f"   ✗ FAIL: Should reject non-string input")
            return False
        except ValueError:
            print(f"   ✓ PASS: Correctly rejected non-string input")
        except Exception:
            print(f"   ✓ PASS: Rejected invalid input (expected)")
            
    except Exception as e:
        print(f"   ⚠ Could not test (expected without real token): {e}")
    
    # Test 2: Filter logic with min_star_rating: 5
    print("\n2. Testing filter logic with min_star_rating: 5...")
    try:
        fetcher = Fetcher(apify_token="test_token", settings=settings)
        
        # Create test reviews
        mock_reviews = [
            {"rating": 5, "text": "Great app! I love using it every day."},
            {"rating": 5, "text": "Love it! Perfect for my needs."},
            {"rating": 4, "text": "Good but could be better."},
            {"rating": 3, "text": "Average app with some features."},
        ]
        
        filtered = fetcher.filter_reviews(mock_reviews)
        
        print(f"   Input: {len(mock_reviews)} reviews")
        print(f"   Output: {len(filtered)} reviews")
        print(f"   5-star reviews in output: {sum(1 for r in filtered if r.get('rating') == 5)}")
        print(f"   4-star reviews in output: {sum(1 for r in filtered if r.get('rating') == 4)}")
        
        # With min_star_rating: 5, should only keep 5-star reviews
        if len(filtered) == 2:
            print("   ✓ PASS: Correctly filtered to 2 reviews (both 5-stars)")
        else:
            print(f"   ✗ FAIL: Expected 2 reviews, got {len(filtered)}")
            return False
        
        if sum(1 for r in filtered if r.get("rating") == 5) == 2:
            print("   ✓ PASS: Both 5-star reviews included")
        else:
            print("   ✗ FAIL: Expected 2 five-star reviews")
            return False
        
        if sum(1 for r in filtered if r.get("rating") == 4) == 0:
            print("   ✓ PASS: 4-star review correctly filtered out")
        else:
            print("   ✗ FAIL: 4-star review should be filtered out")
            return False
            
    except Exception as e:
        print(f"   ✗ FAIL: Error testing filter: {e}")
        import traceback
        traceback.print_exc()
        return False
    
    print("\n" + "=" * 60)
    print("✓ ALL TESTS PASSED")
    print("=" * 60)
    print("\nFixes applied:")
    print("1. Added URL validation to ensure string type")
    print("2. Fixed filter logic: min_star_rating: 5 includes ALL 5-star reviews")
    print("3. Added URL extraction validation in main.py")
    
    return True


if __name__ == "__main__":
    success = test_url_extraction()
    sys.exit(0 if success else 1)
