"""Analyzer class for deterministic statistical analysis of reviews."""
import json
import logging
import re
from datetime import datetime, timezone, timedelta
from typing import Dict, Any, List, Optional
from pathlib import Path

import pandas as pd
import numpy as np

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class Analyzer:
    """
    Performs deterministic analysis on review data using Pandas/NumPy.
    
    Responsibilities:
    - Filter reviews by date (last 90 days)
    - Calculate volatility slope
    - Compute keyword density
    - Generate risk score
    """
    
    def __init__(self, pain_keywords_path: Path = None, settings: Dict[str, Any] = None):
        """
        Initialize the Analyzer.
        
        Args:
            pain_keywords_path: Path to pain_keywords.json config
            settings: Settings configuration dictionary (from settings.json)
        """
        self.pain_keywords = None
        self.settings = settings or {}
        self.weights = self.settings.get("weights", {})
        # TODO: Load pain_keywords.json
        if pain_keywords_path:
            self.load_pain_keywords(pain_keywords_path)
    
    def load_pain_keywords(self, config_path: Path) -> None:
        """
        Load pain keywords configuration from JSON file.
        
        Args:
            config_path: Path to pain_keywords.json file
            
        Raises:
            FileNotFoundError: If config file doesn't exist
            json.JSONDecodeError: If file contains invalid JSON
        """
        if not config_path.exists():
            raise FileNotFoundError(f"Pain keywords config not found: {config_path}")
        
        with open(config_path, 'r', encoding='utf-8') as f:
            self.pain_keywords = json.load(f)
        
        logger.info(f"Loaded {len(self.pain_keywords.get('categories', {}))} pain keyword categories")
    
    def filter_by_date(self, df: pd.DataFrame, days_back: int = 90) -> pd.DataFrame:
        """
        Filter DataFrame to last N days using vectorized pandas operations.
        
        Args:
            df: Reviews DataFrame with 'date' column
            days_back: Number of days to look back
            
        Returns:
            Filtered DataFrame
        """
        if df.empty or 'date' not in df.columns:
            logger.warning("DataFrame is empty or missing 'date' column")
            return df
        
        # Calculate cutoff date (timezone-aware)
        cutoff_date = datetime.now(timezone.utc) - timedelta(days=days_back)
        
        # Ensure date column is datetime type
        if not pd.api.types.is_datetime64_any_dtype(df['date']):
            df['date'] = pd.to_datetime(df['date'], errors='coerce', utc=True)
        
        # Vectorized filtering
        filtered_df = df[df['date'] >= cutoff_date].copy()
        
        logger.info(f"Filtered to {len(filtered_df)} reviews within last {days_back} days (from {len(df)} total)")
        
        return filtered_df
    
    def calculate_slope(self, df: pd.DataFrame) -> float:
        """
        Calculate the slope of pain-keyword review trend over time using linear regression.
        
        T-011 Fix: Uses pain-keyword-driven signals instead of traditional 1-2 star reviews.
        
        Logic:
        1. Identify reviews containing pain keywords (any category)
        2. Resample by week
        3. Calculate slope using np.polyfit
        
        Args:
            df: Filtered reviews DataFrame with 'date' and 'text' columns
            
        Returns:
            Slope value (m from linear regression). Returns 0.0 if insufficient data.
            
        Note:
            If insufficient data points (< 2 weeks), returns 0.0 and logs warning
        """
        if df.empty or 'date' not in df.columns:
            logger.warning("DataFrame missing required columns for slope calculation")
            return 0.0
        
        # T-011 Fix: Use pain-keyword reviews instead of low-star reviews
        # Identify reviews with pain keywords
        has_pain_keyword = self._identify_pain_keyword_reviews(df)
        pain_keyword_reviews = df[has_pain_keyword].copy()
        
        if len(pain_keyword_reviews) < 2:
            logger.warning(f"Insufficient pain-keyword reviews ({len(pain_keyword_reviews)}) for slope calculation")
            return 0.0
        
        # Ensure date is datetime and set as index
        if not pd.api.types.is_datetime64_any_dtype(pain_keyword_reviews['date']):
            pain_keyword_reviews['date'] = pd.to_datetime(pain_keyword_reviews['date'], errors='coerce', utc=True)
        
        # Drop rows with invalid dates
        pain_keyword_reviews = pain_keyword_reviews.dropna(subset=['date'])
        
        if len(pain_keyword_reviews) < 2:
            logger.warning(f"Insufficient pain-keyword reviews with valid dates ({len(pain_keyword_reviews)}) for slope calculation")
            return 0.0
        
        pain_keyword_reviews = pain_keyword_reviews.set_index('date')
        
        # Resample by week and count pain-keyword reviews per week
        weekly_counts = pain_keyword_reviews.resample('W').size()
        
        if len(weekly_counts) < 2:
            logger.warning(f"Insufficient weeks ({len(weekly_counts)}) for slope calculation")
            return 0.0
        
        # Calculate slope using linear regression (np.polyfit)
        # x = week indices (0, 1, 2, ...), y = pain-keyword review counts per week
        week_indices = np.arange(len(weekly_counts))
        counts = weekly_counts.values
        
        try:
            # Fit linear regression: y = mx + b, get slope (m)
            slope, _ = np.polyfit(week_indices, counts, deg=1)
            logger.info(f"Calculated slope: {slope:.4f} (pain-keyword reviews per week)")
            return float(slope)
        except (np.linalg.LinAlgError, ValueError) as e:
            logger.warning(f"Slope calculation failed: {e}. Returning 0.0")
            return 0.0
    
    def _identify_pain_keyword_reviews(self, df: pd.DataFrame) -> pd.Series:
        """
        Identify reviews that contain any pain keywords (T-011: Redefine "negative").
        
        Args:
            df: Reviews DataFrame with 'text' column (or 'title' + 'text')
            
        Returns:
            Boolean Series indicating which reviews contain pain keywords
        """
        if df.empty or 'text' not in df.columns:
            return pd.Series([False] * len(df), index=df.index)
        
        if not self.pain_keywords or 'categories' not in self.pain_keywords:
            return pd.Series([False] * len(df), index=df.index)
        
        # Combine title and text if both exist, otherwise use text
        if 'title' in df.columns:
            combined_text = (df['title'].fillna('') + ' ' + df['text'].fillna('')).str.lower()
        else:
            combined_text = df['text'].fillna('').str.lower()
        
        # Create a combined pattern for ALL pain keywords across all categories
        all_keywords = []
        for category_data in self.pain_keywords['categories'].values():
            keywords = category_data.get('keywords', [])
            all_keywords.extend([kw.lower() for kw in keywords])
        
        if not all_keywords:
            return pd.Series([False] * len(df), index=df.index)
        
        # Create regex pattern for all keywords (case-insensitive)
        escaped_keywords = [re.escape(kw) for kw in all_keywords]
        pattern = '|'.join(escaped_keywords)
        
        # Vectorized matching: check if review contains any pain keyword
        has_pain_keyword = combined_text.str.contains(pattern, case=False, na=False, regex=True)
        
        return has_pain_keyword
    
    def calculate_keyword_density(self, df: pd.DataFrame) -> Dict[str, int]:
        """
        Calculate keyword density per category using vectorized pandas operations.
        
        Args:
            df: Reviews DataFrame with 'text' column (or 'title' + 'text')
            
        Returns:
            Dictionary mapping category names to counts
        """
        if df.empty or 'text' not in df.columns:
            logger.warning("DataFrame missing 'text' column for keyword density")
            return {}
        
        if not self.pain_keywords or 'categories' not in self.pain_keywords:
            logger.warning("Pain keywords not loaded")
            return {}
        
        # Combine title and text if both exist, otherwise use text
        if 'title' in df.columns:
            combined_text = (df['title'].fillna('') + ' ' + df['text'].fillna('')).str.lower()
        else:
            combined_text = df['text'].fillna('').str.lower()
        
        category_counts = {}
        
        # Vectorized keyword matching for each category
        for category_name, category_data in self.pain_keywords['categories'].items():
            keywords = category_data.get('keywords', [])
            if not keywords:
                continue
            
            # Create regex pattern for all keywords in category (case-insensitive)
            # Escape special regex characters and join with |
            escaped_keywords = [re.escape(kw.lower()) for kw in keywords]
            pattern = '|'.join(escaped_keywords)
            
            # Vectorized matching: count occurrences of any keyword in each review
            matches = combined_text.str.count(pattern, flags=re.IGNORECASE)
            
            # Count reviews that contain at least one keyword from this category
            category_count = int((matches > 0).sum())
            category_counts[category_name] = category_count
            
            if category_count > 0:
                logger.debug(f"Category '{category_name}': {category_count} reviews matched")
        
        logger.info(f"Keyword density calculated: {sum(category_counts.values())} total matches across {len(category_counts)} categories")
        
        return category_counts
    
    def _get_mece_pillar_mapping(self) -> Dict[str, str]:
        """
        T-012: Map categories to MECE Pillars.
        
        Returns:
            Dictionary mapping category names to pillar names
        """
        return {
            # Functional Risk: critical, performance, privacy
            "critical": "Functional",
            "performance": "Functional",
            "privacy": "Functional",
            # Economic Risk: scam_financial, subscription, ads
            "scam_financial": "Economic",
            "subscription": "Economic",
            "ads": "Economic",
            # Experience Risk: usability, competitor_mention, generic_pain
            "usability": "Experience",
            "competitor_mention": "Experience",
            "generic_pain": "Experience"
        }
    
    def _calculate_pillar_densities(
        self,
        category_counts: Dict[str, int],
        total_reviews: int
    ) -> Dict[str, float]:
        """
        T-012: Calculate Pillar Density for each MECE pillar.
        
        Formula: Density = (Sum of Weights of Matching Keywords) / Total Reviews Analyzed
        
        Args:
            category_counts: Dictionary of category counts
            total_reviews: Total number of reviews analyzed
            
        Returns:
            Dictionary mapping pillar names to density values
        """
        if total_reviews == 0 or not self.pain_keywords:
            return {"Functional": 0.0, "Economic": 0.0, "Experience": 0.0}
        
        pillar_mapping = self._get_mece_pillar_mapping()
        pillar_weights = {"Functional": 0.0, "Economic": 0.0, "Experience": 0.0}
        
        # Sum weights for each pillar based on category matches
        for category_name, count in category_counts.items():
            if category_name in pillar_mapping:
                pillar = pillar_mapping[category_name]
                if category_name in self.pain_keywords.get("categories", {}):
                    category_weight = self.pain_keywords["categories"][category_name].get("weight", 0)
                    # Sum weights: each matching review contributes its category weight
                    pillar_weights[pillar] += count * category_weight
        
        # Calculate density: sum of weights / total reviews
        pillar_densities = {
            pillar: weights / total_reviews
            for pillar, weights in pillar_weights.items()
        }
        
        logger.debug(f"Pillar densities: Functional={pillar_densities['Functional']:.4f}, "
                    f"Economic={pillar_densities['Economic']:.4f}, "
                    f"Experience={pillar_densities['Experience']:.4f}")
        
        return pillar_densities
    
    def calculate_risk_score(
        self,
        slope: float,
        volatility_score: float,
        category_counts: Dict[str, int],
        total_reviews: int = 1
    ) -> tuple[float, Dict[str, float], str]:
        """
        T-012: Calculate MECE Risk Score using Pillar + Boost formula.
        
        Formula:
        - BaseScore = (FunctionalDensity + EconomicDensity + ExperienceDensity) × 10.0
        - FinalRisk = min(100.0, BaseScore × (1 + max(0, VolatilitySlope)))
        
        Args:
            slope: Trend slope value (volatility slope)
            volatility_score: Volume-based volatility score (unused in MECE formula)
            category_counts: Dictionary of category counts
            total_reviews: Total number of reviews analyzed
            
        Returns:
            Tuple of (risk_score, pillar_densities, primary_pillar)
            - risk_score: Final risk score (0-100)
            - pillar_densities: Dictionary mapping pillar names to densities
            - primary_pillar: Name of pillar with highest density
        """
        # T-012: Calculate pillar densities
        pillar_densities = self._calculate_pillar_densities(category_counts, total_reviews)
        
        # Step C: Calculate Base Risk Score
        # BaseScore = (FunctionalDensity + EconomicDensity + ExperienceDensity) × 10.0
        total_density = sum(pillar_densities.values())
        base_score = total_density * 10.0
        
        # Step D: Apply Volatility Boost
        # FinalRisk = min(100.0, BaseScore × (1 + max(0, VolatilitySlope)))
        # Logic: If slope is positive (getting worse), amplify the score. If negative/flat, keep Base Score.
        volatility_boost = 1.0 + max(0.0, slope)  # Only boost if slope is positive
        final_risk = min(100.0, base_score * volatility_boost)
        
        # Identify primary pillar (highest density)
        primary_pillar = max(pillar_densities.items(), key=lambda x: x[1])[0] if pillar_densities else "None"
        
        logger.info(
            f"MECE Risk Score: Base={base_score:.2f}, Boost={volatility_boost:.3f}, "
            f"Final={final_risk:.2f}, Primary Pillar={primary_pillar}"
        )
        
        return round(final_risk, 2), pillar_densities, primary_pillar
    
    def analyze(self, reviews: List[Dict[str, Any]], app_name: str = "Unknown", days_back: int = 90) -> Dict[str, Any]:
        """
        Main analysis method - orchestrates all calculations and generates schema_app_gap.json.
        
        Pipeline:
        1. Convert reviews to DataFrame
        2. Filter by date (last N days)
        3. Calculate descriptive metrics (total reviews, negative ratio)
        4. Calculate slope (predictive analytics)
        5. Calculate keyword density (prescriptive analytics)
        6. Calculate risk score
        7. Generate schema_app_gap.json structure
        
        Args:
            reviews: List of review dictionaries from Fetcher
            app_name: Name of the app being analyzed
            days_back: Number of days to analyze (default: 90)
            
        Returns:
            Analysis results dictionary (schema_app_gap.json format)
        """
        if not reviews:
            logger.warning(f"No reviews provided for analysis of {app_name}")
            return self._empty_analysis_result(app_name)
        
        logger.info(f"Starting analysis for {app_name} ({len(reviews)} reviews)")
        
        # Step 1: Convert to DataFrame
        df = pd.DataFrame(reviews)
        
        # Step 2: Parse and normalize date column
        date_columns = ['date', 'reviewDate', 'createdAt', 'updatedAt']
        date_col = None
        for col in date_columns:
            if col in df.columns:
                date_col = col
                break
        
        if not date_col:
            logger.warning("No date column found, using current date for all reviews")
            df['date'] = datetime.now(timezone.utc)
        else:
            df['date'] = pd.to_datetime(df[date_col], errors='coerce', utc=True)
            # Drop rows with invalid dates
            df = df.dropna(subset=['date'])
        
        # Step 3: Normalize score/rating column
        score_columns = ['score', 'rating', 'starRating', 'stars']
        score_col = None
        for col in score_columns:
            if col in df.columns:
                score_col = col
                break
        
        if not score_col:
            logger.warning("No score column found, defaulting to 3 (neutral)")
            df['score'] = 3
        else:
            df['score'] = pd.to_numeric(df[score_col], errors='coerce').fillna(3)
            df['score'] = df['score'].astype(int).clip(1, 5)
        
        # Step 4: Filter by date
        df_filtered = self.filter_by_date(df, days_back)
        
        if df_filtered.empty:
            logger.warning(f"No reviews within last {days_back} days")
            return self._empty_analysis_result(app_name)
        
        # Step 5: Calculate descriptive metrics
        total_reviews = len(df_filtered)
        
        # T-011 Fix: Redefine "negative" as reviews with pain keywords (not just low-star reviews)
        # This handles the "Irony Paradox" where 5-star reviews contain pain keywords
        has_pain_keyword = self._identify_pain_keyword_reviews(df_filtered)
        negative_reviews = df_filtered[has_pain_keyword].copy()
        negative_count = len(negative_reviews)
        negative_ratio = negative_count / total_reviews if total_reviews > 0 else 0.0
        
        logger.info(f"Negative reviews (pain-keyword based): {negative_count} / {total_reviews} = {negative_ratio:.2%}")
        
        # Step 6: Calculate slope (predictive analytics)
        # T-011 Fix: Now uses pain-keyword-driven signals
        volatility_slope = self.calculate_slope(df_filtered)
        
        # Step 7: Calculate keyword density (prescriptive analytics)
        category_counts = self.calculate_keyword_density(df_filtered)
        
        # Step 8: Calculate volatility score (volume impact)
        # Volume score = number of pain-keyword reviews (used in risk score calculation)
        volatility_score = float(negative_count)
        
        # Step 9: Calculate risk score (T-012: MECE Pillar + Boost formula)
        risk_score, pillar_densities, primary_pillar = self.calculate_risk_score(
            slope=volatility_slope,
            volatility_score=volatility_score,
            category_counts=category_counts,
            total_reviews=total_reviews
        )
        
        # Step 10: Detect version impact (if version column exists)
        broken_update_detected = False
        suspected_version = None
        if 'version' in df_filtered.columns:
            # T-011 Fix: Use pain-keyword reviews instead of low-star reviews
            # Check if there's a spike in pain-keyword reviews for a specific version
            version_negative_counts = df_filtered[has_pain_keyword].groupby('version').size()
            if len(version_negative_counts) > 0:
                max_version = version_negative_counts.idxmax()
                max_count = version_negative_counts.max()
                # If a version has significantly more pain-keyword reviews, flag it
                if max_count > (negative_count * 0.3):  # More than 30% of negatives
                    broken_update_detected = True
                    suspected_version = str(max_version)
        
        # Step 11: Build top pain categories (sorted by impact)
        top_pain_categories = []
        if self.pain_keywords and 'categories' in self.pain_keywords:
            for category_name, count in category_counts.items():
                if count > 0 and category_name in self.pain_keywords['categories']:
                    weight = self.pain_keywords['categories'][category_name].get('weight', 0)
                    top_pain_categories.append({
                        'category': category_name,
                        'count': count,
                        'weight': weight
                    })
        
        # Sort by impact (count * weight) descending
        top_pain_categories.sort(key=lambda x: x['count'] * x['weight'], reverse=True)
        
        # Step 12: Extract evidence (sample negative reviews)
        evidence = []
        if not negative_reviews.empty:
            # Get top 5 most "helpful" negative reviews (by text length as proxy)
            text_col = 'text' if 'text' in negative_reviews.columns else 'title'
            if text_col in negative_reviews.columns:
                # Calculate text length for sorting
                negative_reviews_copy = negative_reviews.copy()
                negative_reviews_copy['_text_length'] = negative_reviews_copy[text_col].astype(str).str.len()
                # Sort by length descending and take top 5
                evidence_reviews = negative_reviews_copy.nlargest(5, '_text_length', keep='first')
                for _, review in evidence_reviews.iterrows():
                    review_text = str(review.get('text', review.get('title', '')))
                    if review_text:
                        evidence.append(review_text[:200])  # Limit length
        
        # Step 13: Build schema_app_gap.json structure (T-012: Enhanced with MECE pillars)
        analysis_result = {
            "app_name": app_name,
            "analysis_date": datetime.now(timezone.utc).strftime("%Y-%m-%d"),
            "metrics": {
                "total_reviews_90d": total_reviews,
                "negative_ratio": round(negative_ratio, 3),
                "volatility_slope": round(volatility_slope, 4),
                "risk_score": risk_score
            },
            "signals": {
                "broken_update_detected": broken_update_detected,
                "suspected_version": suspected_version,
                "top_pain_categories": top_pain_categories[:5],  # Top 5 only
                # T-012: Add MECE pillar information
                "pillar_densities": {
                    "Functional": round(pillar_densities.get("Functional", 0.0), 4),
                    "Economic": round(pillar_densities.get("Economic", 0.0), 4),
                    "Experience": round(pillar_densities.get("Experience", 0.0), 4)
                },
                "primary_pillar": primary_pillar
            },
            "evidence": evidence
        }
        
        logger.info(
            f"Analysis complete for {app_name}: "
            f"Risk Score={risk_score}, Slope={volatility_slope:.4f}, "
            f"Negative Ratio={negative_ratio:.2%}"
        )
        
        return analysis_result
    
    def _empty_analysis_result(self, app_name: str) -> Dict[str, Any]:
        """Generate empty analysis result structure (T-012: Enhanced with MECE pillars)."""
        return {
            "app_name": app_name,
            "analysis_date": datetime.now(timezone.utc).strftime("%Y-%m-%d"),
            "metrics": {
                "total_reviews_90d": 0,
                "negative_ratio": 0.0,
                "volatility_slope": 0.0,
                "risk_score": 0.0
            },
            "signals": {
                "broken_update_detected": False,
                "suspected_version": None,
                "top_pain_categories": [],
                # T-012: Add MECE pillar information
                "pillar_densities": {
                    "Functional": 0.0,
                    "Economic": 0.0,
                    "Experience": 0.0
                },
                "primary_pillar": "None"
            },
            "evidence": []
        }
    
    def save_analysis(self, analysis_result: Dict[str, Any], output_path: Path) -> None:
        """
        Save analysis results to schema_app_gap.json file.
        
        Args:
            analysis_result: Analysis results dictionary (from analyze())
            output_path: Path to save JSON file
        """
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(analysis_result, f, indent=2, ensure_ascii=False, default=str)
        
        logger.info(f"Saved analysis results to {output_path}")
