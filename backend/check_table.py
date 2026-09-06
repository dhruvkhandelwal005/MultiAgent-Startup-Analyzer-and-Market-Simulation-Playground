import asyncio
from app.db import get_connection


async def main():
    conn = await get_connection()
    rows = await conn.fetch(
        "SELECT column_name, data_type FROM information_schema.columns WHERE table_name='human_approvals'"
    )
    for r in rows:
        print(dict(r))
    await conn.close()


asyncio.run(main())