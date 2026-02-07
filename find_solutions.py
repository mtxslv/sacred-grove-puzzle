import networkx as nx
from pathlib import Path

dir_to_save = Path(__file__).parent
file_name = dir_to_save / 'state-graph.graphml'

try:
    graph = nx.read_graphml(file_name)
    print(f"Successfully loaded the graph from {file_name}")
    print(f"Graph has {len(graph.nodes)} nodes and {len(graph.edges)} edges.")
except Exception as e:
    print(f"An error occurred while loading the file: {e}")

# List all solution nodes
# That is, those with shadow_statue_position, mirror_statue_position equal to 5, 15 or 15, 5
solution_nodes = []
for node in graph.nodes:
    node_data = graph.nodes[node]
    if (node_data.get('shadow_statue_position') == 5 and node_data.get('mirror_statue_position') == 15) or \
       (node_data.get('shadow_statue_position') == 15 and node_data.get('mirror_statue_position') == 5):
        solution_nodes.append(node)
print(f"Found {len(solution_nodes)} solution nodes:")
for node in solution_nodes:
    print(f"Node {node} with data: {graph.nodes[node]}")

original_state = (11, 13, 9)  # (wolf_link_position, mirror_statue_position, shadow_statue_position)

# run dijkstra between original state and first solution node with weight as the number of steps
if solution_nodes:
    solution_node = solution_nodes[0]
    try:
        path = nx.dijkstra_path(graph, source=str(original_state), target=solution_node, weight='steps')
        print('\n\n\n-------------')
        print(f"Shortest path from {original_state} to {solution_node}:")
        for step in path:
            print(f"Node {step} with data: {graph.nodes[step]}")
    except nx.NetworkXNoPath:
        print(f"No path found from {original_state} to {solution_node}.")
else:
    print("No solution nodes found in the graph.")

# Now run dijkstra between original state and all solution nodes, and find the shortest path among them
shortest_path = None
shortest_path_length = float('inf')
for solution_node in solution_nodes:
    try:
        path = nx.dijkstra_path(graph, source=str(original_state), target=solution_node, weight='steps')
        path_length = nx.dijkstra_path_length(graph, source=str(original_state), target=solution_node, weight='steps')
        if path_length < shortest_path_length:
            shortest_path_length = path_length
            shortest_path = path
    except nx.NetworkXNoPath:
        print(f"No path found from {original_state} to {solution_node}.")
if shortest_path:
    print('\n\n\n-------------')
    print(f"Shortest path from {original_state} to any solution node (length {shortest_path_length}):")
    for step in shortest_path:
        print(f"Node {step} with data: {graph.nodes[step]}")
else:
    print("No path found from original state to any solution node.")
    