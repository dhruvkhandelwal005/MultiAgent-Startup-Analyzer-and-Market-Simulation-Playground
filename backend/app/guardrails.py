from app.db import get_connection


async def check_budget_constraint(simulation_id: int, estimated_cost: float) -> dict:
    conn = await get_connection()
    try:
        row = await conn.fetchrow(
            "SELECT current_budget FROM simulations WHERE id = $1", simulation_id
        )
    finally:
        await conn.close()

    if row is None:
        return {"passed": False, "reason": f"Simulation {simulation_id} not found."}

    current_budget = row["current_budget"]
    if estimated_cost > current_budget:
        return {
            "passed": False,
            "reason": f"Estimated cost {estimated_cost} exceeds current budget {current_budget}.",
        }
    return {"passed": True, "reason": "Within budget."}