from app.db import get_connection


async def create_pending_approval(decision_id: int) -> int:
    conn = await get_connection()
    try:
        row = await conn.fetchrow(
            "INSERT INTO human_approvals (decision_id, status) VALUES ($1, 'pending') RETURNING id",
            decision_id,
        )
    finally:
        await conn.close()
    return row["id"]


async def respond_to_approval(approval_id: int, approve: bool) -> dict:
    status = "approved" if approve else "rejected"
    conn = await get_connection()
    try:
        row = await conn.fetchrow(
            "UPDATE human_approvals SET status = $1, responded_at = now() WHERE id = $2 RETURNING id, decision_id, status",
            status,
            approval_id,
        )
        if row:
            await conn.execute(
                "UPDATE agent_decisions SET status = $1 WHERE id = $2",
                status,
                row["decision_id"],
            )
    finally:
        await conn.close()
    return dict(row) if row else {}


async def get_pending_approvals(simulation_id: int) -> list[dict]:
    conn = await get_connection()
    try:
        rows = await conn.fetch(
            """
            SELECT ha.id AS approval_id, ha.decision_id, ad.action, ad.reason, ad.estimated_cost
            FROM human_approvals ha
            JOIN agent_decisions ad ON ad.id = ha.decision_id
            WHERE ha.status = 'pending' AND ad.simulation_id = $1
            """,
            simulation_id,
        )
    finally:
        await conn.close()
    return [dict(r) for r in rows]