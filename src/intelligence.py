"""Forensic Intelligence module for T-008: Irrefutable Evidence reporting."""
import json
import logging
import re
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, Any, List, Optional, Tuple

import pandas as pd
import numpy as np

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Optional sklearn for N-Gram analysis
try:
    from sklearn.feature_extraction.text import CountVectorizer
    HAS_SKLEARN = True
except ImportError:
    HAS_SKLEARN = False
    logger.warning("sklearn not installed; N-Gram analysis will use fallback (collections.Counter)")


class ForensicAnalyzer:
    """
    T-008: Forensic Intelligence Engine.
    
    Intermediate processing layer between Analyzer (Statistics) and Reporter (Markdown).
    Derives meaning from raw stats: timelines, semantic clusters, migration flows.
    
    Input: Raw Reviews DataFrame (reviews_df) - required for N-Gram and Timeline.
    Output: intelligence.json, niche_matrix.json
    """

    # MECE Pillar mapping (Design 2.2)
    PILLAR_MAPPING = {
        "critical": "Functional",
        "performance": "Functional",
        "privacy": "Functional",
        "ai_quality": "Functional",
        "scam_financial": "Economic",
        "subscription": "Economic",
        "broken_promise": "Economic",
        "ads": "Economic",
        "usability": "Experience",
        "competitor_mention": "Experience",
        "generic_pain": "Experience",
    }

    # T-023: Domain vocabulary for Whale detection (> 40 words OR contains these)
    WHALE_DOMAIN_VOCAB = {
        "latency", "vector", "workflow", "pipeline", "integration", "api",
        "batch", "export", "sync", "sync failed", "credits", "quota",
        "render", "export", "4k", "resolution", "frame rate",
    }

    # T-023: Whale multiplier for Pain Density (3x weight)
    WHALE_MULTIPLIER = 3.0

    # Common stop words for N-Gram filtering
    STOP_WORDS = {
        "the", "a", "an", "is", "are", "was", "were", "be", "been", "being",
        "have", "has", "had", "do", "does", "did", "will", "would", "could",
        "should", "may", "might", "must", "shall", "can", "need", "dare",
        "to", "of", "in", "for", "on", "with", "at", "by", "from", "as",
        "into", "through", "during", "before", "after", "above", "below",
        "good", "great", "nice", "love", "best", "awesome", "amazing",
    }

    def __init__(self, pain_keywords_path: Path = None, app_name: str = ""):
        """
        Initialize ForensicAnalyzer.

        Args:
            pain_keywords_path: Path to pain_keywords.json (for pain density)
            app_name: Current app name (for stop-word filtering in N-Grams)
        """
        self.pain_keywords = None
        self.app_name = app_name or ""
        if pain_keywords_path and pain_keywords_path.exists():
            with open(pain_keywords_path, "r", encoding="utf-8") as f:
                self.pain_keywords = json.load(f)

    def _reviews_to_dataframe(self, reviews: List[Dict[str, Any]]) -> pd.DataFrame:
        """Convert reviews list to DataFrame with normalized date/text/score columns."""
        if not reviews:
            return pd.DataFrame()

        df = pd.DataFrame(reviews)

        # Normalize date
        date_cols = ["date", "reviewDate", "createdAt", "updatedAt"]
        date_col = next((c for c in date_cols if c in df.columns), None)
        if date_col:
            df["date"] = pd.to_datetime(df[date_col], errors="coerce", utc=True)
            df = df.dropna(subset=["date"])
        else:
            df["date"] = pd.Timestamp.now(tz=timezone.utc)

        # Normalize score/rating
        score_cols = ["score", "rating", "starRating", "stars"]
        score_col = next((c for c in score_cols if c in df.columns), None)
        if score_col:
            df["score"] = pd.to_numeric(df[score_col], errors="coerce").fillna(3).astype(int).clip(1, 5)
        else:
            df["score"] = 3

        # Normalize text
        text_cols = ["text", "reviewText", "content", "body", "comment"]
        text_col = next((c for c in text_cols if c in df.columns), None)
        if text_col:
            df["text"] = df[text_col].fillna("").astype(str)
        else:
            df["text"] = ""
        if "title" in df.columns:
            df["text"] = (df["title"].fillna("") + " " + df["text"]).str.strip()

        return df

    def _has_pain_keyword(self, text: str) -> bool:
        """Check if text contains any pain keyword."""
        if not self.pain_keywords or "categories" not in self.pain_keywords:
            return False
        text_lower = text.lower()
        for cat_data in self.pain_keywords["categories"].values():
            for kw in cat_data.get("keywords", []):
                if kw.lower() in text_lower:
                    return True
        return False

    def _is_whale_review(self, text: str) -> bool:
        """
        T-023: Whale detection - high-value reviews (long or domain-specific).

        Returns True if review has > 40 words OR contains domain vocabulary.
        """
        if not text or not isinstance(text, str):
            return False
        text_lower = text.lower()
        word_count = len(text_lower.split())
        if word_count > 40:
            return True
        return any(vocab in text_lower for vocab in self.WHALE_DOMAIN_VOCAB)

    def _get_pain_weight(self, has_pain: bool, is_whale: bool) -> float:
        """T-023: Return pain contribution (1.0 or WHALE_MULTIPLIER for whale reviews)."""
        if not has_pain:
            return 0.0
        return self.WHALE_MULTIPLIER if is_whale else 1.0

    def detect_event_timeline(
        self,
        reviews_df: pd.DataFrame,
        min_reviews_per_week: int = 5,
    ) -> List[Dict[str, Any]]:
        """
        T-008 2.1: Timeline of Pain - Event Detection.

        Group reviews by week (ISO), calculate Pain Density per week,
        flag anomalies where Density > (rolling_mean + 2*std).

        Args:
            reviews_df: DataFrame with 'date', 'text' columns
            min_reviews_per_week: Ignore weeks with fewer reviews (noise filter)

        Returns:
            List of {week, density, event} dicts
        """
        if reviews_df.empty or "date" not in reviews_df.columns or "text" not in reviews_df.columns:
            return []

        df = reviews_df.copy()
        df["date"] = pd.to_datetime(df["date"], errors="coerce", utc=True)
        df = df.dropna(subset=["date"])
        if df.empty:
            return []

        # Mark reviews with pain keywords
        df["has_pain"] = df["text"].apply(self._has_pain_keyword)
        # T-023: Whale-adjusted pain weight for density (3x for whale reviews)
        df["is_whale"] = df["text"].apply(self._is_whale_review)
        df["pain_weight"] = df.apply(
            lambda r: self._get_pain_weight(r["has_pain"], r["is_whale"]), axis=1
        )

        # T-022: Keep copy with version for Named Spike correlation
        cols = ["date", "text"]
        if "version" in df.columns:
            cols.append("version")
        df_with_version = df[cols].copy()
        if "version" not in df_with_version.columns:
            df_with_version["version"] = ""
        df_with_version["version"] = df_with_version["version"].fillna("").astype(str)

        # Resample by week (W-MON for ISO week start)
        # T-023: Use pain_weight (whale-adjusted) instead of raw pain_count for density
        df = df.set_index("date")
        weekly = df.resample("W-MON").agg(
            total=("text", "count"),
            pain_count=("pain_weight", "sum"),
        )
        weekly = weekly[weekly["total"] >= min_reviews_per_week]
        if len(weekly) < 2:
            return []

        weekly["density"] = weekly["pain_count"] / weekly["total"]
        weekly["week_str"] = weekly.index.strftime("%Y-%W")

        # Rolling mean and std for anomaly detection (μ + 2σ)
        weekly["rolling_mean"] = weekly["density"].rolling(window=min(4, len(weekly)), min_periods=1).mean()
        weekly["rolling_std"] = weekly["density"].rolling(window=min(4, len(weekly)), min_periods=1).std().fillna(0)
        threshold = weekly["rolling_mean"] + 2 * weekly["rolling_std"]
        weekly["is_anomaly"] = weekly["density"] > threshold

        result = []
        for idx, row in weekly.iterrows():
            event = None
            version_label = None
            if row["is_anomaly"]:
                # T-022: Named Spike - find most frequent version in this week's window
                version_label = self._name_spike(idx, df_with_version)
                if version_label:
                    event = f"The Version {version_label} Spike"
                else:
                    event = "Critical Spike"

            entry = {
                "week": row["week_str"],
                "density": round(float(row["density"]), 4),
                "total": int(row["total"]),
                "pain_count": int(row["pain_count"]),
                "event": event,
            }
            if version_label:
                entry["version"] = version_label
            result.append(entry)
        return result

    def _name_spike(self, week_start: pd.Timestamp, df: pd.DataFrame) -> Optional[str]:
        """
        T-022: Named Spike Correlation.

        For an anomaly week, search reviews in that window for the most frequent
        'version' string. Returns the version label for "The Version [X] Spike".

        Args:
            week_start: Week start Timestamp (Monday)
            df: DataFrame with date, version columns

        Returns:
            Most frequent version string, or None if no version data
        """
        if df.empty or "version" not in df.columns:
            return None

        week_end = week_start + pd.Timedelta(days=7)
        mask = (df["date"] >= week_start) & (df["date"] < week_end)
        week_reviews = df.loc[mask]

        if week_reviews.empty:
            return None

        versions = week_reviews["version"].replace("", np.nan).dropna()
        if len(versions) == 0:
            return None

        # Most frequent version
        vc = versions.astype(str).value_counts()
        if vc.empty:
            return None
        top_version = vc.index[0]
        if not top_version or top_version == "nan":
            return None
        return str(top_version)

    def extract_semantic_clusters(
        self,
        text_series: pd.Series,
        ngram_range: Tuple[int, int] = (2, 3),
        top_n: int = 5,
    ) -> List[Tuple[str, int]]:
        """
        T-008 2.2: Semantic Clustering - N-Gram Analysis.

        Discover unknown pain points not in pain_keywords.json.
        Uses sklearn CountVectorizer (or fallback) on 2-3 word phrases.

        Args:
            text_series: Series of review texts (rating <= 2 preferred)
            ngram_range: (min_n, max_n) for n-grams
            top_n: Number of top phrases to return

        Returns:
            List of (phrase, count) tuples
        """
        if text_series.empty or text_series.str.len().sum() == 0:
            return []

        texts = text_series.fillna("").astype(str).tolist()
        texts = [t.strip() for t in texts if len(t.strip()) > 3]

        # Build stop words: standard + app name tokens
        stop = set(self.STOP_WORDS)
        app_tokens = set(re.findall(r"\b\w+\b", self.app_name.lower()))
        stop.update(app_tokens)

        if HAS_SKLEARN:
            try:
                vectorizer = CountVectorizer(
                    ngram_range=ngram_range,
                    stop_words=list(stop),
                    max_features=100,
                    min_df=2,
                )
                X = vectorizer.fit_transform(texts)
                counts = np.asarray(X.sum(axis=0)).flatten()
                terms = vectorizer.get_feature_names_out()
                pairs = list(zip(terms, counts))
            except Exception as e:
                logger.warning(f"CountVectorizer failed: {e}")
                return self._fallback_ngrams(texts, top_n)
        else:
            return self._fallback_ngrams(texts, top_n)

        # Filter generic phrases (Req 2.2: "sync failed" valid; "good app" invalid)
        generic = {
            "good app", "great app", "best app", "nice app", "love it", "love this",
            "this app", "and there", "there s", "it s", "i m", "don t", "can t",
        }
        pairs = [(p, c) for p, c in pairs if p not in generic and len(p.split()) >= 2]
        pairs.sort(key=lambda x: -x[1])
        return pairs[:top_n]

    def _fallback_ngrams(self, texts: List[str], top_n: int) -> List[Tuple[str, int]]:
        """Fallback N-Gram using collections.Counter."""
        from collections import Counter
        generic = {
            "good app", "great app", "best app", "this app", "and there", "there s",
            "it s", "i m", "don t", "can t", "love it", "love this", "but i", "no way",
        }
        all_ngrams = []
        for text in texts:
            words = [w.lower() for w in re.findall(r"\b\w+\b", text) if w.lower() not in self.STOP_WORDS]
            for i in range(len(words) - 1):
                bigram = f"{words[i]} {words[i+1]}"
                if len(bigram) > 4 and bigram not in generic:
                    all_ngrams.append(bigram)
            for i in range(len(words) - 2):
                trigram = f"{words[i]} {words[i+1]} {words[i+2]}"
                if len(trigram) > 6:
                    all_ngrams.append(trigram)
        counts = Counter(all_ngrams)
        return counts.most_common(top_n)

    def map_competitor_migration(
        self,
        text_series: pd.Series,
        competitors_list: List[str],
        score_series: Optional[pd.Series] = None,
    ) -> List[Dict[str, Any]]:
        """
        T-008 2.3 / T-018: Competitor Migration Graphing.

        Scan review text for competitor mentions in Churn context only.
        T-018: Strict regex - (switched|moved|migrated|changed) to {app}.
        Ignores "better than {app}" (Comparison) to avoid false positives.

        Args:
            text_series: Review texts
            competitors_list: App names from targets.json (exclude current app)
            score_series: Optional review scores (1-5) - unused after T-018 refinement

        Returns:
            List of {competitor, type, count} where type is "churn"
        """
        if text_series.empty or not competitors_list:
            return []

        churn_counts: Dict[str, int] = {}

        for idx, text in text_series.items():
            if not isinstance(text, str) or len(text.strip()) < 5:
                continue
            text_lower = text.lower()

            for comp in competitors_list:
                comp_lower = comp.lower().replace("_", " ")
                if comp_lower not in text_lower:
                    continue

                # T-018: Strict regex - competitor must appear in "X to {app}" context
                # (switched|moved|migrated|changed) to {app}
                comp_escaped = re.escape(comp_lower)
                churn_pattern = rf"(?:switched|moved|migrated|changed)\s+to\s+{comp_escaped}"
                if re.search(churn_pattern, text_lower):
                    churn_counts[comp] = churn_counts.get(comp, 0) + 1
                # Explicitly ignore "better than {app}" - do not count as comparison

        return [{"competitor": comp, "type": "churn", "count": count} for comp, count in churn_counts.items()]

    def generate_matrix(
        self,
        analyses: List[Dict[str, Any]],
    ) -> Dict[str, Dict[str, float]]:
        """
        T-008 2.4: Feature/Fail Matrix for Niche Reports.

        Build {app_name: {pillar: score}} from analyses with pillar_densities.

        Args:
            analyses: List of schema_app_gap.json structures

        Returns:
            Dict suitable for reports/niche_matrix.json
        """
        matrix = {}
        for a in analyses:
            app_name = a.get("app_name", "Unknown")
            pillar_densities = a.get("signals", {}).get("pillar_densities", {})
            if not pillar_densities:
                matrix[app_name] = {"Functional": 0.0, "Economic": 0.0, "Experience": 0.0}
                continue
            # Normalize densities to 0-100 scale (density * 10, capped at 100)
            matrix[app_name] = {
                "Functional": round(min(100.0, float(pillar_densities.get("Functional", 0)) * 10), 2),
                "Economic": round(min(100.0, float(pillar_densities.get("Economic", 0)) * 10), 2),
                "Experience": round(min(100.0, float(pillar_densities.get("Experience", 0)) * 10), 2),
            }
        return matrix

    def run_forensic(
        self,
        reviews: List[Dict[str, Any]],
        app_name: str,
        competitors: List[str],
    ) -> Dict[str, Any]:
        """
        Run full forensic analysis on reviews.

        Returns intelligence dict with timeline, clusters, migration.
        """
        self.app_name = app_name
        df = self._reviews_to_dataframe(reviews)
        if df.empty:
            return {"timeline": [], "clusters": [], "migration": []}

        # Exclude current app from competitors
        competitors = [c for c in competitors if c.lower() != app_name.lower().replace(" ", "_")]

        timeline = self.detect_event_timeline(df)
        negative_df = df[df["score"] <= 2]
        clusters = self.extract_semantic_clusters(negative_df["text"], top_n=5)
        migration = self.map_competitor_migration(df["text"], competitors, df["score"])

        return {
            "timeline": timeline,
            "clusters": [{"phrase": p, "count": c} for p, c in clusters],
            "migration": migration,
        }
