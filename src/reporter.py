"""Reporter class for generating markdown analysis reports."""
import json
import logging
from typing import Dict, Any, List, Optional
from pathlib import Path
from datetime import datetime

import pandas as pd

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class Reporter:
    """
    Generates human-readable markdown reports from analysis results.
    
    Responsibilities:
    - Format analysis data into storytelling markdown
    - Include executive summary, evidence, and raw data samples
    - Output to report_APPNAME.md files
    """
    
    def __init__(self, output_dir: Path = None):
        """
        Initialize the Reporter.
        
        Args:
            output_dir: Directory to save reports (default: reports/)
        """
        self.output_dir = output_dir or Path("reports")
        self.output_dir.mkdir(exist_ok=True)
    
    def generate_executive_summary(self, analysis: Dict[str, Any]) -> str:
        """
        Generate executive summary section.
        
        Args:
            analysis: Analysis results dictionary
            
        Returns:
            Markdown-formatted executive summary
        """
        # TODO: Generate f-string summary with risk score and condition
        pass
    
    def generate_evidence_section(self, analysis: Dict[str, Any]) -> str:
        """
        Generate evidence section with pain clusters and cliff events.
        
        Args:
            analysis: Analysis results dictionary
            
        Returns:
            Markdown-formatted evidence section
        """
        # TODO: Format pain categories and version impact data
        pass
    
    def generate_raw_data_sample(self, reviews: list, top_n: int = 5) -> str:
        """
        Generate raw data sample section with top reviews.
        
        Args:
            reviews: List of review dictionaries
            top_n: Number of reviews to include
            
        Returns:
            Markdown-formatted raw data section
        """
        # TODO: Extract and format top N "most helpful" 1-star reviews
        pass
    
    def generate_report(self, app_name: str, analysis: Dict[str, Any], reviews: list = None) -> Path:
        """
        Generate complete markdown report.
        
        Args:
            app_name: Name of the app
            analysis: Analysis results dictionary
            reviews: Optional list of reviews for raw data sample
            
        Returns:
            Path to generated report file
        """
        # TODO: Combine all sections and write to report_APPNAME.md
        pass
    
    def aggregate_leaderboard(self, data_dir: Path = None) -> Path:
        """
        Aggregate all analysis files into a ranked leaderboard.
        
        T-010: Aggregate Leaderboard - Holistically (Ranked Comparison)
        
        Process:
        1. Scan data/ folder for all *_analysis.json files
        2. Load and merge into Pandas DataFrame
        3. Sort by risk_score (descending)
        4. Generate markdown table with Rank, App Name, Risk Score, Volatility Slope, Primary Pain Category
        5. Save to data/market_leaderboard.md
        
        Args:
            data_dir: Directory containing analysis files (default: data/)
            
        Returns:
            Path to generated leaderboard file
        """
        if data_dir is None:
            data_dir = Path("data")
        
        logger.info(f"Scanning {data_dir} for analysis files...")
        
        # Step 1: Find all analysis files
        analysis_files = list(data_dir.glob("*_analysis.json"))
        
        if not analysis_files:
            logger.warning(f"No analysis files found in {data_dir}")
            return self._create_empty_leaderboard(data_dir)
        
        logger.info(f"Found {len(analysis_files)} analysis files")
        
        # Step 2: Load all analysis files into list of dicts
        analyses = []
        for analysis_file in analysis_files:
            try:
                with open(analysis_file, 'r', encoding='utf-8') as f:
                    analysis = json.load(f)
                    analyses.append(analysis)
            except Exception as e:
                logger.warning(f"Failed to load {analysis_file}: {e}")
                continue
        
        if not analyses:
            logger.error("No valid analysis files loaded")
            return self._create_empty_leaderboard(data_dir)
        
        logger.info(f"Loaded {len(analyses)} analyses")
        
        # Step 3: Convert to DataFrame (T-012: Enhanced with MECE pillars)
        df_data = []
        for analysis in analyses:
            app_name = analysis.get("app_name", "Unknown")
            metrics = analysis.get("metrics", {})
            signals = analysis.get("signals", {})
            
            # T-012: Extract primary pillar (MECE-based)
            primary_pillar = signals.get("primary_pillar", "None")
            suspected_version = signals.get("suspected_version")
            
            df_data.append({
                "app_name": app_name,
                "risk_score": metrics.get("risk_score", 0.0),
                "volatility_slope": metrics.get("volatility_slope", 0.0),
                "negative_ratio": metrics.get("negative_ratio", 0.0),
                "total_reviews_90d": metrics.get("total_reviews_90d", 0),
                "primary_pillar": primary_pillar,
                "suspected_version": suspected_version if suspected_version else "None",
                "broken_update_detected": signals.get("broken_update_detected", False)
            })
        
        df = pd.DataFrame(df_data)
        
        # Step 4: Sort by risk_score (descending) and add rank
        df = df.sort_values("risk_score", ascending=False).reset_index(drop=True)
        df.insert(0, "rank", range(1, len(df) + 1))
        
        # Step 5: Generate markdown table
        leaderboard_md = self._generate_leaderboard_markdown(df, len(analyses))
        
        # Step 6: Save to data/market_leaderboard.md
        output_file = data_dir / "market_leaderboard.md"
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(leaderboard_md)
        
        logger.info(f"Saved leaderboard to {output_file}")
        
        return output_file
    
    def _generate_leaderboard_markdown(self, df: pd.DataFrame, total_apps: int) -> str:
        """
        T-012: Generate markdown leaderboard table with MECE pillar columns.
        
        Args:
            df: DataFrame with ranked apps
            total_apps: Total number of apps analyzed
            
        Returns:
            Markdown-formatted leaderboard
        """
        md_lines = [
            "# Market Leaderboard: Screen Time & Focus Apps",
            "",
            f"**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
            f"**Total Apps Analyzed:** {total_apps}",
            "",
            "## Risk Score Ranking (MECE Methodology)",
            "",
            "Apps are ranked by Risk Score (descending). Higher scores indicate more volatility and potential issues.",
            "",
            "| Rank | App Name | Risk Score | Vol. Slope | Neg. Ratio (%) | Volume | Primary Pillar | Suspected Version |",
            "|------|----------|------------|------------|----------------|--------|----------------|-------------------|"
        ]
        
        # Add table rows
        for _, row in df.iterrows():
            rank = int(row["rank"])
            app_name = row["app_name"].replace("_", " ")
            risk_score = f"{row['risk_score']:.2f}"
            volatility_slope = f"{row['volatility_slope']:.4f}"
            negative_ratio_pct = f"{row['negative_ratio'] * 100:.1f}%"
            volume = int(row["total_reviews_90d"])
            primary_pillar = row.get("primary_pillar", "None")
            suspected_version = row.get("suspected_version", "None")
            
            md_lines.append(
                f"| {rank} | {app_name} | {risk_score} | {volatility_slope} | {negative_ratio_pct} | {volume} | {primary_pillar} | {suspected_version} |"
            )
        
        md_lines.extend([
            "",
            "## Interpretation",
            "",
            "### MECE Risk Scoring Methodology",
            "",
            "**MECE Pillars:** Mutually Exclusive, Collectively Exhaustive risk categories",
            "",
            "1. **Functional Risk:** Technical issues affecting app performance",
            "   - Categories: `critical`, `performance`, `privacy`",
            "   - Examples: Crashes, freezes, bugs, slow loading, data leaks",
            "",
            "2. **Economic Risk:** Financial concerns and monetization issues",
            "   - Categories: `scam_financial`, `subscription`, `ads`",
            "   - Examples: Unexpected charges, billing problems, deceptive pricing",
            "",
            "3. **Experience Risk:** Usability and competitive positioning",
            "   - Categories: `usability`, `competitor_mention`, `generic_pain`",
            "   - Examples: Confusing UI, difficult navigation, preference for alternatives",
            "",
            "### Risk Score Calculation",
            "",
            "**Formula:** `BaseScore × (1 + max(0, VolatilitySlope))`",
            "",
            "- **Base Score:** `(FunctionalDensity + EconomicDensity + ExperienceDensity) × 10.0`",
            "  - Density = Sum of keyword weights / Total reviews analyzed",
            "  - Scaler (10.0) standardizes so ~1 major pain point per user = 100",
            "",
            "- **Volatility Boost:** Amplifies score if trend is worsening (positive slope)",
            "  - If slope > 0: Score increases proportionally",
            "  - If slope ≤ 0: Base score remains unchanged",
            "",
            "### Column Definitions",
            "",
            "- **Risk Score (0-100):** MECE-based composite metric (Pillar + Boost)",
            "- **Vol. Slope (Trend):** Rate of change in pain-keyword reviews per week",
            "  - Positive = increasing problems (worsening)",
            "  - Negative = decreasing problems (improving)",
            "  - Zero = stable (no trend)",
            "- **Neg. Ratio (%):** Percentage of reviews containing pain keywords",
            "- **Volume:** Total number of reviews analyzed (last 90 days)",
            "- **Primary Pillar:** MECE pillar with highest density (Functional/Economic/Experience)",
            "- **Suspected Version:** App version with spike in pain-keyword reviews (if detected)",
            "",
            "### Risk Score Ranges",
            "- **0-25:** Low Risk (Stable)",
            "- **26-50:** Moderate Risk (Watch)",
            "- **51-75:** High Risk (Concerning)",
            "- **76-100:** Critical Risk (Urgent Action Needed)",
            ""
        ])
        
        return "\n".join(md_lines)
    
    def _create_empty_leaderboard(self, data_dir: Path) -> Path:
        """Create empty leaderboard when no analysis files found."""
        output_file = data_dir / "market_leaderboard.md"
        content = f"""# Market Leaderboard: Screen Time & Focus Apps

**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
**Status:** No analysis files found

Please run the analyzer first to generate analysis files.
"""
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(content)
        
        logger.warning(f"Created empty leaderboard at {output_file}")
        return output_file
