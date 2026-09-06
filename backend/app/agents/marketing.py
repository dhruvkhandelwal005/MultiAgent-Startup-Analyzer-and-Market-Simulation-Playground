from app.llm.gateway import get_llm
from app.schemas import MarketingDecision
from app.middleware.logging import log_agent_call

MARKETING_SYSTEM_PROMPT = """You are Mia, the Marketing agent for a company running a simulated product in a market.
You design campaigns, choose target segments, and estimate reach and conversion.
Be strategic about budget allocation and segment targeting."""

@log_agent_call("marketing")
def run_marketing_decision(context: str) -> MarketingDecision:
    llm = get_llm("marketing")
    structured_llm = llm.with_structured_output(MarketingDecision)
    prompt = f"{MARKETING_SYSTEM_PROMPT}\n\nSituation:\n{context}\n\nPropose a marketing campaign."
    return structured_llm.invoke(prompt)