import asyncio
import json
from app.db import get_connection

async def main():
    conn = await get_connection()

    sim = await conn.fetchrow(
        "INSERT INTO simulations (name, initial_budget, current_budget, status) VALUES ($1, $2, $3, $4) RETURNING id",
        "AI Study Assistant Sim", 1000000, 850000, "active"
    )
    sim_id = sim["id"]

    await conn.execute(
        "INSERT INTO products (simulation_id, name, description, features, pricing, quality_score, target_segments) VALUES ($1,$2,$3,$4,$5,$6,$7)",
        sim_id, "AI Study Assistant", "Personalized learning platform",
        json.dumps(["Study plans", "Question generation", "Progress tracking"]),
        199, 70, json.dumps(["Students", "Tech Workers"])
    )

    await conn.execute(
        "INSERT INTO population_groups (simulation_id, segment_type, population_size, product_relevance, purchasing_power, awareness, adoption_rate, active_users) VALUES ($1,$2,$3,$4,$5,$6,$7,$8)",
        sim_id, "Students", 10000, 80, 60, 40, 15, 1200
    )

    await conn.execute(
        "INSERT INTO competitors (simulation_id, name, product_quality, price, marketing_strength, market_share) VALUES ($1,$2,$3,$4,$5,$6)",
        sim_id, "Competitor A", 75, 180, 60, 20
    )

    await conn.execute(
        "INSERT INTO metrics_snapshots (simulation_id, total_population, active_users, revenue, expenses, cash_remaining, market_share) VALUES ($1,$2,$3,$4,$5,$6,$7)",
        sim_id, 10000, 1200, 238800, 70000, 850000, 65.5
    )

    print(f"Seeded simulation_id = {sim_id}")
    await conn.close()

asyncio.run(main())