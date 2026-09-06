"""
Persistent memory: save decisions to Postgres, retrieve history for context.
"""

from app.db import get_connection


async def save_decision(
    simulation_id: int,
    agent_role: str,
    action: str,
    reason: str,
    estimated_cost: float,
    requires_approval: bool,
) -> int:
    conn = await get_connection()
    agent = await conn.fetchrow("SELECT id FROM agents WHERE role = $1", agent_role)
    agent_id = agent["id"] if agent else None

    row = await conn.fetchrow(
        """INSERT INTO agent_decisions
           (simulation_id, agent_id, action, reason, estimated_cost, requires_approval, status)
           VALUES ($1, $2, $3, $4, $5, $6, $7) RETURNING id""",
        simulation_id, agent_id, action, reason, estimated_cost, requires_approval, "proposed"
    )
    await conn.close()
    return row["id"]


async def get_recent_history_text(simulation_id: int, limit: int = 3) -> str:
    conn = await get_connection()
    rows = await conn.fetch(
        "SELECT action, reason, status, created_at FROM agent_decisions WHERE simulation_id = $1 ORDER BY created_at DESC LIMIT $2",
        simulation_id, limit
    )
    await conn.close()

    if not rows:
        return "No previous decisions."

    lines = [f"- {r['action']} (status: {r['status']}, reason: {r['reason'][:100]})" for r in rows]
    return "Previous decisions:\n" + "\n".join(lines)