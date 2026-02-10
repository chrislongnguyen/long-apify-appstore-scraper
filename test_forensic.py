#!/usr/bin/env python3
"""T-019: Forensic Unit Tests for ForensicAnalyzer."""
import sys
import time
from datetime import datetime, timezone, timedelta
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent / "src"))

import pandas as pd

from src.intelligence import ForensicAnalyzer


def _make_review(date: datetime, text: str, score: int = 2) -> dict:
    return {"date": date.isoformat(), "text": text, "score": score}


def test_detect_event_timeline():
    """Test detect_event_timeline with mock spike (50 reviews, 40 pain in week)."""
    config_dir = Path(__file__).parent / "config"
    fa = ForensicAnalyzer(pain_keywords_path=config_dir / "pain_keywords.json")

    # Build 50 reviews: 40 with "crash" (pain keyword), 10 without
    base_date = datetime.now(timezone.utc) - timedelta(days=14)
    reviews = []
    pain_text = "The app crashes constantly. Worst experience ever."
    neutral_text = "Great app, love it."
    for i in range(40):
        reviews.append(_make_review(base_date + timedelta(days=i % 7), pain_text))
    for i in range(10):
        reviews.append(_make_review(base_date + timedelta(days=i % 7), neutral_text))

    df = fa._reviews_to_dataframe(reviews)
    timeline = fa.detect_event_timeline(df, min_reviews_per_week=5)

    assert isinstance(timeline, list), "Timeline should be a list"
    if len(timeline) >= 1:
        for t in timeline:
            assert "week" in t and "density" in t, "Each entry needs week and density"
            assert 0 <= t["density"] <= 1, "Density should be 0-1"
    print("✓ PASS: detect_event_timeline returns valid structure")


def test_extract_semantic_clusters():
    """Test extract_semantic_clusters with mock text corpus."""
    config_dir = Path(__file__).parent / "config"
    fa = ForensicAnalyzer(pain_keywords_path=config_dir / "pain_keywords.json", app_name="TestApp")

    # Corpus with repeated phrases
    texts = [
        "sync failed multiple times",
        "sync failed again today",
        "premium locked behind paywall",
        "premium locked content",
        "login failed this morning",
        "login failed again",
    ] * 10  # 60 texts
    series = pd.Series(texts)

    clusters = fa.extract_semantic_clusters(series, top_n=5)

    assert isinstance(clusters, list), "Clusters should be a list"
    assert len(clusters) >= 1, "Should find at least one phrase"
    for item in clusters:
        assert isinstance(item, (tuple, dict)), "Each item is (phrase, count) or dict"
        if isinstance(item, tuple):
            assert len(item) == 2, "Tuple should be (phrase, count)"
    print("✓ PASS: extract_semantic_clusters returns valid structure")


def test_map_competitor_migration():
    """Test map_competitor_migration with churn vs comparison (T-018 strict regex)."""
    config_dir = Path(__file__).parent / "config"
    fa = ForensicAnalyzer(pain_keywords_path=config_dir / "pain_keywords.json")

    texts = pd.Series([
        "I switched to Opal and never looked back",
        "Moved to Forest for better focus",
        "Better than Opal ever was",  # Should be IGNORED (comparison)
    ])
    competitors = ["Opal", "Forest"]

    result = fa.map_competitor_migration(texts, competitors)

    # T-018: Only "switched to X" / "moved to X" count as churn
    churns = [r for r in result if r.get("type") == "churn"]
    assert any(r["competitor"] == "Opal" for r in churns), "Should detect 'switched to Opal'"
    assert any(r["competitor"] == "Forest" for r in churns), "Should detect 'moved to Forest'"
    # "Better than Opal" should NOT be in churn
    opal_churn = next((r for r in churns if r["competitor"] == "Opal"), None)
    assert opal_churn and opal_churn["count"] == 1, "Only one 'switched to Opal', not 'better than'"
    print("✓ PASS: map_competitor_migration (T-018 strict regex)")


def test_performance_500_reviews():
    """Ensure 500 reviews process in < 2.0 seconds (Req 2.2)."""
    config_dir = Path(__file__).parent / "config"
    fa = ForensicAnalyzer(pain_keywords_path=config_dir / "pain_keywords.json")

    base_date = datetime.now(timezone.utc) - timedelta(days=60)
    reviews = []
    for i in range(500):
        text = "sync failed and login failed repeatedly" if i % 5 == 0 else "generic review text here"
        reviews.append(_make_review(base_date + timedelta(days=i % 60), text, score=2 if i % 3 == 0 else 4))

    df = fa._reviews_to_dataframe(reviews)
    negative_df = df[df["score"] <= 2]

    start = time.perf_counter()
    fa.extract_semantic_clusters(negative_df["text"], top_n=5)
    elapsed = time.perf_counter() - start

    assert elapsed < 2.0, f"N-Gram processing took {elapsed:.2f}s, must be < 2.0s"
    print(f"✓ PASS: 500 reviews processed in {elapsed:.2f}s (< 2.0s)")


def test_generate_matrix():
    """Test generate_matrix produces valid niche_matrix schema."""
    config_dir = Path(__file__).parent / "config"
    fa = ForensicAnalyzer(pain_keywords_path=config_dir / "pain_keywords.json")

    analyses = [
        {"app_name": "AppA", "signals": {"pillar_densities": {"Functional": 5.0, "Economic": 2.0, "Experience": 1.0}}},
        {"app_name": "AppB", "signals": {"pillar_densities": {"Functional": 1.0, "Economic": 8.0, "Experience": 0.5}}},
    ]

    matrix = fa.generate_matrix(analyses)

    assert "AppA" in matrix and "AppB" in matrix
    assert matrix["AppA"]["Functional"] == 50.0  # 5.0 * 10
    assert matrix["AppB"]["Economic"] == 80.0  # 8.0 * 10
    print("✓ PASS: generate_matrix schema valid")


def run_all():
    """Run all forensic tests."""
    print("=" * 60)
    print("FORENSIC ANALYZER TESTS (T-019)")
    print("=" * 60)
    try:
        test_detect_event_timeline()
        test_extract_semantic_clusters()
        test_map_competitor_migration()
        test_generate_matrix()
        test_performance_500_reviews()
        print("\n" + "=" * 60)
        print("✓ All forensic tests passed")
        print("=" * 60)
        return True
    except AssertionError as e:
        print(f"\n✗ FAIL: {e}")
        return False
    except Exception as e:
        print(f"\n✗ ERROR: {e}")
        import traceback
        traceback.print_exc()
        return False


if __name__ == "__main__":
    success = run_all()
    sys.exit(0 if success else 1)
