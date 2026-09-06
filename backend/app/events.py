import asyncio
from typing import Optional

_queues: dict[int, asyncio.Queue] = {}


def create_queue(request_id: int) -> asyncio.Queue:
    q = asyncio.Queue()
    _queues[request_id] = q
    return q


def get_queue(request_id: int) -> Optional[asyncio.Queue]:
    return _queues.get(request_id)


def remove_queue(request_id: int):
    _queues.pop(request_id, None)


async def publish(request_id: int, message: dict):
    q = _queues.get(request_id)
    if q:
        await q.put(message)