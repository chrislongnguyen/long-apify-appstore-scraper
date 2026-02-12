"""
Venture Architect — 3-stage LLM pipeline for Venture Blueprint (Phase 7).

T-026: Maps User Psychology → System Dynamics → Strategic Principles.
"""
import json
import logging
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

from src.ai_client import AIClient
from src.intelligence import ForensicAnalyzer
from src.reporter import Reporter
from src.schemas import EPSPrescription, HolographicICP, SystemDynamicsMap

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
WHALE_DOMAIN_VOCAB = ForensicAnalyzer.WHALE_DOMAIN_VOCAB

# --- System Prompts (Design §4.6) ---
ICP_SYSTEM_PROMPT = """You are a Cultural Anthropologist and Consumer Psychologist.

YOUR TASK: Construct a "Holographic ICP" (Ideal Customer Profile) by
triangulating three independent data signals about users of "{app_name}".

DATA SIGNALS PROVIDED:
1. PAIN SIGNAL (1-2★ App Store reviews): What makes users LEAVE.
2. SUCCESS SIGNAL (5★ "Whale" reviews, >40 words OR domain vocabulary): What makes users STAY.
3. CONTEXT SIGNAL (Reddit threads): How users talk about this problem
   OUTSIDE the app — alternatives, workarounds, real-world triggers.

ANALYSIS RULES:
- If Pain says "Too complex" but Success says "Love the depth," the ICP is
  SPLIT. Identify which segment is the "Whale" (high-LTV).
- The "Ultimate Desired Outcome" (UDO) is NEVER the feature itself.
  Go deeper: "Weight loss" → "Social confidence" → "Effortless metabolic control."
- Use Reddit to find WHERE the app fits in their life (trigger context).
- Look for ALTERNATIVES mentioned: competitors, spreadsheets, pen & paper.

OUTPUT: Respond with a single JSON object matching this exact schema:
{who, why_udo, what_how_workflow, when_trigger, alternatives,
 icp_segment, pain_success_paradox, user_personas}

The "who" field must be a dict with keys like demographic, psychographic.

I4 — USER PERSONAS (required): Include exactly 3 non-overlapping user_personas. Each persona must have:
- persona_name: short name (e.g. "The Reluctant Quitter")
- archetype: one-line archetype label
- user_story: 5-6 concise sentences tracing their journey: Who they are → What they want (UDO) → What drives them (UDS/UDS.UD) → What blocks them (UBS/UBS.UD) → Why they fail (UDS.UB) → What could save them (UBS.UB)
- segment: "primary", "secondary", or "whale_segment"

IMPORTANT: Output ONLY valid JSON. No preamble, no explanation, no markdown.
All string values must be plain text (no nested objects where strings are expected)."""

SYSTEM_DYNAMICS_PROMPT = """You are an Evolutionary Biologist and Behavioral Systems Architect.

YOUR TASK: Given the Holographic ICP and curated review evidence for
"{app_name}", populate a 7-Node System Dynamics Map.

THE 7 NODES:
1. UDO  — Ultimate Desired Outcome (the "adverb + noun" of their life)
2. UDS  — Ultimate Driving System (conscious force TOWARD UDO)
3. UDS.UD — Root Driver of UDS (why the motivation succeeds — usually Layer 5 Biology)
4. UDS.UB — Root Blocker of UDS (why the motivation fails — usually Layer 4 Psychology)
5. UBS  — Ultimate Blocking System (conscious force AWAY from UDO)
6. UBS.UD — Root Driver of UBS (why the PROBLEM keeps winning — usually Layer 5 Biology)
7. UBS.UB — Root Blocker of UBS (what NATURALLY kills the problem — the system's own weakness)

DEPTH LAYERS (apply to each node):
  Layer 1: App (Interface/Features)
  Layer 2: Behavior (Habits/Workflows)
  Layer 3: System (Feedback Loops)
  Layer 4: Psychology (Biases — Fear, Ego, Status, Loss Aversion)
  Layer 5: Biology (Dopamine, Cortisol, Ghrelin, Energy Conservation)

CRITICAL RULES:
- Every node MUST include at least one "evidence" quote from the reviews or Reddit.
- UDS.UD and UBS.UD MUST reach Layer 5 (Biology). If you stop at Layer 3, go deeper.
- "Incumbent Failure" must explain which Layer the current app addresses vs. which it ignores.
- Think like Darwin, not like a PM. The user is an organism optimizing survival, not a "customer."

OUTPUT: Respond with a single JSON object matching this exact schema:
{udo, uds, uds_ud, uds_ub, ubs, ubs_ud, ubs_ub, incumbent_failure, depth_layers}

Each of uds, uds_ud, uds_ub, ubs, ubs_ud, ubs_ub must have: label, evidence (list of strings), layer.
The udo must have: statement, adverb, noun.
The depth_layers must be a dict (not a list).

IMPORTANT: Output ONLY valid JSON. No preamble, no explanation, no markdown.
All string values must be plain text (no nested objects where strings are expected)."""

