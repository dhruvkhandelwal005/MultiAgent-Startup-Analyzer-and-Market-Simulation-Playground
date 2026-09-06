"""
Deterministic adoption calculation.
Given a population segment + product quality + awareness,
calculate how many people adopt the product.
"""

def calculate_adoption(
    population_size: int,
    product_relevance: float,   # 0-100
    purchasing_power: float,    # 0-100
    awareness: float,           # 0-100
    product_quality: float,     # 0-100
) -> dict:
    """
    Returns potential_users and active_users for a segment.
    All inputs 0-100 scale except population_size.
    """
    # Potential = people in segment who COULD adopt (relevance + purchasing power)
    potential_fraction = (product_relevance / 100) * (purchasing_power / 100)
    potential_users = int(population_size * potential_fraction)

    # Actual adoption depends on awareness (do they know?) and quality (do they want it?)
    adoption_fraction = (awareness / 100) * (product_quality / 100)
    active_users = int(potential_users * adoption_fraction)

    return {
        "potential_users": potential_users,
        "active_users": active_users,
    }