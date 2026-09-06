import asyncio
import sys
from app.db import get_connection

async def main(filepath):
    conn = await get_connection()
    with open(filepath, "r") as f:
        sql = f.read()
    await conn.execute(sql)
    print(f"Executed: {filepath}")
    await conn.close()

if __name__ == "__main__":
    asyncio.run(main(sys.argv[1]))