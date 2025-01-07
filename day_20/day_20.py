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


def get_cheat_paths(path: list[tuple], grid: list[list], dur: int) -> list[tuple[tuple, tuple]]:
    # start -> dur -> end
    
    def is_in_range(loc):
        return (0 < loc[0] < len(grid) - 1) and (0 < loc[1] < len(grid[0]) - 1)

    def take_steps(loc, dur):
        all_steps = [[loc]]
        count = 0
        first_cheat_step = True
        delta = [(-1, 0), (1, 0), (0, -1), (0, 1)] # up, down, left, right
        
        while count < dur:
            new_steps = []
            
            for cheat_path in all_steps:
                prev = cheat_path[-1]
                
                for d in delta:
                    dr, dc = d
                    next_loc = (prev[0] + dr, prev[1] + dc)
                    
                    if is_in_range(next_loc):
                        if first_cheat_step:
                            # first cheat step has to be the wall
                            if grid[next_loc[0]][next_loc[1]] == '#':
                                new_steps.append(cheat_path + [next_loc])
                        else:
                            # assumption: cannot repat the cheat loc
                            if next_loc not in cheat_path:
                                new_steps.append(cheat_path + [next_loc])
                                
                first_cheat_step = False
                
                all_steps = copy.deepcopy(new_steps)
            count += 1

        # filter out invalid cheat path
        cheat_paths = []
        for cheat_path in all_steps:
            # has to end on the path
            if cheat_path[-1] in path:
                # uniquely defined by the start and the end
                # TODO: need to redefine end
                
                end_idx = 1
                while True:
                    if grid[cheat_path[-1 * (end_idx + 1)][0]][cheat_path[-1 * (end_idx + 1)][1]] == '#':
                        break
                    else:
                        end_idx += 1
                
                # unique_cheat_path = (cheat_path[0], cheat_path[-1 * end_idx])
                if end_idx == 1:
                    unique_cheat_path = cheat_path
                else:
                    unique_cheat_path = cheat_path[:-1 * end_idx + 1]
                    
                if unique_cheat_path not in cheat_paths:
                    cheat_paths.append(unique_cheat_path)
                
        return cheat_paths

    all_cheat_paths = []
    for loc in path:
        cheat_paths = take_steps(loc, dur)
        all_cheat_paths.extend(cheat_paths)
    
    return all_cheat_paths
        
        
def get_cheat_paths_2(path: list[tuple], grid: list[list], dur: int) -> dict[int: set[tuple[tuple]]]:
    cheat_paths = defaultdict(set)
    for p in path:
        r_min = max(0, p[0] - dur)
        r_max = min(p[0] + dur + 1, len(grid))
        c_min = max(0, p[1] - dur)
        c_max = min(p[1] + dur + 1, len(grid[0]))
        for r in range(r_min, r_max):
            for c in range(c_min, c_max):
                shortest_dist = abs(p[0]-r) + abs(p[1]-c)
                if 0 < shortest_dist <= dur and grid[r][c] != '#':
                    cheat_paths[shortest_dist].add((p, (r, c))) # start and end of the cheat path
    return cheat_paths        
    

DEBUG = False
CHEAT_DUR = 20
LIMIT = 100

input_reader = Reader('day_20/day_20_input.txt')
grid_str,  = input_reader.get_item()

grid_builder = Matrix(grid_str)
grid = grid_builder.to_list()
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
# cheat_paths = get_cheat_paths(path, grid, CHEAT_DUR) # ((cheat_s_loc), (cheat_e_loc))
cheat_paths = get_cheat_paths_2(path, grid, CHEAT_DUR)


# # PART 1: calculate how much it saved
# for cheat_path in cheat_paths:
#     cheat_s_loc, cheat_e_loc = cheat_path[0], cheat_path[-1]
#     cheat_dist = dist_from_end[cheat_e_loc] + dist_from_start[cheat_s_loc] + CHEAT_DUR
#     if cheat_dist < total_dist:
#         cheat_sheet[total_dist - cheat_dist] += 1
        
#         if DEBUG:
#             print('SAVES {} PICOSEC'.format(total_dist - cheat_dist))
#             grid_copy = copy.deepcopy(grid)
#             for idx, p in enumerate(cheat_path):
#                 grid_copy[p[0]][p[1]] = str(idx)
#                 grid_copy[p[0]][p[1]] = str(idx)
#             prettyprint(grid_copy)
    
# PART 2: calculate how much it saved
for cost, cheats in cheat_paths.items():
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
