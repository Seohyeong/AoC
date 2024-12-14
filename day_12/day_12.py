from collections import deque

garden = []
with open('day_12/day_12_input.txt') as file:
    for line in file:
        garden.append([x for x in line.strip()])
        
num_rows, num_cols = len(garden), len(garden[0])
all_plots = set()
for r in range(num_rows):
    for c in range(num_cols):
        all_plots.add((r, c))
    
    
def get_adj_plots(loc: tuple[int, int]) -> list[tuple[int, int]]:
    adj_plots = []
    row, col = loc[0], loc[1]
    veggie_type = garden[row][col]
    if row > 0:
        north = (row - 1, col) # north
        if garden[north[0]][north[1]] == veggie_type:
            adj_plots.append(north)
    if row < num_rows - 1:
        south = (row + 1, col) # south
        if garden[south[0]][south[1]] == veggie_type:
            adj_plots.append(south)
    if col > 0:
        west = (row, col - 1) # west
        if garden[west[0]][west[1]] == veggie_type:
            adj_plots.append(west)
    if col < num_cols - 1:
        east = (row, col + 1) # east
        if garden[east[0]][east[1]] == veggie_type:
            adj_plots.append(east)
    return adj_plots


def traverse(loc: tuple[int, int]):
    queue = deque([loc])
    while queue:
        curr_loc = queue.popleft()
        # remove from all_plots
        all_plots.remove(curr_loc)
        # log the area
        veggie_area.add(curr_loc)
        adj_plots = get_adj_plots(curr_loc)
        for loc in adj_plots:
            # if haven't been visited and not in the queue (TODO: better way?)
            if loc not in veggie_area and loc not in queue:
                queue.append(loc)
        

def get_perimeter(locs: set[tuple[int, int]]) -> int:
    perimeter = 0
    for loc in locs:
        perimeter += 4
        if (loc[0] - 1, loc[1]) in locs:
            perimeter -= 1
        if (loc[0] + 1, loc[1]) in locs:
            perimeter -= 1
        if (loc[0], loc[1] - 1) in locs:
            perimeter -= 1
        if (loc[0], loc[1] + 1) in locs:
            perimeter -= 1
    return perimeter
        

def get_num_sides(locs: set[tuple[int, int]]) -> int:
    rows = [x[0] for x in list(locs)]
    cols = [x[1] for x in list(locs)]
    min_r, max_r, min_c, max_c = min(rows), max(rows), min(cols), max(cols)
    
    total_lines = 0
    
    # count horizontal lines
    new_seg = True
    for r in range(min_r, max_r + 2):
        num_lines_per_row = 0
        prev_up = None
        for c in range(min_c, max_c + 2):
            up = (r - 1, c) in locs if (0 <= r - 1 < num_rows and 0 <= c < num_cols) else False
            yourself = (r, c) in locs if (0 <= r < num_rows and 0 <= c < num_cols) else False
            if up != yourself: # if either exists
                # up and not yourself -> not up and yourself: need to be counted
                if prev_up is not None and prev_up != up:
                    new_seg = True
                if new_seg:
                    num_lines_per_row += 1
                new_seg = False
            else: # if inside the shape or there is a gap
                new_seg = True
            prev_up = up
        total_lines += num_lines_per_row
    total_hrz_lines = total_lines
    print("total horizontal lines: {}".format(total_hrz_lines))
    
    # count vertical lines
    new_seg = True
    for c in range(min_c, max_c + 2):
        num_lines_per_row = 0
        prev_left = None
        for r in range(min_r, max_r + 2):
            left = (r, c - 1) in locs if (0 <= r < num_rows and 0 <= c - 1 < num_cols) else False
            yourself = (r, c) in locs if (0 <= r < num_rows and 0 <= c < num_cols) else False
            if left != yourself: # if either exists
                if prev_left is not None and prev_left != left:
                    new_seg = True
                if new_seg:
                    num_lines_per_row += 1
                new_seg = False
            else: # if inside the shape or there is a gap
                new_seg = True
            prev_left = left
        total_lines += num_lines_per_row
    total_vtc_lines = total_lines - total_hrz_lines
    print("total vertical lines: {}".format(total_vtc_lines))
    
    return total_lines
    
    
veggie_areas = [] # list of sets
while all_plots:
    veggie_area = set()
    traverse(list(all_plots)[0])
    veggie_areas.append(veggie_area)

cost = 0
for areas in veggie_areas:
    veggie = garden[list(areas)[0][0]][list(areas)[0][1]]
    area = len(areas)
    # perimeter = get_perimeter(areas)
    num_sides = get_num_sides(areas)
    # cost += area * perimeter
    cost += area * num_sides
    print("{} AREA: {}, SIDES: {}, COST: {}".format(veggie, area, num_sides, area * num_sides))

        
print("TOTAL COST: {}".format(cost)) # 953738
