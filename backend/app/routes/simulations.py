import asyncio
import time

from fastapi import APIRouter
from fastapi.responses import StreamingResponse
from pydantic import BaseModel

from app.graph.workflow import build_graph
from app.events import create_queue, remove_queue, publish

router = APIRouter()


class EventRequest(BaseModel):
    event_type: str = "general"
    current_event: str


@router.post("/simulations/{simulation_id}/events")
async def trigger_event(simulation_id: int, request: EventRequest):
    request_id = int(time.time() * 1000)
    graph = build_graph()
    state = {
        "simulation_id": simulation_id,
        "event_type": request.event_type,
        "current_event": request.current_event,
        "request_id": request_id,
    }
    result = await graph.ainvoke(state)
    return {
        "request_id": request_id,
        "ceo_decision": result.get("ceo_decision"),
        "requires_approval": result.get("requires_approval"),
    }


@router.post("/simulations/{simulation_id}/events/stream")
async def trigger_event_stream(simulation_id: int, request: EventRequest):
    request_id = int(time.time() * 1000)
    queue = create_queue(request_id)

    async def run_graph():
        graph = build_graph()
        state = {
            "simulation_id": simulation_id,
            "event_type": request.event_type,
            "current_event": request.current_event,
            "request_id": request_id,
        }
        result = await graph.ainvoke(state)
        await publish(request_id, {"done": True, "result": {
            "ceo_decision": result.get("ceo_decision"),
            "requires_approval": result.get("requires_approval"),
        }})

    async def event_generator():
        task = asyncio.create_task(run_graph())
        try:
            while True:
                message = await queue.get()
                import json
                yield f"data: {json.dumps(message)}\n\n"
                if message.get("done"):
                    break
        finally:
            remove_queue(request_id)
            await task

    return StreamingResponse(event_generator(), media_type="text/event-stream")