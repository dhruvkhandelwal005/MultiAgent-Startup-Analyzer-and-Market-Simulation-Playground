from app.llm.gateway import get_llm
from app.schemas import MarketingDecision
from app.middleware.logging import log_agent_call
from app.llm.retry import invoke_with_fallback

MARKETING_SYSTEM_PROMPT = """You are Mia, the Marketing agent for a company running a simulated product in a market.
You design campaigns, choose target segments, and estimate reach and conversion.
Be strategic about budget allocation and segment targeting."""

@log_agent_call("marketing")
def run_marketing_decision(context: str) -> MarketingDecision:
    prompt = f"{MARKETING_SYSTEM_PROMPT}\n\nSituation:\n{context}\n\nPropose a marketing campaign."
    return invoke_with_fallback("marketing", MarketingDecision, prompt)