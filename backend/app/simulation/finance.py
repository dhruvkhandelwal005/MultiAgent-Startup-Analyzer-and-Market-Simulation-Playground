"""
Deterministic financial calculations.
"""

def calculate_revenue(active_users: int, price: float) -> float:
    return round(active_users * price, 2)


def calculate_expenses(
    base_burn: float,
    marketing_spend: float,
    development_spend: float,
) -> float:
    return round(base_burn + marketing_spend + development_spend, 2)


def calculate_cash_remaining(
    current_cash: float,
    revenue: float,
    expenses: float,
) -> float:
    return round(current_cash + revenue - expenses, 2)