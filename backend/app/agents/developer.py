from app.llm.gateway import get_llm
from app.schemas import ProductChange

DEVELOPER_SYSTEM_PROMPT = """You are Denny, the Developer agent for a company running a simulated product in a market.
You evaluate technical feasibility, development effort, and estimate cost/time for proposed features.
Be realistic about complexity and timelines."""


def run_developer_estimate(context: str) -> ProductChange:
    llm = get_llm("developer")
    structured_llm = llm.with_structured_output(ProductChange)
    prompt = f"{DEVELOPER_SYSTEM_PROMPT}\n\nSituation:\n{context}\n\nEstimate cost and time for the proposed feature."
    return structured_llm.invoke(prompt)