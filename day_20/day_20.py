import sys
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parent.parent))

from rsc.rsc import Reader, Matrix
from rsc.rsc import prettyprint

from collections import defaultdict
import heapq
import copy


def dijkstra(s):
    distances = defaultdict(lambda: float('inf'))
    prev_loc = dict()
    distances[s] = 0
    q = [(0, s)]
    
    while q:
        dist, node = heapq.heappop(q)
        for adj in graph[node]:
            new_dist = dist + 1
            if new_dist < distances[adj]:
                distances[adj] = new_dist
                prev_loc[adj] = node
                heapq.heappush(q, (new_dist, adj))
                
    return distances, prev_loc

        
def get_cheat_paths(path: list[tuple], grid: list[list], dur: int) -> dict[int: set[tuple[tuple]]]:
    # get shortest distance from every location in path to every location within the 2 * dur radius
    # filter out by end cheat location being the wall
    # return a dictionary with keys being the cost of the cheat path and the values being the start and end of the cheat path
    cheat_dict = defaultdict(set)
    for p in path:
        r_min = max(0, p[0] - dur)
        r_max = min(p[0] + dur + 1, len(grid))
        c_min = max(0, p[1] - dur)
        c_max = min(p[1] + dur + 1, len(grid[0]))
        for r in range(r_min, r_max):
            for c in range(c_min, c_max):
                shortest_dist = abs(p[0]-r) + abs(p[1]-c)
                if 0 < shortest_dist <= dur and grid[r][c] != '#':
                    cheat_dict[shortest_dist].add((p, (r, c))) # start and end of the cheat path
    return cheat_dict        
    

DEBUG = False
CHEAT_DUR = 20
LIMIT = 100

input_reader = Reader('day_20/day_20_input.txt')
grid_str,  = input_reader.get_item()

grid_builder = Matrix(grid_str)
grid = grid_builder.to_list()
if DEBUG:
    prettyprint(grid)

s_loc = grid_builder.get_loc('S')
e_loc = grid_builder.get_loc('E')
graph = grid_builder.to_graph()

# run dijkstra
dist_from_start, prev_loc = dijkstra(s_loc)
dist_from_end, _ = dijkstra(e_loc)

# shortest path distance
total_dist = dist_from_start[e_loc]

# path of the shortest path
path = []
path.append(e_loc)
while path[-1] != s_loc:
    path.append(prev_loc[path[-1]])
path.reverse()

if DEBUG:
    grid_copy = copy.deepcopy(grid)
    for p in path[1:-1]:
        grid_copy[p[0]][p[1]] = '■'
    prettyprint(grid_copy)

# activate cheat
cheat_sheet = defaultdict(int)
cheat_dict = get_cheat_paths(path, grid, CHEAT_DUR)
    
# calculate how much it saved
for cost, cheats in cheat_dict.items():
    for cheat in cheats:
        cheat_s_loc, cheat_e_loc = cheat
        cheat_dist = dist_from_end[cheat_e_loc] + dist_from_start[cheat_s_loc] + cost
        if cheat_dist < total_dist:
            cheat_sheet[total_dist - cheat_dist] += 1

count_count = 0
cheat_sheet = dict(sorted(cheat_sheet.items()))
for saved, count in cheat_sheet.items():
    if saved >= LIMIT:
        count_count += count
        print('{} cheats save {} picoseconds'.format(count, saved))
    
print(count_count)