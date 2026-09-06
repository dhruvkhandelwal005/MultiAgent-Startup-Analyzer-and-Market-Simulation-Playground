from fastapi import APIRouter, HTTPException

from app.mcp_server.queries import get_latest_metrics

router = APIRouter()


@router.get("/simulations/{simulation_id}/metrics")
async def get_metrics(simulation_id: int):
    metrics = await get_latest_metrics(simulation_id)
    if not metrics:
        raise HTTPException(status_code=404, detail="No metrics found")
    return metrics