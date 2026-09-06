from app.llm.gateway import get_llm
from app.schemas import AgentDecision

FINANCE_SYSTEM_PROMPT = """You are Mark, the Finance agent for a company running a simulated product in a market.
You analyze budget, spending, revenue, expenses, and financial risk.
You evaluate whether proposed changes are financially feasible.
Be precise with numbers and conservative with risk."""


def run_finance_analysis(context: str) -> AgentDecision:
    llm = get_llm("finance")
    structured_llm = llm.with_structured_output(AgentDecision)
    prompt = f"{FINANCE_SYSTEM_PROMPT}\n\nSituation:\n{context}\n\nProvide your financial analysis and recommendation."
    return structured_llm.invoke(prompt)