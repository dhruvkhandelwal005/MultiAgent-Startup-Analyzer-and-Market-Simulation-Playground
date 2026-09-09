from fastapi import APIRouter

from app.mcp_server.queries import get_population_segments, get_competitors

router = APIRouter()


@router.get("/simulations/{simulation_id}/population")
async def get_population(simulation_id: int):
    return await get_population_segments(simulation_id)


@router.get("/simulations/{simulation_id}/competitors")
async def get_market_competitors(simulation_id: int):
    return await get_competitors(simulation_id)