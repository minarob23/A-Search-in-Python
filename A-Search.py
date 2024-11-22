import pandas as pd

# Function to input the graph connections and heuristic values
def input_graph():
    graph = {}
    heuristic = {}
    nodes = []

    # Input number of nodes
    num_nodes = int(input("Enter the number of cities (nodes): "))

    # Input the cities and their heuristic values
    print("Enter the city names and their heuristic values (h):")
    for _ in range(num_nodes):
        city = input(f"City {_ + 1}: ")
        nodes.append(city)
        heuristic[city] = float(input(f"Heuristic value (h) for {city}: "))
        graph[city] = {}

    # Input the graph connections (edges)
    print("\nEnter the connections between cities (no duplicate neighbors):")
    for i, city in enumerate(nodes):
        print(f"Enter neighbors of {city} (type 'done' to stop):")
        entered_neighbors = set()
        while True:
            neighbor = input(f"  Neighbor of {city}: ")
            if neighbor.lower() == 'done':
                break
            if neighbor not in nodes:
                print("  Invalid city name! Try again.")
                continue
            if neighbor in entered_neighbors:
                print(f"  {neighbor} is already entered as a neighbor. Try another city.")
                continue
            if neighbor in graph[city]:  # If the reverse already exists, don't add it
                print(f"  The connection between {city} and {neighbor} already exists. Skipping.")
                continue
            cost = float(input(f"    Cost to {neighbor}: "))
            graph[city][neighbor] = cost
            graph[neighbor][city] = cost  # Symmetric connection
            entered_neighbors.add(neighbor)

    return graph, heuristic

# A* Search Function
def a_star_search(graph, heuristic, start, goal):
    agenda = [(start, 0)]  # (node, g(n))
    visited = set()
    path = {}
    g = {node: float('inf') for node in graph}
    g[start] = 0
    iteration_num = 1

    while agenda:
        # Sort by f(n) = g(n) + h(n)
        agenda.sort(key=lambda x: g[x[0]] + heuristic[x[0]])
        current, current_cost = agenda.pop(0)

        # Display iteration number
        print(f"\n--- Iteration {iteration_num} ---")

        # Log and display iteration details for all nodes
        iteration_details = {
            'Node': [],
            'g(n)': [],
            'h(n)': [],
            'g+h': [],
            'Visited': []
        }

        # Populate the iteration details for all nodes
        for node in graph:
            iteration_details['Node'].append(node)
            iteration_details['g(n)'].append(g[node] if node in g else float('inf'))
            iteration_details['h(n)'].append(heuristic[node])
            iteration_details['g+h'].append(g[node] + heuristic[node] if node in g else float('inf'))
            iteration_details['Visited'].append(1 if node in visited else 0)

        # Convert to DataFrame and display it
        iteration_table = pd.DataFrame(iteration_details)
        print(iteration_table.to_string(index=False))

        iteration_num += 1

        if current == goal:
            break

        visited.add(current)

        for neighbor, cost in graph[current].items():
            if neighbor not in visited:
                new_cost = g[current] + cost
                if new_cost < g[neighbor]:
                    g[neighbor] = new_cost
                    agenda.append((neighbor, new_cost))
                    path[neighbor] = current

    # Construct optimal path
    optimal_path = []
    temp = goal
    while temp in path:
        optimal_path.append(temp)
        temp = path[temp]
    optimal_path.append(start)
    optimal_path.reverse()

    return optimal_path

# Main Function
if __name__ == "__main__":
    # Input graph and heuristic
    graph, heuristic = input_graph()

    # Input source and destination
    start_node = input("\nEnter the source city: ")
    goal_node = input("Enter the destination city: ")

    # Run A* Search
    optimal_path = a_star_search(graph, heuristic, start_node, goal_node)

    # Display Optimal Path
    print("\nOptimal Path:")
    print(" -> ".join(optimal_path))
