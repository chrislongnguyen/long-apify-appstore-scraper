#!/usr/bin/env python3
"""T-026/T-027 tests for VentureArchitect + Blueprint rendering."""
import json
import sys
import tempfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent / "src"))

from src.venture_architect import VentureArchitect


class MockAIClient:
    """Deterministic mock AI client for stage outputs."""

    def generate_structured(self, system_prompt, user_prompt, **kwargs):
        p = system_prompt.lower()
        if "system dynamics map" in p:
            return {
                "udo": {"statement": "Effortlessly Lean", "adverb": "Effortlessly", "noun": "Lean"},
                "uds": {"label": "Longevity desire", "evidence": ["Quote A"], "layer": "Layer 4 (Psychology)"},
                "uds_ud": {"label": "Survival instinct", "evidence": ["Quote B"], "layer": "Layer 5 (Biology)"},
                "uds_ub": {"label": "Decision fatigue", "evidence": ["Quote C"], "layer": "Layer 4 (Psychology)"},
                "ubs": {"label": "Instant gratification", "evidence": ["Quote D"], "layer": "Layer 2 (Behavior)"},
                "ubs_ud": {"label": "Energy conservation", "evidence": ["Quote E"], "layer": "Layer 5 (Biology)"},
                "ubs_ub": {"label": "Acute pain trigger", "evidence": ["Quote F"], "layer": "Layer 4 (Psychology)"},
                "incumbent_failure": "Addresses app layer only.",
                "depth_layers": {
                    "layer_1_app": "UI",
                    "layer_2_behavior": "Habits",
                    "layer_3_system": "Loops",
                    "layer_4_psychology": "Biases",
                    "layer_5_biology": "Hormones",
                },
            }
        if "eps prescription generator" in p:
            return {
                "principles": [
                    {"id": "P1", "name": "Amplify UDS.UD", "strategy": "Amplify", "node_ref": "uds_ud", "rationale": "Drive motivation"},
                    {"id": "P2", "name": "Disable UDS.UB", "strategy": "Disable", "node_ref": "uds_ub", "rationale": "Reduce fatigue"},
                    {"id": "P3", "name": "Starve UBS.UD", "strategy": "Starve", "node_ref": "ubs_ud", "rationale": "Break blocker engine"},
                    {"id": "P4", "name": "Amplify UBS.UB", "strategy": "Amplify", "node_ref": "ubs_ub", "rationale": "Trigger weakness"},
                ],
                "environment": {
                    "form_factor": "Widget",
                    "rationale": "Zero cognitive load",
                    "anti_pattern": "Full manual app",
                },
                "tools": {
                    "desirable_wrapper": {"name": "Timer widget", "hook": "Simple"},
                    "effective_core": {"name": "Behavior engine", "mechanic": "Automatic nudge"},
                },
                "sop": [
                    {"step": 1, "actor": "System", "action": "Monitor"},
                    {"step": 2, "actor": "User", "action": "Acknowledge"},
                ],
                "trojan_horse": {
                    "level_1_desirable": "Beautiful timer",
                    "level_5_effective": "Behavioral conditioning",
                },
                "strategic_inversion_table": [
                    {"incumbent_method": "Manual logging", "root_cause_node": "ubs_ud", "new_principle": "Zero-load"}
                ],
            }
        if "holographic icp" in p:
            return {
                "who": {"demographic": "25-40", "psychographic": "goal-oriented"},
                "why_udo": "Effortless metabolic control",
                "what_how_workflow": ["Open app", "Track progress", "Adjust behavior"],
                "when_trigger": "After meals",
                "alternatives": ["Competitor A", "Spreadsheet"],
                "icp_segment": {
                    "primary": "Casual optimizer",
                    "secondary": "Biohacker",
                    "whale_segment": "Biohacker",
                },
                "pain_success_paradox": {
                    "pain_says": "Too complex",
                    "success_says": "Love depth",
                    "inference": "Split ICP",
                },
            }
        raise AssertionError(f"Unknown stage prompt: {system_prompt[:120]}")


def test_generate_blueprint_outputs():
    """T-026/T-027: end-to-end venture blueprint generation with standardized JSON payload."""
    raw_reviews = [
        {"score": 5, "title": "Great", "text": " ".join(["great"] * 40)},
        {"score": 1, "title": "Bad", "text": "Too many bugs and hidden paywalls"},
    ]
    filtered_reviews = [
        {"score": 1, "title": "Bad", "text": "Too many bugs and hidden paywalls"},
    ]
    analysis = {
        "signals": {"top_pain_categories": [{"category": "critical", "count": 3, "weight": 10}]},
        "metrics": {"risk_score": 72.0, "negative_ratio": 0.4},
    }

    with tempfile.TemporaryDirectory() as tmp:
        output_dir = Path(tmp)
        va = VentureArchitect(ai_client=MockAIClient(), settings={})
        blueprint_path, system_map_path = va.generate_blueprint(
            app_name="Test App",
            raw_reviews=raw_reviews,
            filtered_reviews=filtered_reviews,
            analysis=analysis,
            reddit_data=[],
            output_dir=output_dir,
            niche_name="TestNiche",
        )

        assert blueprint_path.exists(), "Blueprint markdown was not created"
        assert system_map_path.exists(), "System map JSON was not created"

        payload = json.loads(system_map_path.read_text(encoding="utf-8"))
        # Standardized keys (T-026 item 3)
        assert payload["app_name"] == "Test App"
        assert "generated_at" in payload
        assert "icp" in payload
        assert "system_dynamics" in payload
        assert "eps_prescription" in payload
        assert "system_map" not in payload
        assert "eps" not in payload

        md = blueprint_path.read_text(encoding="utf-8")
        assert "# Venture Blueprint: Test App" in md
        assert "## 1. The System Map" in md
        assert "## 4. The Trojan Horse" in md
        assert "Strategic Inversion" in md
    print("✓ PASS: T-026/T-027 blueprint generation and schema standardization")


if __name__ == "__main__":
    test_generate_blueprint_outputs()
    print("\n✓ All venture architect tests passed")
