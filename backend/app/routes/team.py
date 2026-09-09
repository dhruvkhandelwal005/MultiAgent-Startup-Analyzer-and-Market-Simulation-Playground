from fastapi import APIRouter
from pydantic import BaseModel

from app.db import get_connection

router = APIRouter()


class TeamRequest(BaseModel):
    agent_roles: list[str]


@router.post("/simulations/{simulation_id}/team")
async def save_team(simulation_id: int, request: TeamRequest):
    conn = await get_connection()
    await conn.execute("DELETE FROM teams WHERE simulation_id = $1", simulation_id)
    for role in request.agent_roles:
        agent = await conn.fetchrow("SELECT id FROM agents WHERE role = $1", role)
        if agent:
            await conn.execute(
                "INSERT INTO teams (simulation_id, agent_id) VALUES ($1, $2)",
                simulation_id,
                agent["id"],
            )
    await conn.close()
    return {"agent_roles": request.agent_roles}


@router.get("/simulations/{simulation_id}/team")
async def get_team(simulation_id: int):
    conn = await get_connection()
    rows = await conn.fetch(
        """SELECT a.role FROM teams t
           JOIN agents a ON a.id = t.agent_id
           WHERE t.simulation_id = $1""",
        simulation_id,
    )
    await conn.close()
    return {"agent_roles": [r["role"] for r in rows]}