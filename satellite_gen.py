import csv
import random

N = 113
OUT = "synthetic3.csv"
SEED = 112

random.seed(SEED)

with open(OUT, "w", newline="", encoding="utf-8") as f:
    w = csv.writer(f)
    w.writerow(["satellite", "fuel_cost_kg", "revenue_usd"])

    for i in range(1, N + 1):
        name = f"SAT-{i:03d}"                         # Name Satellite sequentially
        fuel = round(random.uniform(0.1, 20.0), 2)    # Randomly generate fuel cost from 0.1 kg to 20.kg, round to 2 dec places
        revenue = random.randint(100, 50000)          # Randomly generate revenue from $100 to $50,000
        w.writerow([name, fuel, revenue])

print(f"Wrote {N} rows to {OUT}")
