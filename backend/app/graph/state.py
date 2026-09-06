from typing import TypedDict, Optional


class SimulationState(TypedDict, total=False):
    simulation_id: int
    current_event: str
    finance_analysis: Optional[dict]
    product_analysis: Optional[dict]
    developer_analysis: Optional[dict]
    marketing_analysis: Optional[dict]
    ceo_decision: Optional[dict]
    requires_approval: bool