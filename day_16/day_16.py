import sys
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parent.parent))

from collections import deque

from rsc.rsc import Reader, Matrix
from rsc.rsc import prettyprint

input_reader = Reader('day_16/day_16_input.txt')
grid_str,  = input_reader.get_item()

grid_builder = Matrix(grid_str)
grid = grid_builder.to_list()
prettyprint(grid)

s_loc = grid_builder.get_loc('S')
e_loc = grid_builder.get_loc('E')
graph = grid_builder.to_graph()


def bfs(graph, s_loc, e_loc):
    # TODO: bfs giving priority to the direction it's currently on
    queue = deque([[s_loc]]) # keep list of paths
    while queue:
        path = queue.popleft()
        node = path[-1]
        if node == e_loc:
            return path
        for adj in graph.get(node, []):
            if adj not in path:
                new_path = list(path)
                new_path.append(adj)
                queue.append(new_path)

# path = bfs(graph, s_loc, e_loc)

# for loc in path:
#     grid[loc[0]][loc[1]] = '>'
    
# prettyprint(grid)

def get_min_node(distances, visited):
    min_node = None
    min_node_dist = float('inf')
    for node in distances:
        if node not in visited:
            if distances[node][0] <= min_node_dist:
                min_node = node
                min_node_dist = distances[node][0]
    return min_node

def dijkstra(graph, s_loc, with_path = False):
    # delta = {'E': (0, 1), 'W': (0, -1), 'N': (-1, 0), 'S': (1, 0)}
    delta = {(0, 1): 'E', (0, -1): 'W', (-1, 0): 'N', (1, 0): 'S'}
    
    if with_path:
        distances = {node: (float('inf'), None, []) for node in graph} # score, dir, path
        distances[s_loc] = (0, 'E', [s_loc])
    else:
        distances = {node: (float('inf'), None) for node in graph} # score, dir
        distances[s_loc] = (0, 'E')
    
    visited = set()
    visited.add(s_loc)
    
    # start with the s_loc
    for nb in graph[s_loc]:
        curr_delta = (nb[0] - s_loc[0], nb[1] - s_loc[1])
        s_to_nb = 1 if distances[s_loc][1] == delta[curr_delta] else 1001
        if distances[s_loc][0] + s_to_nb < distances[nb][0]:
            if with_path:
                distances[nb] = (distances[s_loc][0] + s_to_nb, delta[curr_delta], distances[s_loc][2] + [nb])
            else:
                distances[nb] = (distances[s_loc][0] + s_to_nb, delta[curr_delta])
            
    # for rest of the nodes 
    for _ in range(len(graph) - 1):
        node = get_min_node(distances, visited)
        visited.add(node)
        
        for nb in graph[node]:
            curr_delta = (nb[0] - node[0], nb[1] - node[1])
            node_to_nb = 1 if distances[node][1] == delta[curr_delta] else 1001
            if distances[node][0] + node_to_nb < distances[nb][0]:
                if with_path:
                    distances[nb] = (distances[node][0] + node_to_nb, delta[curr_delta], distances[node][2] + [nb])
                else:
                    distances[nb] = (distances[node][0] + node_to_nb, delta[curr_delta])
    
    return distances
        
    
dist = dijkstra(graph, s_loc)
print(dist[e_loc])
    
# path = dist[e_loc][2]
# for loc in path:
#     grid[loc[0]][loc[1]] = '>'
    
# prettyprint(grid)
    