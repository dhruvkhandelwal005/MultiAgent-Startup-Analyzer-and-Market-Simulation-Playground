import asyncio
from app.guardrails import check_budget_constraint


async def main():
    result = await check_budget_constraint(simulation_id=1, estimated_cost=1000)
    print(result)

    result2 = await check_budget_constraint(simulation_id=1, estimated_cost=999999999)
    print(result2)


asyncio.run(main())