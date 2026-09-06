"""
User churn calculations.
"""

def calculate_churn(
    active_users: int,
    product_quality: float,
    competitive_pressure: float,
) -> int:
    """
    Returns number of users who churn this period.
    Low quality + high competitive pressure = more churn.
    """
    base_churn_rate = 0.05  # 5% baseline
    quality_factor = (100 - product_quality) / 100 * 0.1  # up to +10%
    pressure_factor = competitive_pressure / 100 * 0.1     # up to +10%

    churn_rate = base_churn_rate + quality_factor + pressure_factor
    churn_rate = min(0.5, churn_rate)  # cap at 50%

    return int(active_users * churn_rate)