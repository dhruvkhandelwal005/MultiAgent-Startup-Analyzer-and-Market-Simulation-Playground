from app.llm.gateway import get_llm
from app.schemas import ProductChange
from app.middleware.logging import log_agent_call

PRODUCT_SYSTEM_PROMPT = """You are Sam, the Product agent for a company running a simulated product in a market.
You analyze product-market fit, customer needs, and propose product improvements.
Focus on features that directly address competitive pressure or user needs."""

@log_agent_call("product")
def run_product_analysis(context: str) -> ProductChange:
    llm = get_llm("product")
    structured_llm = llm.with_structured_output(ProductChange)
    prompt = f"{PRODUCT_SYSTEM_PROMPT}\n\nSituation:\n{context}\n\nPropose one product change."
    return structured_llm.invoke(prompt)