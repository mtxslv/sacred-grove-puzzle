import networkx as nx

TILE_GRAPH = nx.DiGraph()

# First we add the nodes, which represent the tiles. 
# We have 21 tiles, numbered from 1 to 21.
for i in range(21):
    TILE_GRAPH.add_node(i+1)

# Now we add the edges, which represent the connections between the tiles.

TILE_GRAPH.add_edge(1, 2, dir='E')
TILE_GRAPH.add_edge(2, 1, dir='W')

TILE_GRAPH.add_edge(1, 4, dir='S')
TILE_GRAPH.add_edge(4, 1, dir='N')

TILE_GRAPH.add_edge(2, 3, dir='E')
TILE_GRAPH.add_edge(3, 2, dir='W')

TILE_GRAPH.add_edge(2, 5, dir='S')
TILE_GRAPH.add_edge(5, 2, dir='N')

TILE_GRAPH.add_edge(3, 6, dir='S')
TILE_GRAPH.add_edge(6, 3, dir='N')

TILE_GRAPH.add_edge(4, 5, dir='E')
TILE_GRAPH.add_edge(5, 4, dir='W')

TILE_GRAPH.add_edge(5, 6, dir='E')
TILE_GRAPH.add_edge(6, 5, dir='W')

TILE_GRAPH.add_edge(6, 7, dir='E')
TILE_GRAPH.add_edge(7, 6, dir='W')

TILE_GRAPH.add_edge(7, 8, dir='E')
TILE_GRAPH.add_edge(8, 7, dir='W')

TILE_GRAPH.add_edge(5, 9, dir='S')
TILE_GRAPH.add_edge(9, 5, dir='N')

TILE_GRAPH.add_edge(6, 10, dir='S')
TILE_GRAPH.add_edge(10, 6, dir='N')

TILE_GRAPH.add_edge(7, 11, dir='S')
TILE_GRAPH.add_edge(11, 7, dir='N')

TILE_GRAPH.add_edge(8, 12, dir='S')
TILE_GRAPH.add_edge(12, 8, dir='N')

TILE_GRAPH.add_edge(9, 10, dir='E')
TILE_GRAPH.add_edge(10, 9, dir='W')

TILE_GRAPH.add_edge(10, 11, dir='E')
TILE_GRAPH.add_edge(11, 10, dir='W')

TILE_GRAPH.add_edge(11, 12, dir='E')
TILE_GRAPH.add_edge(12, 11, dir='W')

TILE_GRAPH.add_edge(12, 13, dir='E')
TILE_GRAPH.add_edge(13, 12, dir='W')

TILE_GRAPH.add_edge(9, 15, dir='S')
TILE_GRAPH.add_edge(15, 9, dir='N')

TILE_GRAPH.add_edge(10, 16, dir='S')
TILE_GRAPH.add_edge(16, 10, dir='N')

TILE_GRAPH.add_edge(11, 17, dir='S')
TILE_GRAPH.add_edge(17, 11, dir='N')

TILE_GRAPH.add_edge(12, 18, dir='S')
TILE_GRAPH.add_edge(18, 12, dir='N')

TILE_GRAPH.add_edge(14, 15, dir='E')
TILE_GRAPH.add_edge(15, 14, dir='W') 

TILE_GRAPH.add_edge(15, 16, dir='E')
TILE_GRAPH.add_edge(16, 15, dir='W')

TILE_GRAPH.add_edge(16, 17, dir='E')
TILE_GRAPH.add_edge(17, 16, dir='W')

TILE_GRAPH.add_edge(17, 18, dir='E')
TILE_GRAPH.add_edge(18, 17, dir='W')

TILE_GRAPH.add_edge(14, 19, dir='S')
TILE_GRAPH.add_edge(19, 14, dir='N')

TILE_GRAPH.add_edge(15, 20, dir='S')
TILE_GRAPH.add_edge(20, 15, dir='N')

TILE_GRAPH.add_edge(16, 21, dir='S')
TILE_GRAPH.add_edge(21, 16, dir='N')

TILE_GRAPH.add_edge(19, 20, dir='E')
TILE_GRAPH.add_edge(20, 19, dir='W')

TILE_GRAPH.add_edge(20, 21, dir='E') 
TILE_GRAPH.add_edge(21, 20, dir='W')