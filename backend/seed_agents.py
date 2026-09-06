import asyncio
from app.db import get_connection

AGENTS = [
    ("Alex", "ceo", "CEO - overall strategy and final decisions"),
    ("Mark", "finance", "Finance - budget, revenue, risk analysis"),
    ("Sam", "product", "Product - features, product-market fit"),
    ("Denny", "developer", "Developer - technical feasibility, cost/time estimates"),
    ("Mia", "marketing", "Marketing - campaigns, acquisition, segments"),
]

async def main():
    conn = await get_connection()
    for name, role, desc in AGENTS:
        existing = await conn.fetchrow("SELECT id FROM agents WHERE role = $1", role)
        if not existing:
            await conn.execute(
                "INSERT INTO agents (name, role, description) VALUES ($1, $2, $3)",
                name, role, desc
            )
            print(f"Inserted {name} ({role})")
        else:
            print(f"{name} ({role}) already exists")
    await conn.close()

asyncio.run(main())