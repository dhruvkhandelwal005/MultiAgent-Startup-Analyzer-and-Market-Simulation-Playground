from app.llm.gateway import get_llm
from app.schemas import ProductDefinition
from app.middleware.logging import log_agent_call
from app.llm.retry import invoke_with_fallback

PRODUCT_BUILDER_PROMPT = """You are the following team of agents collaboratively designing a new virtual product/company for a market simulation: {team}.
Given the founder's idea and budget, define a complete, coherent product: a name, a one-paragraph description, 3-5 concrete features, a monthly price in INR, 1-3 target customer segments, and an initial quality score (0-100, reflecting how polished the MVP is).
Only reason from the perspectives of the agents listed above — do not invent input from roles not on the team.
Be concrete and specific, not generic."""


@log_agent_call("product_builder")
def run_product_build(idea: str, budget: float, team_roles: list[str] | None = None) -> ProductDefinition:
    team = ", ".join(r.upper() for r in team_roles) if team_roles else "CEO, FINANCE, PRODUCT, DEVELOPER, MARKETING"
    prompt = (
        f"{PRODUCT_BUILDER_PROMPT.format(team=team)}\n\n"
        f"Founder's idea: {idea}\n"
        f"Initial budget: ₹{budget}\n\n"
        f"Define the product now."
    )
    return invoke_with_fallback("product_builder", ProductDefinition, prompt)