"""
Simulation engine orchestrator.
Reads current state from Postgres, runs Phase 3 deterministic simulation
functions, writes a new metrics_snapshots row, and updates the simulation's
budget. AI agents never write these numbers directly - only this engine does.
"""

from app.db import get_connection
from app.simulation.adoption import calculate_adoption
from app.simulation.finance import calculate_revenue, calculate_expenses, calculate_cash_remaining
from app.simulation.market import calculate_competitive_pressure, apply_competitive_pressure_to_adoption
from app.simulation.churn import calculate_churn

BASE_BURN = 50000.0


async def run_simulation_tick(simulation_id: int, decision_cost: float = 0.0) -> dict:
    conn = await get_connection()

    simulation = await conn.fetchrow(
        "SELECT current_budget FROM simulations WHERE id = $1", simulation_id
    )
    product = await conn.fetchrow(
        "SELECT pricing, quality_score FROM products WHERE simulation_id = $1", simulation_id
    )
    segments = await conn.fetch(
        "SELECT id, population_size, product_relevance, purchasing_power, awareness FROM population_groups WHERE simulation_id = $1",
        simulation_id,
    )
    competitors = await conn.fetch(
        "SELECT product_quality, price, marketing_strength FROM competitors WHERE simulation_id = $1",
        simulation_id,
    )

    if not simulation or not product:
        await conn.close()
        return {}

    price = float(product["pricing"])
    quality = float(product["quality_score"])

    if competitors:
        pressures = [
            calculate_competitive_pressure(
                our_quality=quality,
                our_price=price,
                competitor_quality=float(c["product_quality"]),
                competitor_price=float(c["price"]),
                competitor_marketing_strength=float(c["marketing_strength"]),
            )
            for c in competitors
        ]
        avg_pressure = sum(pressures) / len(pressures)
    else:
        avg_pressure = 0.0

    total_population = 0
    total_active_users = 0

    for seg in segments:
        total_population += seg["population_size"]

        adoption = calculate_adoption(
            population_size=seg["population_size"],
            product_relevance=float(seg["product_relevance"]),
            purchasing_power=float(seg["purchasing_power"]),
            awareness=float(seg["awareness"]),
            product_quality=quality,
        )
        potential = adoption["potential_users"]
        base_active = adoption["active_users"]
        base_fraction = (base_active / potential) if potential > 0 else 0.0

        adjusted_fraction = apply_competitive_pressure_to_adoption(base_fraction, avg_pressure)
        adjusted_active = int(potential * adjusted_fraction)

        churned = calculate_churn(
            active_users=adjusted_active,
            product_quality=quality,
            competitive_pressure=avg_pressure,
        )
        new_active = max(0, adjusted_active - churned)

        await conn.execute(
            "UPDATE population_groups SET active_users = $1, adoption_rate = $2, updated_at = now() WHERE id = $3",
            new_active,
            round((new_active / seg["population_size"]) * 100, 2) if seg["population_size"] else 0,
            seg["id"],
        )

        total_active_users += new_active

    revenue = calculate_revenue(total_active_users, price)
    expenses = calculate_expenses(
        base_burn=BASE_BURN,
        marketing_spend=0.0,
        development_spend=decision_cost,
    )
    current_cash = float(simulation["current_budget"])
    cash_remaining = calculate_cash_remaining(current_cash, revenue, expenses)

    market_share = round((total_active_users / total_population) * 100, 2) if total_population else 0.0

    await conn.execute(
        "UPDATE simulations SET current_budget = $1, updated_at = now() WHERE id = $2",
        cash_remaining,
        simulation_id,
    )

    await conn.execute(
        """INSERT INTO metrics_snapshots
           (simulation_id, total_population, active_users, revenue, expenses, cash_remaining, market_share)
           VALUES ($1, $2, $3, $4, $5, $6, $7)""",
        simulation_id, total_population, total_active_users, revenue, expenses, cash_remaining, market_share,
    )

    await conn.close()

    return {
        "total_population": total_population,
        "active_users": total_active_users,
        "revenue": revenue,
        "expenses": expenses,
        "cash_remaining": cash_remaining,
        "market_share": market_share,
    }