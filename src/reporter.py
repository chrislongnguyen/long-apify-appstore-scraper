"""Reporter class for generating markdown analysis reports."""
import json
import logging
from typing import Dict, Any, List, Optional
from pathlib import Path
from datetime import datetime

import pandas as pd
from jinja2 import Environment, FileSystemLoader

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def _extract_review_text(review: dict) -> str:
    """Extract text from review dict."""
    for field in ["text", "reviewText", "content", "body", "comment"]:
        if field in review and review[field]:
            return str(review[field])
    title = review.get("title", "")
    return str(title) if title else ""


def _extract_rating(review: dict) -> Optional[int]:
    """Extract rating from review dict."""
    for field in ["rating", "starRating", "stars", "score"]:
        if field in review and review[field] is not None:
            try:
                r = int(review[field])
                if 1 <= r <= 5:
                    return r
            except (ValueError, TypeError):
                pass
    return None


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
        metrics = analysis.get("metrics", {})
        signals = analysis.get("signals", {})
        risk_score = metrics.get("risk_score", 0.0)
        primary_pillar = signals.get("primary_pillar", "None")
        suspected_version = signals.get("suspected_version")
        
        if risk_score >= 76:
            condition = "CRITICAL"
        elif risk_score >= 51:
            condition = "HIGH RISK"
        elif risk_score >= 26:
            condition = "MODERATE"
        else:
            condition = "STABLE"
        
        verdict = f"App is in **{condition}** condition with a Risk Score of **{risk_score:.1f}/100**."
        if primary_pillar != "None":
            verdict += f" Primary pain pillar: **{primary_pillar}**."
        if suspected_version:
            verdict += f" Suspected problematic version: **{suspected_version}**."
        return verdict
    
    def generate_financial_impact_section(self, analysis: Dict[str, Any]) -> str:
        """
        T-024: Generate Financial Impact section (Fermi + Trend Acceleration).
        
        Args:
            analysis: Analysis results dictionary
            
        Returns:
            Markdown-formatted financial impact section
        """
        signals = analysis.get("signals", {})
        lines = []
        
        monthly_leakage = signals.get("monthly_leakage_usd", 0)
        lines.append(f"- **Estimated Monthly Revenue Leakage:** ${monthly_leakage:,.2f}")
        
        slope_delta = signals.get("slope_delta")
        slope_delta_insight = signals.get("slope_delta_insight")
        if slope_delta is not None and slope_delta_insight:
            # Extract percentage for display if available
            lines.append(f"- **Trend Acceleration:** {slope_delta_insight}")
        else:
            lines.append("- **Trend Acceleration:** Insufficient data (need 8+ weeks)")
        
        return "\n".join(lines) if lines else "No financial impact data available."
    
    def generate_evidence_section(self, analysis: Dict[str, Any]) -> str:
        """
        Generate evidence section with pain clusters and cliff events.
        
        Args:
            analysis: Analysis results dictionary
            
        Returns:
            Markdown-formatted evidence section
        """
        signals = analysis.get("signals", {})
        lines = []
        
        top_pain = signals.get("top_pain_categories", [])
        if top_pain:
            lines.append("### Primary Pain Clusters")
            for item in top_pain[:5]:
                cat = item.get("category", "?")
                count = item.get("count", 0)
                weight = item.get("weight", 0)
                lines.append(f"- **{cat}**: {count} mentions (weight {weight})")
        
        if signals.get("broken_update_detected") and signals.get("suspected_version"):
            lines.append("")
            lines.append(f"### Version Impact: Sentiment drop detected after **{signals['suspected_version']}**")
        
        return "\n".join(lines) if lines else "No pain clusters identified."
    
    def generate_raw_data_sample(self, reviews: list, top_n: int = 5) -> str:
        """
        Generate raw data sample section with top reviews.
        
        Args:
            reviews: List of review dicts or evidence strings (from analysis)
            top_n: Number of reviews to include
            
        Returns:
            Markdown-formatted raw data section
        """
        scored = []
        for r in reviews:
            if isinstance(r, str):
                text = r.strip()
                if len(text) > 20:
                    scored.append((1, len(text), text[:500], None))
            else:
                rating = _extract_rating(r)
                text = _extract_review_text(r)
                if rating is not None and rating <= 2 and len(text.strip()) > 20:
                    scored.append((rating, len(text), text[:500], r))
        scored.sort(key=lambda x: (x[0], -x[1]))  # Lower rating first, longer text first
        
        lines = []
        for i, (_, _, text, _) in enumerate(scored[:top_n], 1):
            lines.append(f"{i}. > {text[:400]}{'...' if len(text) > 400 else ''}")
        return "\n\n".join(lines) if lines else "No qualifying negative reviews available."
    
    def _get_momentum_label(self, volatility_slope: float, slope_delta: Optional[float]) -> str:
        """
        T-021 Refined: Momentum label from volatility_slope and slope_delta.
        
        - volatility_slope > 0.1: slope_delta < 0 -> "Decelerating Pain", > 0 -> "Accelerating Pain"
        - -0.05 <= volatility_slope <= 0.05: "Stabilizing"
        - volatility_slope < -0.05: "Improving"
        - 0.05 < volatility_slope <= 0.1: "Worsening" (moderate) or use slope_delta if available
        """
        if volatility_slope > 0.1:
            if slope_delta is not None:
                return "🚀 Accelerating Pain" if slope_delta > 0 else "📉 Decelerating Pain"
            return "🚀 Worsening"
        if -0.05 <= volatility_slope <= 0.05:
            return "📉 Stabilizing"
        if volatility_slope < -0.05:
            return "📈 Improving"
        # 0.05 < volatility_slope <= 0.1: moderate worsening
        if slope_delta is not None:
            return "🚀 Accelerating Pain" if slope_delta > 0 else "📉 Decelerating Pain"
        return "🚀 Worsening"

    def _get_timeline_exhibit_title(self, timeline: List[Dict[str, Any]]) -> str:
        """
        T-024: Use Named Spike from forensic timeline for exhibit title.
        
        If any anomaly has a version label, e.g. "The Version 4.2 Spike",
        return "The Version X.X Crisis". Otherwise "Timeline of Pain".
        """
        for t in timeline:
            event = t.get("event", "")
            version = t.get("version")
            if event and "Version" in event and version:
                return f"The Version {version} Crisis"
        return "Timeline of Pain"
    
    def _build_ascii_timeline(self, timeline: List[Dict[str, Any]], width: int = 50) -> str:
        """Build ASCII chart of weekly pain density (T-008 Exhibit A)."""
        if not timeline:
            return "_No timeline data available._"
        
        max_density = max(t.get("density", 0) for t in timeline) or 0.01
        lines = []
        for t in timeline:
            week = t.get("week", "?")
            density = t.get("density", 0)
            event = t.get("event", "")
            bar_len = int((density / max_density) * width) if max_density else 0
            bar = "█" * bar_len
            marker = " 🔴" if event else ""
            lines.append(f"  {week}: {bar} {density:.0%}{marker}")
        return "```\n" + "\n".join(lines) + "\n```"
    
    def generate_report(
        self,
        app_name: str,
        analysis: Dict[str, Any],
        reviews: list = None,
        forensic: Dict[str, Any] = None,
    ) -> Path:
        """
        T-008: Generate complete forensic intelligence report.
        
        Args:
            app_name: Name of the app
            analysis: Analysis results dictionary (schema_app_gap)
            reviews: Optional list of reviews for evidence quotes
            forensic: Optional forensic data (timeline, clusters, migration)
            
        Returns:
            Path to generated report file
        """
        date_str = datetime.now().strftime("%Y-%m-%d")
        safe_name = app_name.replace(" ", "_")
        output_path = self.output_dir / f"report_{safe_name}_{date_str}.md"
        
        sections = []
        
        # Executive Summary
        sections.append("# Intelligence Report: " + app_name.replace("_", " "))
        sections.append("")
        sections.append(f"**Generated:** {date_str}")
        sections.append("")
        sections.append("## Executive Summary")
        sections.append("")
        sections.append(self.generate_executive_summary(analysis))
        sections.append("")
        
        # T-024: Financial Impact section
        sections.append("### Financial Impact")
        sections.append("")
        sections.append(self.generate_financial_impact_section(analysis))
        sections.append("")
        
        # Exhibit A: Timeline of Pain (T-024: Named Spike title)
        if forensic and forensic.get("timeline"):
            exhibit_title = self._get_timeline_exhibit_title(forensic["timeline"])
            sections.append(f"## Exhibit A: {exhibit_title}")
            sections.append("")
            sections.append("Weekly pain density (reviews with pain keywords / total reviews):")
            sections.append("")
            sections.append(self._build_ascii_timeline(forensic["timeline"]))
            sections.append("")
        
        # Exhibit B: Semantic Clusters (N-Grams)
        if forensic and forensic.get("clusters"):
            sections.append("## Exhibit B: Hidden Pain Phrases (N-Grams)")
            sections.append("")
            sections.append("Top pain phrases discovered in 1-2 star reviews (not in keyword dictionary):")
            sections.append("")
            for item in forensic["clusters"][:5]:
                phrase = item.get("phrase", "?")
                count = item.get("count", 0)
                sections.append(f"- **{phrase}** ({count} occurrences)")
            sections.append("")
        
        # Exhibit C: Witnesses (Evidence)
        sections.append("## Exhibit C: Verified Quotes")
        sections.append("")
        sections.append(self.generate_raw_data_sample(reviews or analysis.get("evidence", []), top_n=5))
        sections.append("")
        
        # Evidence Section
        sections.append("## The Evidence")
        sections.append("")
        sections.append(self.generate_evidence_section(analysis))
        
        content = "\n".join(sections)
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(content)
        
        logger.info(f"Saved report to {output_path}")
        return output_path
    
    def generate_niche_report(
        self,
        niche_name: str,
        analyses: List[Dict[str, Any]],
        niche_matrix: Dict[str, Dict[str, float]],
        forensic_by_app: Dict[str, Dict[str, Any]] = None,
    ) -> Path:
        """
        T-008: Generate Niche Battlefield Report with Feature/Fail Matrix.
        
        Args:
            niche_name: Name of the niche (e.g., "Voice_AI")
            analyses: List of analysis dicts
            niche_matrix: {app_name: {pillar: score}} from ForensicAnalyzer
            forensic_by_app: Optional {app_name: forensic_data} for migration flow
            
        Returns:
            Path to generated report file
        """
        date_str = datetime.now().strftime("%Y-%m-%d")
        output_path = self.output_dir / f"report_NICHE_{niche_name}_{date_str}.md"
        
        sections = [
            f"# Niche Battlefield Report: {niche_name.replace('_', ' ')}",
            "",
            f"**Generated:** {date_str}",
            "",
            "## The Matrix (Feature/Fail Heatmap)",
            "",
            "| App | Functional | Economic | Experience |",
            "|-----|------------|----------|------------|",
        ]
        
        for app_name, pillars in niche_matrix.items():
            func = pillars.get("Functional", 0)
            econ = pillars.get("Economic", 0)
            exp = pillars.get("Experience", 0)
            f_str = f"{func:.1f} 🔴" if func > 50 else f"{func:.1f} 🟢"
            e_str = f"{econ:.1f} 🔴" if econ > 50 else f"{econ:.1f} 🟢"
            x_str = f"{exp:.1f} 🔴" if exp > 50 else f"{exp:.1f} 🟢"
            sections.append(f"| {app_name.replace('_', ' ')} | {f_str} | {e_str} | {x_str} |")
        
        sections.append("")
        sections.append("### Legend")
        sections.append("- 🔴 Score > 50 (High Risk)")
        sections.append("- 🟢 Score ≤ 50 (Low/Moderate Risk)")
        sections.append("")
        
        # T-017: White Space Analysis - "Safe Harbor" = pillars low AND risk_score < 50
        # Build app_name -> risk_score from analyses (critical: high risk_score disqualifies)
        app_risk = {}
        for a in analyses:
            app_risk[a.get("app_name", "Unknown")] = a.get("metrics", {}).get("risk_score", 0)
        
        safe_harbors = []
        for app_name, pillars in niche_matrix.items():
            func = pillars.get("Functional", 0)
            econ = pillars.get("Economic", 0)
            risk_score = app_risk.get(app_name, 0)
            if func < 30 and econ < 30 and risk_score < 50:
                safe_harbors.append(app_name.replace("_", " "))
        sections.append("## 🏳️ White Space Analysis")
        sections.append("")
        if safe_harbors:
            sections.append("**Gap Found:** " + ", ".join(safe_harbors) + " — safe harbor(s) in this niche.")
        else:
            sections.append("**No Gap:** All apps show elevated risk (High Opportunity for differentiation).")
        sections.append("")
        
        # Migration Flow (if available)
        if forensic_by_app:
            sections.append("## User Migration Flow")
            sections.append("")
            for app_name, forensic in forensic_by_app.items():
                migration = forensic.get("migration", [])
                churns = [m for m in migration if m.get("type") == "churn"]
                if churns:
                    parts = [f"{app_name} → {m['competitor']} ({m['count']} mentions)" for m in churns]
                    sections.append(f"- **{app_name}**: " + "; ".join(parts))
            sections.append("")
        
        content = "\n".join(sections)
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(content)
        
        logger.info(f"Saved niche report to {output_path}")
        return output_path

    def render_venture_blueprint(
        self,
        app_name: str,
        icp: Dict[str, Any],
        system_map: Dict[str, Any],
        eps: Dict[str, Any],
        output_dir: Path = None,
        niche_name: str = "",
    ) -> Path:
        """
        T-027: Render Venture Blueprint markdown from Jinja2 template.

        Args:
            app_name: Target app name
            icp: Stage 1 output (Holographic ICP)
            system_map: Stage 2 output (System Dynamics Map)
            eps: Stage 3 output (EPS Prescription)
            output_dir: Optional output dir override
            niche_name: Optional niche name for header context

        Returns:
            Path to generated venture blueprint markdown
        """
        out_dir = output_dir or self.output_dir
        out_dir.mkdir(parents=True, exist_ok=True)

        project_root = Path(__file__).resolve().parent.parent
        templates_dir = project_root / "templates"
        env = Environment(
            loader=FileSystemLoader(str(templates_dir)),
            autoescape=False,
            trim_blocks=True,
            lstrip_blocks=True,
        )
        template = env.get_template("venture_blueprint.j2")

        rendered = template.render(
            app_name=app_name,
            generated_at=datetime.now().strftime("%Y-%m-%d"),
            niche_name=niche_name,
            icp=icp or {},
            system_map=system_map or {},
            eps=eps or {},
        )

        safe_name = app_name.replace(" ", "_").lower()
        output_path = out_dir / f"venture_blueprint_{safe_name}.md"
        output_path.write_text(rendered, encoding="utf-8")
        logger.info(f"Saved venture blueprint to {output_path}")
        return output_path
    
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
            # T-024: Predictive metrics
            monthly_leakage_usd = signals.get("monthly_leakage_usd", 0.0)
            slope_delta = signals.get("slope_delta")
            slope_delta_insight = signals.get("slope_delta_insight")
            
            df_data.append({
                "app_name": app_name,
                "risk_score": metrics.get("risk_score", 0.0),
                "volatility_slope": metrics.get("volatility_slope", 0.0),
                "negative_ratio": metrics.get("negative_ratio", 0.0),
                "total_reviews_90d": metrics.get("total_reviews_90d", 0),
                "primary_pillar": primary_pillar,
                "suspected_version": suspected_version if suspected_version else "None",
                "broken_update_detected": signals.get("broken_update_detected", False),
                "monthly_leakage_usd": monthly_leakage_usd,
                "slope_delta": slope_delta,
                "slope_delta_insight": slope_delta_insight,
            })
        
        df = pd.DataFrame(df_data)
        
        # Step 4: T-024 Sort by monthly_leakage_usd (descending) as primary rank
        df = df.sort_values("monthly_leakage_usd", ascending=False).reset_index(drop=True)
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
            "## Revenue Leakage Ranking (T-024 Predictive)",
            "",
            "Apps are ranked by Estimated Monthly Revenue Leakage (descending). Higher leakage indicates more urgent opportunity.",
            "",
            "| Rank | App Name | Revenue Leakage ($/mo) | Momentum | Risk Score | Vol. Slope | Neg. Ratio (%) | Volume | Primary Pillar | Suspected Version |",
            "|------|----------|------------------------|----------|------------|------------|----------------|--------|----------------|-------------------|"
        ]
        
        # Add table rows
        for _, row in df.iterrows():
            rank = int(row["rank"])
            app_name = row["app_name"].replace("_", " ")
            monthly_leakage = row.get("monthly_leakage_usd", 0)
            leakage_str = f"${monthly_leakage:,.0f}" if monthly_leakage else "—"
            # T-021 Refined: Momentum labels (volatility_slope + slope_delta)
            momentum = self._get_momentum_label(
                row.get("volatility_slope", 0),
                row.get("slope_delta"),
            )
            risk_score = f"{row['risk_score']:.2f}"
            volatility_slope = f"{row['volatility_slope']:.4f}"
            negative_ratio_pct = f"{row['negative_ratio'] * 100:.1f}%"
            volume = int(row["total_reviews_90d"])
            primary_pillar = row.get("primary_pillar", "None")
            suspected_version = row.get("suspected_version", "None")
            
            md_lines.append(
                f"| {rank} | {app_name} | {leakage_str} | {momentum} | {risk_score} | {volatility_slope} | {negative_ratio_pct} | {volume} | {primary_pillar} | {suspected_version} |"
            )
        
        md_lines.extend([
            "",
            "## Interpretation",
            "",
            "### MECE Risk Scoring Methodology (T-031 Severity-First)",
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
            "### Risk Score — Layman's Terms",
            "",
            "We weigh **Scam and subscription** (Economic) signals **2.5× harder** than UI glitches.",
            "Economic pain (deceptive pricing, hidden fees) is treated as higher severity than usability complaints.",
            "",
            "**Critical Floor:** If >10% of signals suggest Scam/Economic risk, the score locks to **High Risk (60+)** regardless of trend.",
            "An \"improving\" trend (negative slope) will dampen the score, but it **cannot erase** serious red flags.",
            "",
            "### Column Definitions",
            "",
            "- **Revenue Leakage ($/mo):** Fermi estimate of monthly revenue opportunity from churn signals",
            "- **Momentum:** 🚀 Accelerating Pain = worsening & speeding up; 📉 Decelerating Pain = worsening but slowing; 📉 Stabilizing = flat trend; 📈 Improving = pain decreasing",
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