EPS_SYSTEM_PROMPT = """You are a Product Architect and Strategic Inverter.

YOUR TASK: Given the 7-Node System Dynamics Map and the ICP for "{app_name}",
derive the EPS (Environment, Principles, SOP & Tools) Solution System.

THE INVERSION RULES (non-negotiable):
1. Principles MUST map 1:1 to system nodes:
   - Principle to AMPLIFY UDS.UD (feed the root motivation)
   - Principle to DISABLE UDS.UB (remove the motivation killer)
   - Principle to STARVE UBS.UD (make the problem's engine work FOR us)
   - Principle to AMPLIFY UBS.UB (trigger the problem's natural weakness)
2. Environment is DERIVED from Principles:
   - If Principle says "Zero Cognitive Load," then Environment CANNOT be a full app.
   - State the anti-pattern (what the incumbent does wrong).
3. Tools have TWO layers:
   - "Desirable Wrapper" (Layer 1 — the feature the user THINKS they want)
   - "Effective Core" (Layer 5 — the mechanism that actually solves the root cause)
4. SOP must specify actor ("User" or "System") for each step.

THE STRATEGIC INVERSION TABLE:
For each major incumbent method, show:
  [Incumbent Method] → [Root Cause Node] → [New Principle]

THE TROJAN HORSE:
  Keys: "level_1_desirable" (The Hook/Marketing Promise — what the user THINKS they're getting),
        "level_5_effective" (The Cure/Biological Mechanism — what actually fixes the root cause).
  Content MUST be two different strings.

OUTPUT: Respond with a single JSON object matching this exact schema:
{principles, environment, tools, sop, trojan_horse, strategic_inversion_table}

IMPORTANT: Output ONLY valid JSON. No preamble, no explanation, no markdown.
All string values must be plain text (no nested objects where strings are expected).
Principles must have: id, name, strategy, node_ref, rationale. Include at least 4 principles."""


def _word_count(text: str) -> int:
    """Count words in text."""
    return len((text or "").split())


def _is_whale_text(text: str) -> bool:
    """Forensic-consistent whale logic: >40 words OR domain vocabulary."""
    if not text or not isinstance(text, str):
        return False
    text_lower = text.lower()
    if _word_count(text_lower) > 40:
        return True
    return any(vocab in text_lower for vocab in WHALE_DOMAIN_VOCAB)


def _format_quote(review: Dict, prefix: str = "") -> str:
    """Format a review as a quote string."""
    title = (review.get("title") or "").strip()
    text = (review.get("text") or "").strip()
    score = review.get("score", "")
    parts = []
    if title:
        parts.append(title)
    if text:
        parts.append(text)
    s = " | ".join(parts) if parts else "(no text)"
    return f"{prefix}{score}★: \"{s[:200]}{'...' if len(s) > 200 else ''}\""


