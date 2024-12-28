import sys
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parent.parent))
sys.setrecursionlimit(50000)

import heapq
from collections import defaultdict

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


def get_adj(node_loc, node_dir):
    delta = [(0, 1), (-1, 0), (0, -1), (1, 0)] # ENWS <-> 0123
    # keep going straight
    new_loc = (node_loc[0] + delta[node_dir][0], node_loc[1] + delta[node_dir][1])
    if grid[new_loc[0]][new_loc[1]] != '#':
        yield (1, (new_loc, node_dir))
    # turn left
    yield (1000, (node_loc, (node_dir + 1) % 4))
    # turh right
    yield (1000, (node_loc, (node_dir - 1) % 4))
    
    
def dijkstra(s_loc):
    distances = defaultdict(lambda: float('inf'))
    from_records = defaultdict(set)
    
    distances[(s_loc, 0)] = 0
    
    q = []
    heapq.heappush(q, (0, (s_loc, 0))) # (cost, ((x, y), dir))
    
    while q:
        # print('\nqueue: {}'.format(q))
        curr_cost, node = heapq.heappop(q)
        # print('popping: ', curr_cost, node)
        node_loc, node_dir = node
        cost_so_far = distances[node]
        
        # already visited
        if cost_so_far < curr_cost:
            continue
        
        # cost: int, nb: ((x, y), dir)
        for cost, nb in get_adj(node_loc, node_dir):
            # print('checking adj: ', cost, nb)
            total_cost = curr_cost + cost
            if total_cost < distances[nb]:
                # print('updating from {} to {}'.format(distances[nb], total_cost))
                heapq.heappush(q, (total_cost, nb))
                distances[nb] = total_cost
                # print(distances)
                from_records[nb] = {node}
            elif total_cost == distances[nb]:
                from_records[nb].add(node)

    return distances, from_records
        
    
dist, records = dijkstra(s_loc)
for i in range(4):
    print('{}-th dir: {}'.format(i, dist[e_loc, i]))
    

# backtrack
best_dir = 1
shortest_path_nodes = set()
stack = [((e_loc), best_dir)]
while stack:
    looking_at = stack.pop()
    shortest_path_nodes.add(looking_at)
    for item in records[looking_at]:
        stack.append(item)

print(len(set(item[0] for item in shortest_path_nodes)))


# # recursive approach
# score_info = {key: {# 'score': float('inf'), 
#                     'E': float('inf'), 
#                     'N': float('inf'), 
#                     'W': float('inf'), 
#                     'S': float('inf')} for key in graph}

# delta = {'E': (0, 1), 'N': (-1, 0), 'W': (0, -1), 'S': (1, 0)}

# def get_adjacent(node_dir, node_pos):
#     node_x, node_y = node_pos
#     for dir, (dx, dy) in delta.items():
#         if grid[node_x + dx][node_y + dy] != '#':
#             if delta[node_dir][0] + dx != 0 or delta[node_dir][1] + dy != 0:
#                 yield (dir, (node_x + dx, node_y + dy))
    
# def walk(node_dir, node_pos):
#     if node_pos == e_loc:
#         return
    
#     for nbs in get_adjacent(node_dir, node_pos):
#         nbs_dir, nbs_pos = nbs
#         score_so_far = score_info[node_pos][node_dir]
#         score = score_so_far + 1 if node_dir == nbs_dir else score_so_far + 1001
#         if score < score_info[nbs_pos][nbs_dir]:
#             score_info[nbs_pos][nbs_dir] = score
#             walk(nbs_dir, nbs_pos)
        
# score_info[s_loc]['E'] = 0
# score_info[s_loc]['N'] = 0
# score_info[s_loc]['W'] = 0
# score_info[s_loc]['S'] = 0
# walk('E', s_loc)
# print(score_info[e_loc])