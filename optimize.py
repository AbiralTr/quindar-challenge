import csv

def greedy_optimize(csv_path, capacity_kg=20.0):
    # Read items from CSV
    items = []
    with open(csv_path, "r", newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for idx, row in enumerate(reader):
            name = row["satellite"]
            fuel = float(row["fuel_cost_kg"])
            revenue = int(row["revenue_usd"])

            if fuel <= 0:
                continue

            density = revenue / fuel  # Dollars per kg
            items.append((idx, name, fuel, revenue, density))

    # Sort by best density first (descending)
    items.sort(key=lambda x: x[4], reverse=True)

    selected_indices = set()
    fuel_used = 0.0
    revenue_total = 0

    # Greedy selection: take the next best density item if it fits
    for idx, name, fuel, revenue, density in items:
        if fuel_used + fuel <= capacity_kg:
            selected_indices.add(idx)
            fuel_used += fuel
            revenue_total += revenue

    return selected_indices, revenue_total

def dp_optimize(csv_path, capacity_kg=20.0, scale=100):
    CAPACITY = int(round(capacity_kg * scale))

    items = []
    with open(csv_path, "r", newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for idx, row in enumerate(reader):
            name = row["satellite"]
            fuel_kg = float(row["fuel_cost_kg"])
            revenue = int(row["revenue_usd"])

            if fuel_kg <= 0:
                continue

            fuel = int(round(fuel_kg * scale))  # kg to integer fuel units
            items.append((idx, name, fuel, revenue, fuel_kg))

    n = len(items) # Getting the number of 'opportunities'

    # Store subproblems in memo so that if they are seen again, we can quickly grab the value
    memo = {}

    # Recursive Function (passes item index, and current fuel units remaining)
    def best_value(i, cap):

        # Base case, return 0 if we are at the end of the items, or if we have no more fuel units (cap) left
        if i == n or cap <= 0:
            return 0

        # If this recursive call has already been comleted (stored in memo), return the stored value from the dict
        key = (i, cap)
        if key in memo:
            return memo[key]

        # Obtain all current item info at index i
        idx, name, fuel, revenue, fuel_kg = items[i]

        # If we skip this opportunity, then just move onto the next one without any lost fuel units
        skip = best_value(i + 1, cap)

        # If we want to take this opportunity, then check if we have enough fuel units
        take = -1 # init take to -1 so that if we don't have enough fuel it is marked as unavailable predeterminantly
        if fuel <= cap:
            # If we take it, then increment index by one, subtract fuel units necessary from our cap, and move onto the next one as we add it to revenue
            take = revenue + best_value(i + 1, cap - fuel)

        # Compare take vs skip, store the best val in memo and store the decision between these two in choice
        if take > skip:
            memo[key] = take
        else:
            memo[key] = skip

        # Return the best value
        return memo[key]

    # Call the recursive statement starting at index 0 and with a full capacity of fuel units
    best_revenue = best_value(0, CAPACITY)

    selected_indices = set()
    i = 0
    cap = CAPACITY

    while i < n and cap > 0:
        idx, name, fuel, revenue, fuel_kg = items[i]

        skip = best_value(i + 1, cap)

        take = -1
        if fuel <= cap:
            take = revenue + best_value(i + 1, cap - fuel)

        if fuel <= cap and take >= skip:
            selected_indices.add(idx)
            cap -= fuel

        i += 1

    return selected_indices, best_revenue

if __name__ == "__main__":
    CSV_PATH = "synthetic3.csv"
    CAPACITY_KG = 20.0
    SCALE = 100  # only used by DP for fuel units

    greedy_selected, greedy_revenue = greedy_optimize(CSV_PATH, capacity_kg=CAPACITY_KG)
    dp_selected, dp_revenue = dp_optimize(CSV_PATH, capacity_kg=CAPACITY_KG, scale=SCALE)

    print("Results:\n\n")
    print(f"CSV: {CSV_PATH}")
    print(f"Capacity: {CAPACITY_KG} kg\n")

    print("Greedy:")
    print(f"Selected indices: {sorted(greedy_selected)}")
    print(f"Total revenue: ${greedy_revenue:,}\n")

    print("DP (Recursive):")
    print(f"Selected indices: {sorted(dp_selected)}")
    print(f"Total revenue: ${dp_revenue:,}\n")