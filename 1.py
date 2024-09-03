def min_cost_to_send_luggage(n, m, weights, cycles_and_costs):
    min_cost = float('inf')

    for i in range(m):
        w = weights[i]
        k = cycles_and_costs[i][0]
        costs = cycles_and_costs[i][1:]

        # Calculate total cost for this company
        total_cost = w  # Add the base weight cost
        for j in range(n):
            cycle_index = j % k
            total_cost += costs[cycle_index]

        min_cost = min(min_cost, total_cost)

    return min_cost


# Read input
n, m = map(int, input().split())
weights = list(map(int, input().split()))

cycles_and_costs = []
for _ in range(m):
    line = list(map(int, input().split()))
    k = line[0]
    costs = line[1:]
    cycles_and_costs.append((k, costs))

# Calculate and print the minimum cost
print(min_cost_to_send_luggage(n, m, weights, cycles_and_costs))
