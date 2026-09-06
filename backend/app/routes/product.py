from fastapi import APIRouter, HTTPException

from app.mcp_server.queries import get_product_info

router = APIRouter()


@router.get("/simulations/{simulation_id}/product")
async def get_product(simulation_id: int):
    product = await get_product_info(simulation_id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return product