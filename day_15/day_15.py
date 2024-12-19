import sys
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parent.parent))

from collections import deque
import copy

from rsc.rsc import Reader, Matrix
from rsc.rsc import prettyprint


ARROWS = {
    '^': (-1, 0),
    '>': (0, 1),
    'v': (1, 0),
    '<': (0, -1)
}

REPLACE_MAP = {
        '#': '##',
        'O': '[]',
        '.': '..',
        '@': '@.'
        }


def is_moveable(grid, loc):
    return grid[loc[0]][loc[1]] == '.'


def is_box(grid, loc):
    return grid[loc[0]][loc[1]] in {'O', '[', ']'}
    
    
def is_wall(grid, loc):
    return grid[loc[0]][loc[1]] == '#'


def advanced_move(dir, grid, robot_pos):
    r, c = robot_pos
    dr, dc = ARROWS[dir]
    next_pos = (r, c)
    
    if is_moveable(grid, (r + dr, c + dc)):
        grid[r + dr][c + dc] = '@' # move
        grid[r][c] = '.' # reset
        next_pos = (r + dr, c + dc)
            
    elif is_box(grid, (r + dr, c + dc)):
        cannot_move = False
        boxes = get_boxes_to_move(dir, grid, robot_pos)
        # check the direction of pusing is not wall
        for box_pos in boxes:
            if is_wall(grid, (box_pos[0] + dr, box_pos[1] + dc)):
                cannot_move = True
                break
        if not cannot_move:
            # move all the boxes and the robot
            new_grid = copy.deepcopy(grid)
            # remove boxes
            for box_pos in boxes:
                new_grid[box_pos[0]][box_pos[1]] = '.'
            # place boxes
            for box_pos in boxes:
                new_grid[box_pos[0] + dr][box_pos[1] + dc] = grid[box_pos[0]][box_pos[1]]
            # move robot
            new_grid[r + dr][c + dc] = '@'
            new_grid[r][c] = '.'
            next_pos = (r + dr, c + dc)
            grid = new_grid
        
    return next_pos, grid
    
    
def default_move(dir, grid, robot_pos):
    r, c = robot_pos
    dr, dc = ARROWS[dir]
    next_pos = (r, c)
    
    if is_moveable(grid, (r + dr, c + dc)):
        grid[r + dr][c + dc] = '@' # move
        grid[r][c] = '.' # reset
        next_pos = (r + dr, c + dc)
        
    elif is_box(grid, (r + dr, c + dc)):
        # look for the first occurence of . in the same dir
        i = 1
        cannot_move = False
        while not is_moveable(grid, (r + i * dr, c + i * dc)):
            if is_wall(grid, (r + i * dr, c + i * dc)):
                cannot_move = True
                break
            i += 1 
        # if box(es) can be moved move the box
        if not cannot_move:
            # grid[r + i * dr][c + i * dc] = 'O'
            for k in range(i, 0, -1):
                    grid[r + k * dr][c + k * dc] = grid[r + (k - 1) * dr][c + (k - 1)* dc]
            grid[r + dr][c + dc] = '@'
            grid[r][c] = '.'
            next_pos = (r + dr, c + dc)
        
    return next_pos, grid


def get_boxes_to_move(dir, grid, robot_pos):
    boxes = set()
    start = (robot_pos[0] + ARROWS[dir][0], robot_pos[1] + ARROWS[dir][1])
    queue = deque([start])
    
    if grid[start[0]][start[1]] == ']':
        queue.append((start[0], start[1] - 1)) # '['
    else:
        queue.append((start[0], start[1] + 1)) # ']'

    while queue:
        curr_pos = queue.popleft()
        boxes.add(curr_pos)
        r, c = curr_pos
        if dir == '^':
            if grid[r - 1][c] == ']':
                queue.append((r - 1, c))
                if (r - 1, c - 1) not in queue:
                    queue.append((r - 1, c - 1))
            elif grid[r - 1][c] == '[':
                queue.append((r - 1, c))
                if (r - 1, c + 1) not in queue:
                    queue.append((r - 1, c + 1))
        elif dir == 'v':
            if grid[r + 1][c] == ']':
                queue.append((r + 1, c))
                if (r + 1, c - 1) not in queue:
                    queue.append((r + 1, c - 1))
            elif grid[r + 1][c] == '[':
                queue.append((r + 1, c))
                if (r + 1, c + 1) not in queue:
                    queue.append((r + 1, c + 1))
    return boxes


def get_gps_coor(grid) -> int:
    boxes = {'O', '['}
    gps_coor = 0
    for r in range(len(grid)):
        for c in range(len(grid[0])):
            if grid[r][c] in boxes:
                gps_coor += r * 100 + c
    return gps_coor


def run(option='part_1'):
    input_reader = Reader('day_15/day_15_input.txt')
    grid_str, inst_str = input_reader.get_item()
    inst = inst_str.replace('\n', '')
    if option == 'part_2':
        for char in REPLACE_MAP:
            grid_str = grid_str.replace(char, REPLACE_MAP[char])
        
    grid_builder = Matrix(grid_str)
    grid = grid_builder.to_list()
    robot_pos = grid_builder.get_loc('@')

    for dir in list(inst):
        # print(dir)
        if dir in {'<', '>'}:
            next_pos, new_grid = default_move(dir, grid, robot_pos)
        else:
            if option == 'part_2':
                next_pos, new_grid = advanced_move(dir, grid, robot_pos)
            else:
                next_pos, new_grid = default_move(dir, grid, robot_pos)
        # prettyprint(new_grid)
        robot_pos, grid = next_pos, new_grid
    print(get_gps_coor(grid))


if __name__ == '__main__':
    run()