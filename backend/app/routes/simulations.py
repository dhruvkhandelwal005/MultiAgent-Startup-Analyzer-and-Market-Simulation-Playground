from fastapi import APIRouter
from pydantic import BaseModel

from app.graph.workflow import build_graph

router = APIRouter()


class EventRequest(BaseModel):
    event_type: str = "general"
    current_event: str


@router.post("/simulations/{simulation_id}/events")
async def trigger_event(simulation_id: int, request: EventRequest):
    graph = build_graph()
    state = {
        "simulation_id": simulation_id,
        "event_type": request.event_type,
        "current_event": request.current_event,
    }
    result = await graph.ainvoke(state)
    return {
        "ceo_decision": result.get("ceo_decision"),
        "requires_approval": result.get("requires_approval"),
    }