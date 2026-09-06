"""
Market share and competitive dynamics.
"""

def calculate_competitive_pressure(
    our_quality: float,
    our_price: float,
    competitor_quality: float,
    competitor_price: float,
    competitor_marketing_strength: float,
) -> float:
    """
    Returns a pressure score 0-100. Higher = competitor is winning more attention.
    """
    quality_diff = competitor_quality - our_quality
    price_diff = our_price - competitor_price  # positive if we're more expensive
    pressure = (quality_diff * 0.5) + (price_diff * 0.2) + (competitor_marketing_strength * 0.3)
    return round(max(0, min(100, pressure)), 2)


def calculate_market_share(
    our_active_users: int,
    competitor_active_users_list: list[int],
) -> float:
    """
    Returns our market share as percentage 0-100.
    """
    total = our_active_users + sum(competitor_active_users_list)
    if total == 0:
        return 0.0
    return round((our_active_users / total) * 100, 2)


def apply_competitive_pressure_to_adoption(
    base_adoption_fraction: float,
    competitive_pressure: float,
) -> float:
    """
    Reduces adoption fraction based on competitive pressure (0-100).
    """
    reduction = competitive_pressure / 100 * 0.5  # max 50% reduction
    adjusted = base_adoption_fraction * (1 - reduction)
    return round(max(0, adjusted), 4)