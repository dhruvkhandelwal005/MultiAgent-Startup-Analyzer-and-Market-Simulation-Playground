import asyncio
from unittest.mock import patch
from app.graph.state import SimulationState
from app.schemas import AgentDecision


async def main():
    fake_decision = AgentDecision(
        agent_role="ceo",
        action="Spend big",
        reason="test",
        confidence=90,
        estimated_cost=999999999,
        expected_impact="test",
        requires_approval=False,
    )

    with patch("app.graph.workflow.run_ceo_decision", return_value=fake_decision):
        from app.graph.workflow import ceo_node
        state: SimulationState = {
            "simulation_id": 1,
            "current_event": "test event",
            "finance_analysis": {},
            "product_analysis": {},
            "developer_analysis": {},
            "marketing_analysis": {},
            "history_text": "",
        }
        result = await ceo_node(state)
        print(result["ceo_decision"]["action"])
        print(result["requires_approval"])


asyncio.run(main())