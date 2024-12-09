# Part 1
map_array = []
r, c = None, None
dir = 'UP'
with open('day_6_input.txt') as file:
    for row_num, line in enumerate(file):
        # does the guard always start heading north?
        if not r and not c:
            # get r
            if '^' in line:
                r = row_num
            # get c
            col_num = 0
            for char in line:
                if char == '^':
                    c = col_num
                    break
                col_num += 1
        l = [x for x in line.strip()]
        map_array.append(l)

num_total_rows, num_total_cols = len(map_array), len(map_array[0])

next_dir = {
    'UP': 'RIGHT',
    'RIGHT': 'DOWN',
    'DOWN': 'LEFT',
    'LEFT': 'UP'
}

next_diff = {
    'UP': (-1, 0),
    'RIGHT': (0, 1),
    'DOWN': (1, 0),
    'LEFT': (0, -1)
}

def run_part_1(r, c, dir):
    visited = set()
    visited.add((r, c)) # add starting location

    while True:
        new_r, new_c = r + next_diff[dir][0], c + next_diff[dir][1]
        if new_r < 0 or new_r > num_total_rows - 1 or new_c < 0 or new_c > num_total_cols - 1:
            break
        if map_array[new_r][new_c] == '#':
            dir = next_dir[dir]
        else:
            visited.add((new_r, new_c))
            r, c = new_r, new_c
    
    return visited

# visited = run_part_1(r, c, dir)
# print(len(visited)) # 5318

# Part 2
# if placing an obstacle makes the guard to visit the same location with the same direction as before
# given guard_r, guard_c, guard_dir and map_array, if there's a loop return true, else return false

def is_loop(r, c, dir, map_array):
    visited = set()
    visited.add((r, c, dir))

    while True:
        new_r, new_c = r + next_diff[dir][0], c + next_diff[dir][1]
        if new_r < 0 or new_r > num_total_rows - 1 or new_c < 0 or new_c > num_total_cols - 1:
            return False
        if map_array[new_r][new_c] == '#':
            dir = next_dir[dir]
        else:
            if (new_r, new_c, dir) in visited:
                return True
            visited.add((new_r, new_c, dir))
            r, c = new_r, new_c

obs = set()
org_r, org_c, org_dir = r, c, dir
visited = run_part_1(org_r, org_c, org_dir) # TODO: this part is recursive
for x, y in visited:
    if map_array[x][y] == '.':
        map_array[x][y] = '#'
        if is_loop(org_r, org_c, org_dir, map_array):
            obs.add((x, y))
        map_array[x][y] = '.'

print(len(obs)) # 1831
                
