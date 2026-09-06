"""
MCP Server exposing simulation data as tools for agents.
Built with FastMCP (decorator-based, works with MCP SDK v2).
"""

import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))

from fastmcp import FastMCP
import json

from app.mcp_server.queries import (
    get_simulation_state,
    get_product_info,
    get_population_segments,
    get_competitors,
    get_latest_metrics,
    get_previous_decisions,
)

mcp = FastMCP("market-sim-tools")


@mcp.tool
async def get_simulation_state_tool(simulation_id: int) -> str:
    """Get current simulation status and budget."""
    result = await get_simulation_state(simulation_id)
    return json.dumps(result, default=str)


@mcp.tool
async def get_product_info_tool(simulation_id: int) -> str:
    """Get current product details: features, pricing, quality, target segments."""
    result = await get_product_info(simulation_id)
    return json.dumps(result, default=str)


@mcp.tool
async def get_population_segments_tool(simulation_id: int) -> str:
    """Get all population segments in the market with their properties."""
    result = await get_population_segments(simulation_id)
    return json.dumps(result, default=str)


@mcp.tool
async def get_competitors_tool(simulation_id: int) -> str:
    """Get all competitors currently in the market."""
    result = await get_competitors(simulation_id)
    return json.dumps(result, default=str)


@mcp.tool
async def get_latest_metrics_tool(simulation_id: int) -> str:
    """Get the most recent simulation metrics snapshot."""
    result = await get_latest_metrics(simulation_id)
    return json.dumps(result, default=str)


@mcp.tool
async def get_previous_decisions_tool(simulation_id: int, limit: int = 5) -> str:
    """Get recent past agent decisions for historical context."""
    result = await get_previous_decisions(simulation_id, limit)
    return json.dumps(result, default=str)


if __name__ == "__main__":
    mcp.run()