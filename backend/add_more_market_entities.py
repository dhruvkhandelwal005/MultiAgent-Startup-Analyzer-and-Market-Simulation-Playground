import asyncio
from app.db import get_connection


async def main():
    conn = await get_connection()

    population = [
        ("Doctors", 500, 85.0, 90.0, 30.0),
        ("Tech Workers", 3000, 70.0, 75.0, 45.0),
        ("Civilians", 20000, 40.0, 50.0, 20.0),
    ]
    for segment_type, size, relevance, purchasing_power, awareness in population:
        await conn.execute(
            """INSERT INTO population_groups
               (simulation_id, segment_type, population_size, product_relevance, purchasing_power, awareness, adoption_rate, active_users)
               VALUES ($1, $2, $3, $4, $5, $6, 0, 0)""",
            1, segment_type, size, relevance, purchasing_power, awareness,
        )

    competitors = [
        ("Competitor B", 60.0, 150.0, 40.0),
        ("Competitor C", 85.0, 250.0, 70.0),
    ]
    for name, quality, price, marketing_strength in competitors:
        await conn.execute(
            """INSERT INTO competitors
               (simulation_id, name, product_quality, price, marketing_strength, market_share)
               VALUES ($1, $2, $3, $4, $5, 0)""",
            1, name, quality, price, marketing_strength,
        )

    await conn.close()
    print("Added 3 population segments and 2 competitors.")


asyncio.run(main())