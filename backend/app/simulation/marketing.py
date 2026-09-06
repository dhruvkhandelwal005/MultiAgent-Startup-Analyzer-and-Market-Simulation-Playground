"""
Marketing campaign impact calculations.
"""

def calculate_awareness_boost(
    current_awareness: float,
    campaign_budget: float,
    segment_population: int,
) -> float:
    """
    Returns new awareness (0-100) after a campaign.
    Budget per capita drives awareness increase, with diminishing returns.
    """
    if segment_population == 0:
        return current_awareness

    budget_per_capita = campaign_budget / segment_population
    # Diminishing returns curve
    boost = min(40, budget_per_capita * 1000)
    new_awareness = min(100, current_awareness + boost)
    return round(new_awareness, 2)


def calculate_campaign_reach(campaign_budget: float, cost_per_reach: float = 5.0) -> int:
    """
    Estimate how many people a campaign reaches given budget.
    """
    if cost_per_reach <= 0:
        return 0
    return int(campaign_budget / cost_per_reach)