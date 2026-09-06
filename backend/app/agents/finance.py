from app.llm.gateway import get_llm
from app.schemas import AgentDecision
from app.middleware.logging import log_agent_call
from app.llm.retry import invoke_with_fallback

FINANCE_SYSTEM_PROMPT = """You are Mark, the Finance agent for a company running a simulated product in a market.
You analyze budget, spending, revenue, expenses, and financial risk.
You evaluate whether proposed changes are financially feasible.
Be precise with numbers and conservative with risk."""

@log_agent_call("finance")
def run_finance_analysis(context: str) -> AgentDecision:
    prompt = f"{FINANCE_SYSTEM_PROMPT}\n\nSituation:\n{context}\n\nProvide your financial analysis and recommendation."
    decision = invoke_with_fallback("finance", AgentDecision, prompt)
    return decision