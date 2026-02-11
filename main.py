#!/usr/bin/env python3
"""Main entry point for App Store Volatility Analyzer."""
from dotenv import load_dotenv

load_dotenv()

import json
import sys
import os
import argparse
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / "src"))

from src.config_validator import (
    load_json_config,
    validate_targets_config,
    validate_pain_keywords_config,
    validate_settings_config
)
from src.fetcher import Fetcher
from src.analyzer import Analyzer
from src.reporter import Reporter
from src.intelligence import ForensicAnalyzer


def main():
    """Main execution function."""
    parser = argparse.ArgumentParser(description="App Store Volatility Analyzer")
    parser.add_argument(
        "--smoke-test",
        action="store_true",
        help="Smoke test mode: limit to configured reviews for first app only"
    )
    parser.add_argument(
        "--apify-token",
        type=str,
        default=None,
        help="Apify API token (or set APIFY_API_KEY env var)"
    )
    args = parser.parse_args()
    
    config_dir = Path(__file__).parent / "config"
    base_data = Path(__file__).parent / "data"
    base_reports = Path(__file__).parent / "reports"
    
    # Load and validate configurations
    try:
        targets_config = load_json_config(config_dir / "targets.json")
        validate_targets_config(targets_config)
        
        # T-016: Dynamic Niche Directories - use subfolders when niche_name is set
        niche_name = targets_config.get("niche_name", "default")
        niche_name = str(niche_name).replace(" ", "_").strip() or "default"
        data_dir = base_data / niche_name
        reports_dir = base_reports / niche_name
        data_dir.mkdir(parents=True, exist_ok=True)
        reports_dir.mkdir(parents=True, exist_ok=True)
        
        pain_keywords_config = load_json_config(config_dir / "pain_keywords.json")
        validate_pain_keywords_config(pain_keywords_config)
        
        settings_config = load_json_config(config_dir / "settings.json")
        validate_settings_config(settings_config)
        
        print("✓ Configuration files validated")
        
    except Exception as e:
        print(f"✗ Configuration error: {e}")
        sys.exit(1)
    
    # Initialize components with settings
    try:
        fetcher = Fetcher(apify_token=args.apify_token, settings=settings_config)
        print("✓ Apify client connected successfully")
    except Exception as e:
        print(f"✗ Failed to initialize Apify client: {e}")
        sys.exit(1)
    
    analyzer = Analyzer(
        pain_keywords_path=config_dir / "pain_keywords.json",
        settings=settings_config
    )
    reporter = Reporter(output_dir=reports_dir)
    forensic_analyzer = ForensicAnalyzer(pain_keywords_path=config_dir / "pain_keywords.json")
    
    # Get apps to process (smoke test: only first app)
    apps_to_process = targets_config["apps"]
    if args.smoke_test:
        apps_to_process = apps_to_process[:1]
        print("\n🔥 SMOKE TEST MODE: Processing first app only, limiting to configured reviews")
    else:
        print(f"\n📋 Processing {len(apps_to_process)} apps from targets.json")
    
    # Track processing results
    successful_apps = []
    failed_apps = []
    analyses_for_niche = []  # Collect analyses for niche report
    forensic_by_app = {}  # Collect forensic data per app for niche report
    
    # Process each app
    for idx, app in enumerate(apps_to_process, 1):
        print(f"\n{'='*60}")
        print(f"[{idx}/{len(apps_to_process)}] Processing: {app['name']}")
        print(f"URL: {app['url']}")
        print(f"{'='*60}")
        
        try:
            # Fetch reviews - ensure we extract URL as string
            app_url = str(app.get("url", "")).strip()
            if not app_url:
                raise ValueError(f"App '{app.get('name', 'Unknown')}' has no valid URL")
            
            params = targets_config["params"]
            reviews = fetcher.fetch_reviews(
                app_url=app_url,
                days_back=params["days_back"],
                max_reviews=params["max_reviews"],
                smoke_test=args.smoke_test
            )
            
            print(f"✓ Fetched {len(reviews)} reviews from Apify")
            
            # Filter reviews (T-005: Drop 5-stars before saving)
            filtered_reviews = fetcher.filter_reviews(reviews)
            print(f"✓ Filtered to {len(filtered_reviews)} reviews (dropped {len(reviews) - len(filtered_reviews)} 5-star reviews)")
            
            # Save filtered reviews to disk
            app_safe_name = app["name"].replace(" ", "_").lower()
            reviews_file = data_dir / f"{app_safe_name}_reviews.json"
            fetcher.save_reviews(filtered_reviews, reviews_file)
            print(f"✓ Saved filtered reviews to {reviews_file}")
            
            # Analyze reviews (T-006, T-007: Calc Logic & Score Risk)
            if filtered_reviews:
                print(f"\nAnalyzing {len(filtered_reviews)} reviews...")
                # T-020: Pass app_config for Fermi (price, niche_category from targets)
                app_config = {}
                if "price" in app:
                    app_config["price"] = app["price"]
                if "niche_category" in app:
                    app_config["niche_category"] = app["niche_category"]
                elif targets_config.get("niche_category"):
                    app_config["niche_category"] = targets_config["niche_category"]
                analysis = analyzer.analyze(
                    reviews=filtered_reviews,
                    app_name=app["name"],
                    days_back=params["days_back"],
                    app_config=app_config if app_config else None,
                )
                
                # Save analysis results (schema_app_gap.json)
                analysis_file = data_dir / f"{app_safe_name}_analysis.json"
                analyzer.save_analysis(analysis, analysis_file)
                print(f"✓ Saved analysis results to {analysis_file}")
                print(f"  Risk Score: {analysis['metrics']['risk_score']}")
                print(f"  Volatility Slope: {analysis['metrics']['volatility_slope']:.4f}")
                print(f"  Negative Ratio: {analysis['metrics']['negative_ratio']:.2%}")
                
                successful_apps.append(app["name"])
                analyses_for_niche.append(analysis)
                
                # T-008: Forensic Intelligence - Run forensic analysis and generate report
                competitor_names = [a["name"].replace(" ", "_") for a in targets_config["apps"]]
                forensic = forensic_analyzer.run_forensic(
                    reviews=filtered_reviews,
                    app_name=app["name"],
                    competitors=competitor_names,
                )
                # Save intelligence.json
                intel_file = reports_dir / f"{app_safe_name}_intelligence.json"
                with open(intel_file, "w", encoding="utf-8") as f:
                    json.dump(forensic, f, indent=2, ensure_ascii=False)
                print(f"✓ Saved forensic intelligence to {intel_file}")
                
                report_path = reporter.generate_report(
                    app_name=app["name"],
                    analysis=analysis,
                    reviews=filtered_reviews,
                    forensic=forensic,
                )
                print(f"✓ Generated report: {report_path}")
                forensic_by_app[app["name"]] = forensic
            else:
                print("⚠ No reviews to analyze")
                successful_apps.append(f"{app['name']} (no reviews)")
            
        except KeyboardInterrupt:
            print(f"\n⚠ Processing interrupted by user")
            print(f"  Completed: {len(successful_apps)} apps")
            print(f"  Remaining: {len(apps_to_process) - idx} apps")
            sys.exit(0)
        except Exception as e:
            error_msg = str(e)
            print(f"\n✗ ERROR processing {app['name']}: {error_msg}")
            
            # Log full traceback for debugging (but don't stop execution)
            import traceback
            print(f"\nError details:")
            traceback.print_exc()
            
            failed_apps.append({
                "name": app["name"],
                "error": error_msg
            })
            
            # In smoke test mode, fail fast
            if args.smoke_test:
                print(f"\n🔥 SMOKE TEST MODE: Failing fast after error")
                sys.exit(1)
            
            # In normal mode, continue to next app
            print(f"⚠ Continuing to next app...\n")
            continue
    
    # Final summary
    print(f"\n{'='*60}")
    print("PROCESSING SUMMARY")
    print(f"{'='*60}")
    print(f"Total apps: {len(apps_to_process)}")
    print(f"✓ Successful: {len(successful_apps)}")
    if successful_apps:
        for app_name in successful_apps:
            print(f"  - {app_name}")
    print(f"✗ Failed: {len(failed_apps)}")
    if failed_apps:
        for failure in failed_apps:
            print(f"  - {failure['name']}: {failure['error']}")
    print(f"{'='*60}")
    
    # Generate leaderboard and niche report if we have successful analyses
    if successful_apps and not args.smoke_test:
        print(f"\n{'='*60}")
        print("GENERATING MARKET LEADERBOARD")
        print(f"{'='*60}")
        try:
            leaderboard_file = reporter.aggregate_leaderboard(data_dir=data_dir)
            print(f"✓ Generated leaderboard: {leaderboard_file}")
        except Exception as e:
            print(f"✗ Failed to generate leaderboard: {e}")
            import traceback
            traceback.print_exc()
        
        # T-008: Generate Niche Battlefield Report and niche_matrix.json
        if len(analyses_for_niche) >= 2:
            try:
                niche_matrix = forensic_analyzer.generate_matrix(analyses_for_niche)
                matrix_file = reports_dir / "niche_matrix.json"
                with open(matrix_file, "w", encoding="utf-8") as f:
                    json.dump(niche_matrix, f, indent=2)
                print(f"✓ Saved niche matrix: {matrix_file}")
                niche_report = reporter.generate_niche_report(
                    niche_name=niche_name,
                    analyses=analyses_for_niche,
                    niche_matrix=niche_matrix,
                    forensic_by_app=forensic_by_app,
                )
                print(f"✓ Generated niche report: {niche_report}")
            except Exception as e:
                print(f"✗ Failed to generate niche report: {e}")
                import traceback
                traceback.print_exc()
    
    if failed_apps and not args.smoke_test:
        print(f"\n⚠ Some apps failed, but processing completed for {len(successful_apps)} apps")
        sys.exit(1)
    elif len(successful_apps) == len(apps_to_process):
        print(f"\n✓ All apps processed successfully!")
    else:
        print(f"\n✓ Processing complete")


if __name__ == "__main__":
    main()
