#!/usr/bin/env python3
"""Test script to verify Analyzer implementation with sample data."""
import sys
import json
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent / "src"))

from src.analyzer import Analyzer
from src.config_validator import load_json_config


def test_analyzer():
    """Test analyzer with Instagram reviews data."""
    print("=" * 60)
    print("ANALYZER TEST: Phase 3 Implementation")
    print("=" * 60)
    
    config_dir = Path(__file__).parent / "config"
    data_dir = Path(__file__).parent / "data"
    
    # Load configurations
    try:
        settings = load_json_config(config_dir / "settings.json")
        pain_keywords = load_json_config(config_dir / "pain_keywords.json")
        print("✓ Configurations loaded")
    except Exception as e:
        print(f"✗ Config loading failed: {e}")
        return False
    
    # Initialize analyzer
    try:
        analyzer = Analyzer(
            pain_keywords_path=config_dir / "pain_keywords.json",
            settings=settings
        )
        print("✓ Analyzer initialized")
    except Exception as e:
        print(f"✗ Analyzer initialization failed: {e}")
        return False
    
    # Load sample reviews
    reviews_file = data_dir / "instagram_reviews.json"
    if not reviews_file.exists():
        print(f"✗ Reviews file not found: {reviews_file}")
        print("  Run: python main.py --smoke-test first")
        return False
    
    try:
        with open(reviews_file, 'r', encoding='utf-8') as f:
            reviews = json.load(f)
        print(f"✓ Loaded {len(reviews)} reviews from {reviews_file}")
    except Exception as e:
        print(f"✗ Failed to load reviews: {e}")
        return False
    
    # Run analysis
    print("\nRunning analysis...")
    try:
        analysis = analyzer.analyze(
            reviews=reviews,
            app_name="Instagram",
            days_back=90
        )
        
        print("\n" + "=" * 60)
        print("ANALYSIS RESULTS")
        print("=" * 60)
        print(f"App: {analysis['app_name']}")
        print(f"Analysis Date: {analysis['analysis_date']}")
        print(f"\nMetrics:")
        print(f"  Total Reviews (90d): {analysis['metrics']['total_reviews_90d']}")
        print(f"  Negative Ratio: {analysis['metrics']['negative_ratio']:.2%}")
        print(f"  Volatility Slope: {analysis['metrics']['volatility_slope']:.4f}")
        print(f"  Risk Score: {analysis['metrics']['risk_score']}")
        print(f"\nSignals:")
        print(f"  Broken Update Detected: {analysis['signals']['broken_update_detected']}")
        print(f"  Suspected Version: {analysis['signals']['suspected_version']}")
        print(f"  Top Pain Categories: {len(analysis['signals']['top_pain_categories'])}")
        for cat in analysis['signals']['top_pain_categories'][:3]:
            print(f"    - {cat['category']}: {cat['count']} reviews (weight: {cat['weight']})")
        print(f"\nEvidence Samples: {len(analysis['evidence'])}")
        
        # Verify schema structure
        required_keys = ['app_name', 'analysis_date', 'metrics', 'signals', 'evidence']
        missing_keys = [key for key in required_keys if key not in analysis]
        if missing_keys:
            print(f"\n✗ FAIL: Missing required keys: {missing_keys}")
            return False
        
        required_metrics = ['total_reviews_90d', 'negative_ratio', 'volatility_slope', 'risk_score']
        missing_metrics = [m for m in required_metrics if m not in analysis['metrics']]
        if missing_metrics:
            print(f"\n✗ FAIL: Missing required metrics: {missing_metrics}")
            return False
        
        print("\n✓ PASS: Analysis completed successfully")
        print("✓ PASS: Schema structure is correct")
        
        # Save test output
        test_output = data_dir / "instagram_analysis_test.json"
        analyzer.save_analysis(analysis, test_output)
        print(f"✓ Saved test analysis to {test_output}")
        
        return True
        
    except Exception as e:
        print(f"\n✗ FAIL: Analysis failed: {e}")
        import traceback
        traceback.print_exc()
        return False


if __name__ == "__main__":
    success = test_analyzer()
    sys.exit(0 if success else 1)
