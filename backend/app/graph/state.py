from typing import TypedDict, Optional


class SimulationState(TypedDict, total=False):
    simulation_id: int
    event_type: str  # "competitor_entry" | "revenue_drop" | "adoption_drop" | "general"
    current_event: str
    history_text: str
    finance_analysis: Optional[dict]
    product_analysis: Optional[dict]
    developer_analysis: Optional[dict]
    marketing_analysis: Optional[dict]
    ceo_decision: Optional[dict]
    requires_approval: bool
    request_id: Optional[int]