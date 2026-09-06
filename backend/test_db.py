import asyncio
from app.db import get_connection

async def main():
    conn = await get_connection()
    version = await conn.fetchval("SELECT version();")
    print("Connected! Postgres version:", version)
    await conn.close()

asyncio.run(main())