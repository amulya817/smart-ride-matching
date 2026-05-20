import networkx as nx

def create_city_graph(grid_size=20):
    G = nx.grid_2d_graph(grid_size, grid_size)

    # Assign uniform weights
    for edge in G.edges():
        G.edges[edge]['weight'] = 1

    return G


def shortest_path_distance(start, end, grid_size=20):
    G = create_city_graph(grid_size)

    start_node = (start[0], start[1])
    end_node = (end[0], end[1])

    distance = nx.shortest_path_length(
        G,
        source=start_node,
        target=end_node,
        weight='weight'
    )

    path = nx.shortest_path(
        G,
        source=start_node,
        target=end_node,
        weight='weight'
    )

    return distance, path


# Test example
if __name__ == "__main__":
    start = (2, 3)
    end = (15, 18)

    distance, path = shortest_path_distance(start, end)

    print(f"Shortest Distance: {distance}")
    print(f"Path: {path}")