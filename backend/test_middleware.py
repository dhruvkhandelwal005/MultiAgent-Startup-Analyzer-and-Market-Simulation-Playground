from app.agents.ceo import run_ceo_decision

result = run_ceo_decision("Test event: revenue dropped 10%. No other data.")
print(result.action)