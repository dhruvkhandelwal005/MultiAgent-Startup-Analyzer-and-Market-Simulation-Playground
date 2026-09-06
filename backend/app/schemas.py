from pydantic import BaseModel, Field
from typing import Optional


class AgentDecision(BaseModel):
    agent_role: str
    action: str
    reason: str
    confidence: float = Field(ge=0, le=100)
    estimated_cost: float = 0
    expected_impact: str
    requires_approval: bool = False


class ProductChange(BaseModel):
    feature: str
    description: str
    development_cost: float
    development_time_days: int
    expected_impact: str


class MarketingDecision(BaseModel):
    campaign_name: str
    target_segment: str
    budget: float
    expected_reach: int
    expected_conversion: float = Field(ge=0, le=100)