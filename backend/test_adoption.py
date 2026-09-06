from app.simulation.adoption import calculate_adoption

result = calculate_adoption(
    population_size=10000,
    product_relevance=80,
    purchasing_power=60,
    awareness=40,
    product_quality=70,
)
print(result)