import asyncio
from app.graph.workflow import build_graph
from app.hitl import get_pending_approvals, respond_to_approval


async def main():
    graph = build_graph()
    state = {
        "simulation_id": 1,
        "event_type": "general",
        "current_event": "Competitor slashed prices by 50%, urgent response needed, large budget request likely.",
    }
    result = await graph.ainvoke(state)
    print("Decision:", result["ceo_decision"]["action"])
    print("Requires approval:", result["requires_approval"])

    pending = await get_pending_approvals(1)
    print("Pending approvals:", pending)

    if pending:
        approval_id = pending[-1]["approval_id"]
        response = await respond_to_approval(approval_id, approve=True)
        print("Response:", response)


asyncio.run(main())