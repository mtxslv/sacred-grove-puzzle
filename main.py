from puzzle_graph import TILE_GRAPH
from moving_characters import WolfLink, Statue
from search import Search
from state_graph_generation import StateGraphGenerator
from pathlib import Path
import networkx as nx
dir_to_save = Path(__file__).parent

def print_trajectory(wolf_link: WolfLink, statue_mirror: Statue, statue_shadow: Statue):
    print("Trajectory:")
    for i in range(len(wolf_link.history)):
        print(f"Step {str(i).rjust(2)} | WL: {str(wolf_link.history[i]).rjust(2)} | MS: {str(statue_mirror.history[i]).rjust(2)} | SS: {str(statue_shadow.history[i]).rjust(2)}")

def main():
    mirror_statue = Statue(position=9, pattern='mirror')
    wolf_link = WolfLink(position=11)
    shadow_statue = Statue(position=13, pattern='shadow')
    search = Search(
        graph=TILE_GRAPH, 
        wolf_link=wolf_link, 
        statue_mirror=mirror_statue, 
        statue_shadow=shadow_statue,
        maximum_steps=200)
    search.random_walk_search()
    print_trajectory(wolf_link, mirror_statue, shadow_statue)

def save_state_graph(graph):
    ## 4. Save the graph to a GraphML file
    file_name = dir_to_save / 'state-graph.graphml'
    try:
        nx.write_graphml(
            graph, 
            file_name,
            encoding='utf-8',
            infer_numeric_types=True
        )
        print(f"Successfully saved the graph to {file_name}")
    except Exception as e:
        print(f"An error occurred while saving the file: {e}")    

def graph_generation():
    state_graph_generator = StateGraphGenerator(graph=TILE_GRAPH)
    state_graph = state_graph_generator.brute_force_state_graph_generation()
    print(f"Generated state graph with {len(state_graph)} states.")
    save_state_graph(state_graph)

if __name__ == "__main__":
    # main()
    graph_generation()

# def main():
#     # Example usage: find all nodes reachable from node 11 and their metadata
#     reachable_nodes = TILE_GRAPH.neighbors(11)
#     for node in reachable_nodes:
#         edge_data = TILE_GRAPH.get_edge_data(11, node)
#         # print(f"Node 11 is connected to Node {node} with direction {edge_data.get('jamal', None)}")
#         print(f"Node 11 is connected to Node {node} with direction {edge_data['dir']}")
# if __name__ == "__main__":
#     main()

#     print(
#         next(iter(
#             [n for n in TILE_GRAPH.neighbors(9) if TILE_GRAPH.get_edge_data(9, n).get('dir') == 'J']
#         ),9)
#     )