import sys
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parent.parent))

from rsc.rsc import prettyprint

from collections import deque, defaultdict
import heapq

        
def make_grid(num_row, num_col, bytes):
    grid = [['.'] * num_col for _ in range(num_row)]
    for r, c in bytes:
        grid[r][c] = '#'
    return grid

def get_adj(loc, grid, num_row, num_col):
    r, c = loc
    if 0 < r and grid[r - 1][c] != '#':
        yield (r - 1, c)
    if r < num_row - 1 and grid[r + 1][c] != '#':
        yield (r + 1, c)
    if 0 < c and grid[r][c - 1] != '#':
        yield (r, c - 1)
    if c < num_col - 1 and grid[r][c + 1] != '#':
        yield (r, c + 1)    
    
def bfs(grid, s, e, num_row, num_col):
    q = deque([(0, s)])
    v = set()
    
    while q:
        dist, curr_loc = q.popleft()
        
        v.add(curr_loc)
        if curr_loc == e:
            return dist
            
        for adj in get_adj(curr_loc, grid, num_row, num_col):
            if adj not in v:
                q.append((dist + 1, adj))
        

def dijkstra(grid, s, e, num_col, num_row):
    distances = defaultdict(lambda: float('inf'))
    distances[s] = 0
    q = [s]
    while q:
        curr_loc = heapq.heappop(q)
        
        for adj in get_adj(curr_loc, grid, num_col, num_row):
            if distances[curr_loc] + 1 < distances[adj]:
                distances[adj] = distances[curr_loc] + 1
                heapq.heappush(q, adj)
    return distances[e]
    
def parse(file_path = 'day_18/day_18_input.txt', clip = True):
    with open(file_path) as file:
        bytes = []
        for line in file:
            x, y = line.strip().split(',') 
            bytes.append((int(y), int(x)))
    if 'ex' in file_path:
        num_row, num_col = 7, 7
        if clip:
            bytes =  bytes[:12]
    elif 'input' in file_path:
        num_row, num_col = 71, 71
        if clip:
            bytes =  bytes[:1024]
    return bytes, num_row, num_col
        

# # Part 1
# bytes, num_row, num_col = parse('day_18/day_18_input.txt')

# grid = make_grid(num_row, num_col, bytes)
# prettyprint(grid)
# s, e = (0, 0), (num_row - 1, num_col - 1)
# print(dijkstra(grid, s, e, num_row, num_col))


# Part 2
bytes, num_row, num_col = parse('day_18/day_18_input.txt', clip = False)
s, e = (0, 0), (num_row - 1, num_col - 1)

for i in range(len(bytes) - 1, 0, -1):
    grid = make_grid(num_row, num_col, bytes[:i])
    if dijkstra(grid, s, e, num_row, num_col) != float('inf'):
        y, x = bytes[i]
        print((x,y))
        break