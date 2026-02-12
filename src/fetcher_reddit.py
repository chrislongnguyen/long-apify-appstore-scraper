"""
RedditFetcher — Reddit context for Venture Architect (Phase 7.3).

T-030: Fetches niche context from Reddit via Apify automation-lab/reddit-scraper.
Output is normalized for construct_holographic_icp (title, text, subreddit, url, comments).
"""
import json
import logging
from pathlib import Path
from typing import Any, Dict, List, Optional
from urllib.parse import quote_plus

from apify_client import ApifyClient
from tenacity import retry, stop_after_attempt, wait_exponential, retry_if_exception_type

logger = logging.getLogger(__name__)

ACTOR_ID = "automation-lab/reddit-scraper"


class RedditFetcher:
    """
    Fetches Reddit posts/search results for niche context (Venture Architect Context Signal).
    Uses Apify actor automation-lab/reddit-scraper; input schema may vary — see actor docs.
    """

    def __init__(self, apify_token: Optional[str] = None, settings: Optional[Dict[str, Any]] = None):
        self.apify_token = apify_token
        self.settings = settings or {}
        self._client: Optional[ApifyClient] = None

    @property
    def client(self) -> ApifyClient:
        if self._client is None:
            import os
            token = self.apify_token or os.getenv("APIFY_API_KEY")
            if not token:
                raise ValueError("Apify API token required. Set APIFY_API_KEY or pass apify_token.")
            self._client = ApifyClient(token)
        return self._client

    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=2, max=10),
        retry=retry_if_exception_type((ConnectionError, TimeoutError)),
        reraise=True,
    )
    def fetch_niche_context(
        self,
        subreddits: List[str],
        search_queries: List[str],
        max_posts: int = 50,
        max_comments_per_post: int = 10,
    ) -> List[Dict[str, Any]]:
        """
        Fetch Reddit context for a niche (search within subreddits or globally).

        Uses actor automation-lab/reddit-scraper with URL sources ("urls"),
        which is confirmed by actor example input and is the most reliable mode.

        Args:
            subreddits: Subreddit names without r/ (e.g. ["nosurf", "digitalminimalism"]).
            search_queries: Search terms (e.g. ["screen time app", "phone addiction"]).
            max_posts: Max posts to fetch per source (configurable via venture_architect.max_posts).
            max_comments_per_post: Max comments to keep per post in normalized output (configurable via venture_architect.max_comments_per_post).

        Returns:
            List of normalized dicts: {title, text, subreddit, url, comments}.
        """
        if not search_queries and not subreddits:
            logger.warning("RedditFetcher: no subreddits or search_queries; returning empty list.")
            return []

        # Build actor-compatible URLs:
        # - Subreddit listings: https://www.reddit.com/r/{subreddit}/
        # - Global search:      https://www.reddit.com/search/?q={query}
        # - Subreddit search:   https://www.reddit.com/r/{subreddit}/search/?q={query}&restrict_sr=1
        urls: List[str] = []
        clean_subs = [s.replace("r/", "").strip() for s in subreddits if isinstance(s, str) and s.strip()]
        for s in clean_subs[:20]:
            urls.append(f"https://www.reddit.com/r/{s}/")
        for q in search_queries[:10]:
            if not isinstance(q, str) or not q.strip():
                continue
            qq = quote_plus(q.strip())
            # Global search (safe default)
            urls.append(f"https://www.reddit.com/search/?q={qq}")
            # If subreddits provided, add scoped searches for better niche signal
            for s in clean_subs[:10]:
                urls.append(f"https://www.reddit.com/r/{s}/search/?q={qq}&restrict_sr=1&sort=relevance&t=year")

        # De-duplicate while preserving order
        urls = list(dict.fromkeys(urls))
        if not urls:
            logger.warning("RedditFetcher: no valid URLs generated from inputs; returning empty list.")
            return []

        # Actor example input:
        # {"urls": [...], "maxPostsPerSource": 5, "sort": "hot", "maxComments": N}
        run_input: Dict[str, Any] = {
            "urls": urls,
            "sort": "relevance",
            "time": "year",
            "maxPostsPerSource": max_posts,
            "maxItems": max_posts,  # compatibility with actors using maxItems
            "includeComments": True,
            "maxComments": max_comments_per_post,  # actor limit per post when supported
            "proxyConfiguration": {"useApifyProxy": True},
        }

        logger.info(
            "Fetching Reddit context: actor=%s, urls=%d, queries=%s, subreddits=%s, maxPostsPerSource=%s, maxCommentsPerPost=%s",
            ACTOR_ID, len(urls), (search_queries or [])[:5], (subreddits or [])[:5], max_posts, max_comments_per_post,
        )
        run = self.client.actor(ACTOR_ID).call(run_input=run_input)
        dataset_items = list(self.client.dataset(run["defaultDatasetId"]).iterate_items())
        normalized = self._normalize_items(dataset_items, max_comments_per_post=max_comments_per_post)
        logger.info("Reddit context: fetched %d raw items, normalized %d", len(dataset_items), len(normalized))
        return normalized

    def _normalize_items(
        self, items: List[Dict[str, Any]], max_comments_per_post: int = 10
    ) -> List[Dict[str, Any]]:
        """Map actor output to {title, text, subreddit, url, comments}. Dedup by URL. Cap comments per post."""
        # I3: Dedup by URL before normalization (preserve first occurrence)
        seen_urls: set = set()
        deduped: List[Dict[str, Any]] = []
        for item in items:
            if not isinstance(item, dict):
                continue
            url = (
                item.get("url")
                or item.get("permalink")
                or item.get("link")
                or ""
            )
            if url and not url.startswith("http"):
                url = "https://www.reddit.com" + (url if url.startswith("/") else "/" + url)
            key = url or str(id(item))
            if key in seen_urls:
                continue
            seen_urls.add(key)
            deduped.append(item)

        out = []
        for item in deduped:
            if not isinstance(item, dict):
                continue
            # Common actor fields: title, body, selftext, text, subreddit, url, permalink, comments
            title = (
                item.get("title")
                or item.get("headline")
                or ""
            )
            text = (
                item.get("body")
                or item.get("selftext")
                or item.get("text")
                or item.get("content")
                or ""
            )
            subreddit = (
                item.get("subreddit")
                or (item.get("subredditName") or {}).get("name") if isinstance(item.get("subredditName"), dict) else ""
            ) or ""
            if isinstance(subreddit, dict):
                subreddit = subreddit.get("name", "") or ""
            url = (
                item.get("url")
                or item.get("permalink")
                or item.get("link")
                or ""
            )
            if url and not url.startswith("http"):
                url = "https://www.reddit.com" + (url if url.startswith("/") else "/" + url)
            comments_raw = item.get("comments") or item.get("replies") or []
            comments = []
            if isinstance(comments_raw, list):
                for c in comments_raw[:max_comments_per_post]:
                    if isinstance(c, dict):
                        comments.append(c.get("body") or c.get("text") or c.get("content") or str(c)[:200])
                    elif isinstance(c, str):
                        comments.append(c[:500])
            elif isinstance(comments_raw, str):
                comments = [comments_raw[:500]]

            out.append({
                "title": str(title)[:500],
                "text": str(text)[:2000],
                "subreddit": str(subreddit),
                "url": str(url),
                "comments": comments,
            })
        return out

    def save_context(self, data: List[Dict[str, Any]], path: Path) -> None:
        """Save raw normalized context to JSON for cache/replay."""
        path.parent.mkdir(parents=True, exist_ok=True)
        with open(path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        logger.info("Saved Reddit context to %s", path)
