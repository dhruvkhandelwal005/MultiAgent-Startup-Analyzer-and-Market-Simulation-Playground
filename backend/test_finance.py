from app.simulation.finance import calculate_revenue, calculate_expenses, calculate_cash_remaining

revenue = calculate_revenue(active_users=1343, price=199)
expenses = calculate_expenses(base_burn=50000, marketing_spend=20000, development_spend=0)
cash = calculate_cash_remaining(current_cash=1000000, revenue=revenue, expenses=expenses)

print("Revenue:", revenue)
print("Expenses:", expenses)
print("Cash remaining:", cash)