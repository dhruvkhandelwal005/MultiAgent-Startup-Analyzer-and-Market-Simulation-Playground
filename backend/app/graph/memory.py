"""
Persistent memory: save decisions to Postgres, retrieve history for context.
"""
import json
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


async def save_evaluation(
    decision_id: int,
    strategic_score: float,
    financial_score: float,
    risk_score: float,
    overall_score: float,
    feedback: str,
) -> int:
    conn = await get_connection()
    row = await conn.fetchrow(
        """INSERT INTO evaluations
           (decision_id, strategic_score, financial_score, risk_score, overall_score, feedback)
           VALUES ($1, $2, $3, $4, $5, $6) RETURNING id""",
        decision_id, strategic_score, financial_score, risk_score, overall_score, feedback
    )
    await conn.close()
    return row["id"]


async def save_product(simulation_id: int, product) -> int:
    conn = await get_connection()
    existing = await conn.fetchrow(
        "SELECT id FROM products WHERE simulation_id = $1", simulation_id
    )
    if existing:
        row = await conn.fetchrow(
            """UPDATE products SET name=$1, description=$2, features=$3, pricing=$4,
               target_segments=$5, quality_score=$6, updated_at=now()
               WHERE simulation_id=$7 RETURNING id""",
            product.name,
            product.description,
            json.dumps(product.features),
            product.pricing,
            json.dumps(product.target_segments),
            product.quality_score,
            simulation_id,
        )
    else:
        row = await conn.fetchrow(
            """INSERT INTO products
               (simulation_id, name, description, features, pricing, target_segments, quality_score)
               VALUES ($1, $2, $3, $4, $5, $6, $7) RETURNING id""",
            simulation_id,
            product.name,
            product.description,
            json.dumps(product.features),
            product.pricing,
            json.dumps(product.target_segments),
            product.quality_score,
        )
    await conn.close()
    return row["id"]