class VentureArchitect:
    """
    3-stage LLM pipeline: ICP → System Dynamics → EPS.
    """

    def __init__(
        self,
        ai_client: AIClient,
        pain_keywords_path: Optional[Path] = None,
        reporter: Optional[Reporter] = None,
        settings: Optional[Dict[str, Any]] = None,
    ):
        self.ai_client = ai_client
        self.settings = settings or {}
        self.pain_keywords_path = pain_keywords_path
        self.reporter = reporter

    def _extract_pain_reviews(self, filtered_reviews: List[Dict]) -> List[Dict]:
        """Extract reviews with rating ≤ 2 (Pain Signal)."""
        return [r for r in filtered_reviews if (r.get("score") or 0) <= 2]

    def _extract_success_reviews(self, raw_reviews: List[Dict], min_words: int = 40) -> List[Dict]:
        """Extract 5★ whale reviews (>40 words OR domain vocab) as Success Signal."""
        return [
            r for r in raw_reviews
            if (r.get("score") or 0) == 5
            and (
                _word_count((r.get("text") or "") + " " + (r.get("title") or "")) >= min_words
                or _is_whale_text((r.get("text") or "") + " " + (r.get("title") or ""))
            )
        ]

    def _curate_evidence(
        self,
        pain_reviews: List[Dict],
        success_reviews: List[Dict],
        max_quotes: int = 10,
        whale_priority: bool = True,
    ) -> List[str]:
        """
        Curate evidence quotes, capping at ~3000 tokens worth.
        Whale priority: longer reviews (>40 words) first.
        """
        def _score(r: Dict) -> int:
            wc = _word_count((r.get("text") or "") + " " + (r.get("title") or ""))
            return (100 if wc >= 40 else 50) if whale_priority else wc

        combined = []
        for r in pain_reviews:
            combined.append((_score(r), _format_quote(r, "1-2★ ")))
        for r in success_reviews:
            combined.append((_score(r), _format_quote(r, "5★ ")))

        combined.sort(key=lambda x: -x[0])
        return [q for _, q in combined[:max_quotes]]

    def _curate_reddit_evidence(
        self, reddit_data: List[Dict], max_quotes: int = 10
    ) -> List[str]:
        """I2: Curate Reddit quotes for Stage 2 evidence pool (System Map). Returns list of strings."""
        if not reddit_data:
            return []
        lines = []
        for item in reddit_data[:max_quotes * 2]:
            if len(lines) >= max_quotes:
                break
            title = (item.get("title") or "").strip()
            text = (item.get("text") or "").strip()[:200]
            subreddit = (item.get("subreddit") or "").strip()
            prefix = f"Reddit r/{subreddit}: " if subreddit else "Reddit: "
            if title or text:
                line = f"{prefix}{title}" if title else f"{prefix}{text}"
                if text and title and text != title:
                    line += f" | {text}"
                lines.append(line)
        return lines[:max_quotes]

    def _summarize_reddit(
        self,
        reddit_data: List[Dict],
        max_items: int = 25,
        include_comments: bool = True,
        max_comments_in_summary: int = 2,
    ) -> str:
        """Summarize Reddit themes for ICP (Context Signal). I3: optional comment sampling per post."""
        if not reddit_data:
            return "No Reddit data available. Infer context from review text only."
        themes = []
        for item in reddit_data[:max_items]:
            title = (item.get("title") or "").strip()
            text = (item.get("text") or "").strip()[:150]
            subreddit = (item.get("subreddit") or "").strip()
            if not title and not text:
                continue
            prefix = f"r/{subreddit}: " if subreddit else ""
            line = f"- {prefix}{title}" if title else f"- {prefix}{text}"
            if text and title and text != title:
                line += f" | {text}"
            if include_comments:
                comments = item.get("comments") or []
                for c in (comments if isinstance(comments, list) else [])[:max_comments_in_summary]:
                    if c and isinstance(c, str) and c.strip():
                        line += f" [Comment: {c.strip()[:80]}...]" if len(c.strip()) > 80 else f" [Comment: {c.strip()}]"
            themes.append(line)
        return "\n".join(themes) if themes else "Reddit data provided but no extractable themes."

    def _repair_icp_response(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Coerce common LLM output mistakes to match HolographicICP schema."""
        out = dict(data)
        # why_udo / when_trigger must be strings (LLM sometimes returns dict/list)
        for key in ("why_udo", "when_trigger"):
            val = out.get(key)
            if isinstance(val, dict):
                # Preserve useful detail in a deterministic flat sentence.
                parts = []
                for k, v in val.items():
                    if isinstance(v, list):
                        vv = ", ".join(str(x) for x in v if x is not None)
                    else:
                        vv = str(v)
                    if vv and vv.strip():
                        parts.append(f"{k}: {vv}")
                out[key] = " | ".join(parts) if parts else ""
            elif isinstance(val, list):
                out[key] = " | ".join(str(x) for x in val if x is not None)
            elif val is None:
                out[key] = ""
            elif not isinstance(val, str):
                out[key] = str(val)
        # what_how_workflow must be list
        w = out.get("what_how_workflow")
        if isinstance(w, str):
            out["what_how_workflow"] = [s.strip() for s in w.split("\n") if s.strip()] or [w]
        elif not isinstance(w, list):
            out["what_how_workflow"] = []
        # alternatives must be list (LLM often returns string)
        alt = out.get("alternatives")
        if isinstance(alt, str):
            out["alternatives"] = [s.strip() for s in alt.replace("\n", ",").split(",") if s.strip()] or [alt]
        elif not isinstance(alt, list):
            out["alternatives"] = []
        # icp_segment must be dict
        seg = out.get("icp_segment")
        if isinstance(seg, str):
            out["icp_segment"] = {"primary": seg, "secondary": seg, "whale_segment": seg}
        elif not isinstance(seg, dict):
            out["icp_segment"] = {"primary": "", "secondary": "", "whale_segment": ""}
        # pain_success_paradox must be dict with pain_says, success_says, inference
        psp = out.get("pain_success_paradox")
        if isinstance(psp, str):
            out["pain_success_paradox"] = {"pain_says": psp, "success_says": "", "inference": psp}
        elif isinstance(psp, dict):
            pain_says = psp.get("pain_says") or psp.get("pain_complains") or psp.get("pain") or ""
            success_says = psp.get("success_says") or psp.get("success_loves") or psp.get("success") or ""
            inference = (
                psp.get("inference")
                or psp.get("paradox")
                or psp.get("paradox_identified")
                or psp.get("reconciliation")
                or psp.get("pricing_model")
                or ""
            )
            if isinstance(inference, dict):
                inference = inference.get("paradox", inference.get("inference", "")) or str(inference)
            # Fallback: use any string value if schema fields missing (LLM uses custom keys)
            if not inference and not pain_says and not success_says:
                for v in psp.values():
                    if isinstance(v, str) and len(v) > 10:
                        inference = v
                        break
            out["pain_success_paradox"] = {
                "pain_says": str(pain_says) if pain_says else "",
                "success_says": str(success_says) if success_says else "",
                "inference": str(inference) if inference else "",
            }
        else:
            out["pain_success_paradox"] = {"pain_says": "", "success_says": "", "inference": ""}
        # I4: user_personas must be list of dicts with persona_name, archetype, user_story, segment
        up = out.get("user_personas")
        if not isinstance(up, list):
            out["user_personas"] = []
        else:
            repaired = []
            segments = ("primary", "secondary", "whale_segment")
            for i, p in enumerate(up[:3]):
                if not isinstance(p, dict):
                    continue
                name = p.get("persona_name") or p.get("name") or p.get("archetype") or f"Persona {i + 1}"
                archetype = p.get("archetype") or p.get("persona_name") or name
                story = p.get("user_story") or p.get("story") or p.get("journey") or ""
                if isinstance(story, list):
                    story = " ".join(str(s) for s in story)
                seg = p.get("segment") or (segments[i] if i < len(segments) else "primary")
                repaired.append({
                    "persona_name": str(name),
                    "archetype": str(archetype),
                    "user_story": str(story),
                    "segment": str(seg),
                })
            out["user_personas"] = repaired
        return out

    def _repair_system_map_response(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Coerce common LLM output mistakes to match SystemDynamicsMap schema."""
        LAYER_NAMES = {1: "Layer 1 (App)", 2: "Layer 2 (Behavior)", 3: "Layer 3 (System)",
                       4: "Layer 4 (Psychology)", 5: "Layer 5 (Biology)"}
        out = dict(data)
        # depth_layers: schema expects Dict, LLM often returns list
        dl = out.get("depth_layers")
        if isinstance(dl, list):
            out["depth_layers"] = {str(i + 1): (x if isinstance(x, str) else str(x)) for i, x in enumerate(dl)}
        elif not isinstance(dl, dict):
            out["depth_layers"] = {}
        for key in ("udo", "uds", "uds_ud", "uds_ub", "ubs", "ubs_ud", "ubs_ub"):
            node = out.get(key)
            if isinstance(node, dict):
                layer = node.get("layer")
                if isinstance(layer, int):
                    node["layer"] = LAYER_NAMES.get(layer, str(layer))
                elif not isinstance(layer, str):
                    node["layer"] = "Unknown"
                if not isinstance(node.get("evidence"), list):
                    node["evidence"] = node.get("evidence", []) if isinstance(node.get("evidence"), list) else []
        return out

    def _repair_eps_response(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Coerce common LLM output mistakes to match EPSPrescription schema."""
        out = dict(data)
        # trojan_horse must be dict with level_1_desirable and level_5_effective
        th = out.get("trojan_horse")
        if isinstance(th, str):
            out["trojan_horse"] = {"level_1_desirable": th, "level_5_effective": "See Level 1"}
        elif isinstance(th, dict):
            l1 = th.get("level_1_desirable") or th.get("level_1") or th.get("hook") or th.get("desirable") or ""
            l5 = th.get("level_5_effective") or th.get("level_5") or th.get("cure") or th.get("effective") or ""
            if not l1 and not l5:
                # Grab any string values as fallback
                vals = [v for v in th.values() if isinstance(v, str) and len(v) > 5]
                l1 = vals[0] if len(vals) > 0 else ""
                l5 = vals[1] if len(vals) > 1 else "See Level 1"
            out["trojan_horse"] = {"level_1_desirable": str(l1), "level_5_effective": str(l5) or "See Level 1"}
        elif isinstance(th, list) and len(th) >= 2:
            out["trojan_horse"] = {"level_1_desirable": str(th[0]), "level_5_effective": str(th[1])}
        else:
            out["trojan_horse"] = {"level_1_desirable": "", "level_5_effective": ""}
        # principles must be list of dicts
        p = out.get("principles")
        if not isinstance(p, list):
            out["principles"] = []
        # environment, tools must be dicts
        for k in ("environment", "tools"):
            v = out.get(k)
            if not isinstance(v, dict):
                out[k] = {}
        # sop must be list
        s = out.get("sop")
        if not isinstance(s, list):
            out["sop"] = []
        # strategic_inversion_table must be list
        sit = out.get("strategic_inversion_table")
        if not isinstance(sit, list):
            out["strategic_inversion_table"] = []
        return out

    # --- Empty fallback objects for graceful degradation ---

    @staticmethod
    def _empty_icp() -> Dict[str, Any]:
        """Return a valid-but-empty HolographicICP dict."""
        return {
            "who": {"demographic": "Unknown", "psychographic": "Unknown"},
            "why_udo": "LLM stage failed — no ICP generated",
            "what_how_workflow": [],
            "when_trigger": "Unknown",
            "alternatives": [],
            "icp_segment": {"primary": "Error", "secondary": "Error", "whale_segment": "Error"},
            "pain_success_paradox": {"pain_says": "", "success_says": "", "inference": "Stage 1 failed"},
            "user_personas": [],
        }

    @staticmethod
    def _empty_system_map() -> Dict[str, Any]:
        """Return a valid-but-empty SystemDynamicsMap dict."""
        empty_node = {"label": "Unknown", "evidence": [], "layer": "Unknown"}
        return {
            "udo": {"statement": "Unknown", "adverb": "Unknown", "noun": "Unknown"},
            "uds": dict(empty_node), "uds_ud": dict(empty_node), "uds_ub": dict(empty_node),
            "ubs": dict(empty_node), "ubs_ud": dict(empty_node), "ubs_ub": dict(empty_node),
            "incumbent_failure": "LLM stage failed — no system map generated",
            "depth_layers": {},
        }

    @staticmethod
    def _empty_eps() -> Dict[str, Any]:
        """Return a valid-but-empty EPSPrescription dict."""
        return {
            "principles": [],
            "environment": {"form_factor": "Unknown", "rationale": "Stage 3 failed", "anti_pattern": ""},
            "tools": {"desirable_wrapper": "Unknown", "effective_core": "Unknown"},
            "sop": [],
            "trojan_horse": {"level_1_desirable": "Unknown", "level_5_effective": "Unknown"},
            "strategic_inversion_table": [],
        }

    def _summarize_analysis_signals(self, analysis: Dict) -> str:
        """Summarize analysis.signals for ICP prompt."""
        signals = analysis.get("signals", {}) or {}
        top = signals.get("top_pain_categories", [])
        if not top:
            return "No top pain categories."
        lines = [f"- {c.get('category', '')}: count={c.get('count', 0)}, weight={c.get('weight', 0)}" for c in top[:5]]
        return "\n".join(lines)

    def construct_holographic_icp(
        self,
        pain_reviews: List[Dict],
        success_reviews: List[Dict],
        reddit_data: List[Dict],
        analysis: Dict,
        app_name: str,
    ) -> Dict[str, Any]:
        """Stage 1: Triangulate Pain + Success + Context into Holographic ICP."""
        pain_quotes = self._curate_evidence(pain_reviews, [], max_quotes=10)
        success_quotes = self._curate_evidence([], success_reviews, max_quotes=10)
        reddit_summary = self._summarize_reddit(reddit_data)
        analysis_summary = self._summarize_analysis_signals(analysis)

        user_prompt = f"""PAIN QUOTES (1-2★):
{chr(10).join(pain_quotes) if pain_quotes else "(none)"}

SUCCESS QUOTES (5★ whale signals: >40 words OR domain vocabulary):
{chr(10).join(success_quotes) if success_quotes else "(none)"}

REDDIT/CONTEXT:
{reddit_summary}

ANALYSIS SIGNALS (top pain categories):
{analysis_summary}

Produce the Holographic ICP JSON for app "{app_name}"."""

        system_prompt = ICP_SYSTEM_PROMPT.replace("{app_name}", app_name)
        data = self.ai_client.generate_structured(
            system_prompt=system_prompt,
            user_prompt=user_prompt,
            response_model=None,
        )
        data = self._repair_icp_response(data)
        validated = HolographicICP.model_validate(data)
        return validated.model_dump()

    def map_system_dynamics(
        self,
        icp: Dict[str, Any],
        pain_reviews: List[Dict],
        success_reviews: List[Dict],
        analysis: Dict,
        app_name: str,
        reddit_data: Optional[List[Dict]] = None,
    ) -> Dict[str, Any]:
        """Stage 2: Populate 7-Node System Dynamics Map. I2: Reddit evidence fused with App Store quotes."""
        evidence = self._curate_evidence(pain_reviews, success_reviews, max_quotes=15)
        reddit_evidence = self._curate_reddit_evidence(reddit_data or [], max_quotes=10)
        icp_json = json.dumps(icp, indent=2)
        metrics = analysis.get("metrics", {}) or {}

        user_prompt = f"""ICP (from Stage 1):
{icp_json}

CURATED EVIDENCE QUOTES (App Store reviews):
{chr(10).join(evidence) if evidence else "(none)"}

REDDIT EVIDENCE QUOTES:
{chr(10).join(reddit_evidence) if reddit_evidence else "(none)"}

METRICS: risk_score={metrics.get('risk_score')}, negative_ratio={metrics.get('negative_ratio')}

Produce the 7-Node System Dynamics Map JSON for app "{app_name}". Ensure uds_ud and ubs_ud reach Layer 5 (Biology). Cite evidence from reviews or Reddit where applicable."""

        system_prompt = SYSTEM_DYNAMICS_PROMPT.replace("{app_name}", app_name)
        data = self.ai_client.generate_structured(
            system_prompt=system_prompt,
            user_prompt=user_prompt,
            response_model=None,
        )
        data = self._repair_system_map_response(data)
        result = SystemDynamicsMap.model_validate(data).model_dump()

        # Depth validation
        uds_ud = result.get("uds_ud", {}) or {}
        ubs_ud = result.get("ubs_ud", {}) or {}
        layer_5_markers = ("layer 5", "biology", "layer5")
        for node_name, node in [("uds_ud", uds_ud), ("ubs_ud", ubs_ud)]:
            layer = (node.get("layer") or "").lower()
            if not any(m in layer for m in layer_5_markers):
                logger.warning(
                    "Depth validation: %s did not reach Layer 5 (Biology). layer=%s",
                    node_name, node.get("layer"),
                )
        return result

    def generate_eps_prescription(
        self,
        system_map: Dict[str, Any],
        icp: Dict[str, Any],
        app_name: str,
    ) -> Dict[str, Any]:
        """Stage 3: Derive EPS (Principles, Environment, Tools, SOP) from System Map."""
        icp_json = json.dumps(icp, indent=2)
        sys_json = json.dumps(system_map, indent=2)

        user_prompt = f"""ICP:
{icp_json}

SYSTEM DYNAMICS MAP:
{sys_json}

Produce the EPS Prescription JSON for app "{app_name}". Include at least 4 principles mapping to uds_ud, uds_ub, ubs_ud, ubs_ub."""

        system_prompt = EPS_SYSTEM_PROMPT.replace("{app_name}", app_name)
        data = self.ai_client.generate_structured(
            system_prompt=system_prompt,
            user_prompt=user_prompt,
            response_model=None,
        )
        data = self._repair_eps_response(data)
        result = EPSPrescription.model_validate(data).model_dump()

        if len(result.get("principles", [])) < 4:
            logger.warning("Inversion validation: EPS has fewer than 4 principles.")
        return result

    def generate_blueprint(
        self,
        app_name: str,
        raw_reviews: List[Dict],
        filtered_reviews: List[Dict],
        analysis: Dict,
        reddit_data: List[Dict],
        output_dir: Path,
        niche_name: str = "",
    ) -> Tuple[Path, Path]:
        """
        Orchestrate 3 stages and save artifacts.

        Returns:
            (blueprint_path, system_map_json_path)
        """
        pain_reviews = self._extract_pain_reviews(filtered_reviews)
        success_reviews = self._extract_success_reviews(raw_reviews)

        logger.info(
            "Venture Architect: %d pain, %d success (5★ whales)",
            len(pain_reviews), len(success_reviews),
        )
        if not reddit_data:
            logger.warning("No Reddit data — running Architect on App Store signals only.")

        # Stage 1
        try:
            icp = self.construct_holographic_icp(
                pain_reviews, success_reviews, reddit_data, analysis, app_name,
            )
        except Exception as e:
            logger.error("[%s] Stage 1 (ICP) failed: %s", app_name, e)
            icp = self._empty_icp()

        # Stage 2 (I2: pass Reddit evidence into System Map)
        try:
            system_map = self.map_system_dynamics(
                icp, pain_reviews, success_reviews, analysis, app_name,
                reddit_data=reddit_data,
            )
        except Exception as e:
            logger.error("[%s] Stage 2 (System Map) failed: %s", app_name, e)
            system_map = self._empty_system_map()

        # Stage 3
        try:
            eps = self.generate_eps_prescription(system_map, icp, app_name)
        except Exception as e:
            logger.error("[%s] Stage 3 (EPS) failed: %s", app_name, e)
            eps = self._empty_eps()

        # Save JSON
        app_safe = app_name.replace(" ", "_").lower()
        system_map_file = output_dir / f"{app_safe}_system_map.json"
        payload = {
            "app_name": app_name,
            "generated_at": datetime.utcnow().isoformat(timespec="seconds") + "Z",
            "icp": icp,
            "system_dynamics": system_map,
            "eps_prescription": eps,
        }
        with open(system_map_file, "w", encoding="utf-8") as f:
            json.dump(payload, f, indent=2, ensure_ascii=False)

        # T-027: Render blueprint via Reporter + Jinja2 template
        reporter = self.reporter or Reporter(output_dir=output_dir)
        blueprint_path = reporter.render_venture_blueprint(
            app_name=app_name,
            icp=icp,
            system_map=system_map,
            eps=eps,
            output_dir=output_dir,
            niche_name=niche_name,
        )

        return blueprint_path, system_map_file
