from app.llm.gateway import get_llm
from app.schemas import AgentDecision
from app.middleware.logging import log_agent_call

CEO_SYSTEM_PROMPT = """You are Alex, the CEO of a company running a simulated product in a market.
You review analysis from Finance, Product, Developer, and Marketing agents,
then make a final strategic decision.
Be decisive, concise, and grounded in the data given to you."""

@log_agent_call("ceo")
def run_ceo_decision(context: str) -> AgentDecision:
    """
    context: a text summary of the current situation (event, other agents' analysis, budget, etc.)
    Returns a structured AgentDecision.
    """
    llm = get_llm("ceo")
    structured_llm = llm.with_structured_output(AgentDecision)

    prompt = f"{CEO_SYSTEM_PROMPT}\n\nSituation:\n{context}\n\nMake your decision. Keep 'reason' and 'expected_impact' under 40 words each."

    from app.llm.retry import invoke_with_retry
    decision = invoke_with_retry(structured_llm, prompt)
    return decision