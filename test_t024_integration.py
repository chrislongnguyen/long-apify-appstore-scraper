#!/usr/bin/env python3
"""T-024 Integration Test: Verify predictive metrics in reports (no Apify fetch)."""
import json
import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / "src"))

from src.config_validator import load_json_config
from src.analyzer import Analyzer
from src.intelligence import ForensicAnalyzer
from src.reporter import Reporter


def main():
    """Run analyzer + forensic + reporter on existing Tattoo_AI data."""
    config_dir = Path(__file__).parent / "config"
    data_dir = Path(__file__).parent / "data" / "Tattoo_AI"
    reports_dir = Path(__file__).parent / "reports" / "Tattoo_AI"
    reports_dir.mkdir(parents=True, exist_ok=True)
    
    settings = load_json_config(config_dir / "settings.json")
    analyzer = Analyzer(
        pain_keywords_path=config_dir / "pain_keywords.json",
        settings=settings,
    )
    forensic_analyzer = ForensicAnalyzer(pain_keywords_path=config_dir / "pain_keywords.json")
    reporter = Reporter(output_dir=reports_dir)
    
    # Load first app's reviews
    reviews_file = data_dir / "tattoo_ai_design_reviews.json"
    if not reviews_file.exists():
        print(f"✗ Not found: {reviews_file}")
        return 1
    
    with open(reviews_file, "r", encoding="utf-8") as f:
        reviews = json.load(f)
    
    print(f"Loaded {len(reviews)} reviews from {reviews_file.name}")
    
    # Analyze
    analysis = analyzer.analyze(
        reviews=reviews,
        app_name="Tattoo_AI_Design",
        days_back=90,
    )
    
    # Verify predictive fields
    signals = analysis.get("signals", {})
    assert "monthly_leakage_usd" in signals, "Missing monthly_leakage_usd"
    assert "slope_delta" in signals, "Missing slope_delta"
    assert "slope_delta_insight" in signals, "Missing slope_delta_insight"
    print(f"✓ Predictive metrics: leakage=${signals['monthly_leakage_usd']}, "
          f"slope_delta={signals['slope_delta']}, insight={signals['slope_delta_insight']}")
    
    # Forensic
    forensic = forensic_analyzer.run_forensic(
        reviews=reviews,
        app_name="Tattoo_AI_Design",
        competitors=["Ai_Tattoo_Ideas_Art", "AI_Ink_Tattoo_Gen"],
    )
    
    # Generate report
    report_path = reporter.generate_report(
        app_name="Tattoo_AI_Design",
        analysis=analysis,
        reviews=reviews,
        forensic=forensic,
    )
    print(f"✓ Generated report: {report_path}")
    
    # Verify report content
    content = report_path.read_text()
    assert "Financial Impact" in content, "Report missing Financial Impact section"
    assert "Estimated Monthly Revenue Leakage" in content, "Report missing leakage"
    assert "Trend Acceleration" in content, "Report missing trend acceleration"
    print("✓ Report contains Financial Impact section")
    
    # Save analysis for leaderboard test
    analyzer.save_analysis(analysis, data_dir / "tattoo_ai_design_analysis.json")
    
    # Aggregate leaderboard (uses all analyses in data dir)
    leaderboard_path = reporter.aggregate_leaderboard(data_dir=data_dir)
    print(f"✓ Generated leaderboard: {leaderboard_path}")
    
    leaderboard_content = leaderboard_path.read_text()
    assert "Revenue Leakage" in leaderboard_content, "Leaderboard missing Revenue Leakage"
    assert "Momentum" in leaderboard_content, "Leaderboard missing Momentum"
    print("✓ Leaderboard contains Revenue Leakage and Momentum columns")
    
    print("\n✓ T-024 Integration test passed")
    return 0


if __name__ == "__main__":
    sys.exit(main())
