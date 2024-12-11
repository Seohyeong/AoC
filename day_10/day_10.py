from collections import defaultdict

trail_map = []
with open('day_10/day_10_input.txt') as file:
    for line in file:
        trail_map.append([x for x in line.strip()])

num_cols, num_rows = len(trail_map[0]), len(trail_map)


def get_trail_heads(trail_map):
    trail_heads = []
    for row in range(num_rows):
        for col in range(num_cols):
            if trail_map[row][col] == '0':
                trail_heads.append((row, col))
    return trail_heads

    
def get_next_steps(point: tuple[int, int]) -> list:
    row, col = point
    curr_height = int(trail_map[row][col])
    next_steps = []
    if row > 0:
        north = (row - 1, col) # north
        if trail_map[north[0]][north[1]] == str(curr_height + 1):
            next_steps.append(north)
    if row < num_rows - 1:
        south = (row + 1, col) # south
        if trail_map[south[0]][south[1]] == str(curr_height + 1):
            next_steps.append(south)
    if col > 0:
        west = (row, col - 1) # west
        if trail_map[west[0]][west[1]] == str(curr_height + 1):
            next_steps.append(west)
    if col < num_cols - 1:
        east = (row, col + 1) # east
        if trail_map[east[0]][east[1]] == str(curr_height + 1):
            next_steps.append(east)
    return next_steps


def walk(trail_head: tuple[int, int]) -> bool:
    global total_trail_tail
    global total_trails
    
    next_steps = get_next_steps(trail_head)
    if not next_steps:
        if trail_map[trail_head[0]][trail_head[1]] == '9':
            total_trail_tail.add(trail_head)
            total_trails += 1
    else:
        for next_step in next_steps:
            walk(next_step)


# Part 1: sum of the number of 9s reachable from each trailhead
# Part 2: sum of the number of unique paths for each trailhead
trail_heads = get_trail_heads(trail_map)
total_trail_tails = 0
total_trails = 0
for trail_head in trail_heads:
    total_trail_tail = set()
    walk(trail_head)
    total_trail_tails += len(total_trail_tail)
print(total_trail_tails) # Part 1
print(total_trails) # Part 2