import sys
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parent.parent))

from collections import deque
import heapq

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


def dijkstra(graph, s_loc, with_path = False):
    delta = {(0, 1): 'E', (0, -1): 'W', (-1, 0): 'N', (1, 0): 'S'}
    
    if with_path:
        distances = {node: (float('inf'), None, []) for node in graph} # score, dir, path
        distances[s_loc] = (0, 'E', [s_loc])
    else:
        distances = {node: (float('inf'), None) for node in graph} # score, dir
        distances[s_loc] = (0, 'E')
    
    q = []
    heapq.heappush(q, (0, s_loc))
    
    while q:
        dist, node = heapq.heappop(q)
        node_dist, node_dir, *path = distances[node]
        
        if node_dist < dist: # already visited
            continue

        for nb in graph[node]:
            nb_delta = (nb[0] - node[0], nb[1] - node[1])
            nb_dir = delta[nb_delta]
            cost = (node_dist + 1) if node_dir == nb_dir else (node_dist + 1001)
            if cost < distances[nb][0]:
                heapq.heappush(q, (cost, nb))
                if with_path:
                    distances[nb] = (cost, nb_dir, path + [nb])
                else:
                    distances[nb] = (cost, nb_dir)

    return distances
        
    
dist = dijkstra(graph, s_loc)
print(dist[e_loc])
    
# path = dist[e_loc][2]
# for loc in path:
#     grid[loc[0]][loc[1]] = '>'
    
# prettyprint(grid)
    