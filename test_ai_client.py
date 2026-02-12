#!/usr/bin/env python3
"""T-025: Unit tests for AIClient and Pydantic schemas."""
import sys
from pathlib import Path
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).parent / "src"))

from src.ai_client import AIClient
from src.schemas import HolographicICP, ICPSegment, PainSuccessParadox, SystemDynamicsMap


# Mock ICP response (Stage 1 schema)
MOCK_ICP_JSON = """{
  "who": {"demographic": "health-conscious adults", "psychographic": "goal-oriented"},
  "why_udo": "Effortless metabolic control without daily decision fatigue",
  "what_how_workflow": ["Start fast", "Log meals", "Track streaks"],
  "when_trigger": "New Year resolution, doctor visit, wedding",
  "alternatives": ["Zero", "Lose It", "Pen and paper"],
  "icp_segment": {
    "primary": "Intermittent fasters",
    "secondary": "Calorie trackers",
    "whale_segment": "Pro users who write long reviews"
  },
  "pain_success_paradox": {
    "pain_says": "Too complex, crashes",
    "success_says": "Love the depth, streak keeps me going",
    "inference": "Split: whales value complexity, casual users want simplicity"
  }
}"""


def test_parse_json_response_raw():
    """Test _parse_json_response handles raw JSON."""
    client = AIClient(provider="gemini", api_key="test-key-for-mock")
    result = client._parse_json_response(MOCK_ICP_JSON)
    assert "who" in result
    assert result["why_udo"] == "Effortless metabolic control without daily decision fatigue"
    assert result["icp_segment"]["primary"] == "Intermittent fasters"
    print("✓ PASS: _parse_json_response parses raw JSON")


def test_parse_json_response_with_fences():
    """Test _parse_json_response strips markdown code fences."""
    client = AIClient(provider="gemini", api_key="test-key-for-mock")
    fenced = "```json\n" + MOCK_ICP_JSON + "\n```"
    result = client._parse_json_response(fenced)
    assert "who" in result
    assert "alternatives" in result
    print("✓ PASS: _parse_json_response strips ```json fences")


def test_generate_structured_mock_pydantic_validation():
    """Test generate_structured with mock LLM returns Pydantic-validated dict."""
    with patch.object(AIClient, "_generate_raw", return_value=MOCK_ICP_JSON):
        client = AIClient(provider="gemini", api_key="test-key-for-mock")
        result = client.generate_structured(
            system_prompt="You are a cultural anthropologist.",
            user_prompt="Analyze these reviews.",
            response_model=HolographicICP,
        )
    assert isinstance(result, dict)
    assert result["why_udo"] == "Effortless metabolic control without daily decision fatigue"
    assert result["icp_segment"]["whale_segment"] == "Pro users who write long reviews"
    assert "pain_success_paradox" in result
    print("✓ PASS: generate_structured returns Pydantic-validated dict")


def test_pydantic_icp_schema():
    """Test HolographicICP schema validates mock data."""
    import json
    data = json.loads(MOCK_ICP_JSON)
    validated = HolographicICP.model_validate(data)
    assert validated.icp_segment.primary == "Intermittent fasters"
    assert validated.pain_success_paradox.inference.startswith("Split")
    print("✓ PASS: HolographicICP Pydantic validation")


def test_pydantic_raises_on_invalid():
    """Test that invalid JSON raises ValidationError."""
    from pydantic import ValidationError
    try:
        HolographicICP.model_validate({"who": "string"})  # Missing required fields
        assert False, "Should have raised ValidationError"
    except ValidationError:
        pass
    print("✓ PASS: HolographicICP raises on invalid data")


if __name__ == "__main__":
    # Run without pytest (simple assertion runner)
    test_parse_json_response_raw()
    test_parse_json_response_with_fences()
    test_pydantic_icp_schema()
    test_pydantic_raises_on_invalid()
    test_generate_structured_mock_pydantic_validation()
    print("\n✓ All T-025 ai_client tests passed")
