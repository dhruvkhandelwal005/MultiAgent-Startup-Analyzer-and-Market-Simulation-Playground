"""
Raw data-access functions for MCP tools.
These query Postgres directly (asyncpg) - no LLM logic here.
"""

from app.db import get_connection


async def get_simulation_state(simulation_id: int) -> dict:
    conn = await get_connection()
    row = await conn.fetchrow(
        "SELECT id, name, initial_budget, current_budget, status FROM simulations WHERE id = $1",
        simulation_id,
    )
    await conn.close()
    return dict(row) if row else {}


async def get_product_info(simulation_id: int) -> dict:
    conn = await get_connection()
    row = await conn.fetchrow(
        "SELECT id, name, description, features, pricing, quality_score, target_segments FROM products WHERE simulation_id = $1",
        simulation_id,
    )
    await conn.close()
    return dict(row) if row else {}


async def get_population_segments(simulation_id: int) -> list[dict]:
    conn = await get_connection()
    rows = await conn.fetch(
        "SELECT id, segment_type, population_size, product_relevance, purchasing_power, awareness, adoption_rate, active_users FROM population_groups WHERE simulation_id = $1",
        simulation_id,
    )
    await conn.close()
    return [dict(r) for r in rows]


async def get_competitors(simulation_id: int) -> list[dict]:
    conn = await get_connection()
    rows = await conn.fetch(
        "SELECT id, name, product_quality, price, marketing_strength, market_share FROM competitors WHERE simulation_id = $1",
        simulation_id,
    )
    await conn.close()
    return [dict(r) for r in rows]


async def get_latest_metrics(simulation_id: int) -> dict:
    conn = await get_connection()
    row = await conn.fetchrow(
        "SELECT * FROM metrics_snapshots WHERE simulation_id = $1 ORDER BY created_at DESC LIMIT 1",
        simulation_id,
    )
    await conn.close()
    return dict(row) if row else {}


async def get_previous_decisions(simulation_id: int, limit: int = 5) -> list[dict]:
    conn = await get_connection()
    rows = await conn.fetch(
        "SELECT action, reason, estimated_cost, status, created_at FROM agent_decisions WHERE simulation_id = $1 ORDER BY created_at DESC LIMIT $2",
        simulation_id,
        limit,
    )
    await conn.close()
    return [dict(r) for r in rows]