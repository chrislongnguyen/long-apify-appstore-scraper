"""
Pydantic schemas for Venture Architect (Phase 7) structured LLM output.

T-025: Strict validation to fail loud on invalid JSON. Every node must cite evidence.
"""
from typing import Any, Dict, List, Optional

from pydantic import BaseModel, Field


# --- Stage 1: Holographic ICP ---

class ICPSegment(BaseModel):
    """Primary, secondary, and whale segments of the ICP."""
    primary: str = Field(description="Primary target segment")
    secondary: str = Field(description="Secondary segment")
    whale_segment: str = Field(description="High-LTV whale segment")


class PainSuccessParadox(BaseModel):
    """The tension between what pain says vs what success says."""
    pain_says: str = Field(description="What 1-2★ reviews complain about")
    success_says: str = Field(description="What 5★ whales love")
    inference: str = Field(description="Inferred reconciliation or split segment")


class UserPersona(BaseModel):
    """I4: One of 3 non-overlapping user personas with a 5-6 sentence user story."""
    persona_name: str = Field(description="Short name for the persona")
    archetype: str = Field(description="Archetype label, e.g. The Reluctant Quitter")
    user_story: str = Field(description="5-6 sentence journey: User → UDO → UDS/UBS → UDS.UB/UBS.UB")
    segment: str = Field(description="primary, secondary, or whale_segment")


class HolographicICP(BaseModel):
    """Stage 1 output: Holographic Ideal Customer Profile."""
    who: Dict[str, Any] = Field(description="Demographic and psychographic profile")
    why_udo: str = Field(description="Ultimate Desired Outcome")
    what_how_workflow: List[str] = Field(description="What/how workflow steps")
    when_trigger: str = Field(description="When/trigger context")
    alternatives: List[str] = Field(description="Competitors, workarounds, alternatives mentioned")
    icp_segment: ICPSegment = Field(description="Segment breakdown")
    pain_success_paradox: PainSuccessParadox = Field(description="Pain vs success tension")
    user_personas: List[UserPersona] = Field(
        default_factory=list,
        description="I4: 3 non-overlapping personas with user stories (5-6 sentences each)",
    )


# --- Stage 2: 7-Node System Dynamics Map ---

class SystemNode(BaseModel):
    """A node in the 7-Node System Dynamics Map."""
    label: str = Field(description="Short label for the node")
    evidence: List[str] = Field(description="Quotes from reviews supporting this node")
    layer: str = Field(description="Depth layer: Layer 1-5 (App, Behavior, System, Psychology, Biology)")
    note: Optional[str] = Field(default=None, description="Optional clarification")


class UDO(BaseModel):
    """Ultimate Desired Outcome (adverb + noun)."""
    statement: str = Field(description="Full UDO statement")
    adverb: str = Field(description="The adverb (how they want to achieve)")
    noun: str = Field(description="The noun (what they want)")


class SystemDynamicsMap(BaseModel):
    """Stage 2 output: 7-Node System Dynamics Map."""
    udo: UDO = Field(description="Ultimate Desired Outcome")
    uds: SystemNode = Field(description="Ultimate Driving System")
    uds_ud: SystemNode = Field(description="Root Driver of UDS (Layer 5)")
    uds_ub: SystemNode = Field(description="Root Blocker of UDS")
    ubs: SystemNode = Field(description="Ultimate Blocking System")
    ubs_ud: SystemNode = Field(description="Root Driver of UBS (Layer 5)")
    ubs_ub: SystemNode = Field(description="Root Blocker of UBS")
    incumbent_failure: str = Field(description="Which layer the incumbent addresses vs ignores")
    depth_layers: Dict[str, Any] = Field(description="Layer 1-5 breakdown by domain")


# --- Stage 3: EPS Prescription ---

class Principle(BaseModel):
    """A strategic principle derived from a system node."""
    id: str = Field(description="Unique identifier")
    name: str = Field(description="Principle name")
    strategy: str = Field(description="e.g. Amplify UDS.UD")
    node_ref: str = Field(description="e.g. uds_ud")
    rationale: str = Field(description="Why this principle")


class EPSPrescription(BaseModel):
    """Stage 3 output: EPS (Environment, Principles, SOP & Tools)."""
    principles: List[Principle] = Field(description="4+ principles mapping to nodes")
    environment: Dict[str, Any] = Field(description="form_factor, rationale, anti_pattern")
    tools: Dict[str, Any] = Field(description="desirable_wrapper, effective_core")
    sop: List[Dict[str, Any]] = Field(description="[{step, actor, action}]")
    trojan_horse: Dict[str, Any] = Field(description="level_1_desirable, level_5_effective")
    strategic_inversion_table: List[Dict[str, Any]] = Field(
        description="[Incumbent Method] -> [Root Cause Node] -> [New Principle]"
    )
