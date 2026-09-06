import asyncio
from app.graph.workflow import build_graph


async def main():
    graph = build_graph()
    state = {
        "simulation_id": 1,
        "event_type": "general",
        "current_event": "New competitor entered with strong marketing.",
    }
    result = await graph.ainvoke(state)
    print("---")
    print(result["ceo_decision"]["action"])


asyncio.run(main())