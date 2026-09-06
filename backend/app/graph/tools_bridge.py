"""
Bridge between LangGraph nodes and MCP tools.
Calls the MCP server and returns parsed data for use in agent context building.
"""

import json
from pathlib import Path
from fastmcp import Client

SERVER_PATH = Path(__file__).parent.parent / "mcp_server" / "server.py"


async def fetch_simulation_context(simulation_id: int) -> dict:
    """
    Calls all relevant MCP tools and returns combined simulation context.
    """
    client = Client(SERVER_PATH)

    async with client:
        product = await client.call_tool("get_product_info_tool", {"simulation_id": simulation_id})
        population = await client.call_tool("get_population_segments_tool", {"simulation_id": simulation_id})
        competitors = await client.call_tool("get_competitors_tool", {"simulation_id": simulation_id})
        metrics = await client.call_tool("get_latest_metrics_tool", {"simulation_id": simulation_id})
        simulation = await client.call_tool("get_simulation_state_tool", {"simulation_id": simulation_id})

    return {
        "simulation": json.loads(simulation.content[0].text),
        "product": json.loads(product.content[0].text),
        "population": json.loads(population.content[0].text),
        "competitors": json.loads(competitors.content[0].text),
        "metrics": json.loads(metrics.content[0].text),
    }


def format_context_as_text(context: dict, event_description: str) -> str:
    """
    Converts the fetched context dict into a readable text block for agent prompts.
    """
    return f"""
Current Event: {event_description}

Simulation: {context['simulation']}

Product: {context['product']}

Population Segments: {context['population']}

Competitors: {context['competitors']}

Latest Metrics: {context['metrics']}
"""