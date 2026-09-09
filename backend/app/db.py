import os
import asyncio
import asyncpg
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")


async def get_connection():
    last_error = None
    for attempt in range(3):
        try:
            return await asyncpg.connect(DATABASE_URL, statement_cache_size=0)
        except Exception as e:
            last_error = e
            if attempt < 2:
                await asyncio.sleep(0.5 if attempt == 0 else 1)
    raise last_error