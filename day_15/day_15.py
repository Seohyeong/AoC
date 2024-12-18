import sys
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parent.parent))

from collections import deque
import copy

from rsc.rsc import Reader, Matrix
from rsc.rsc import prettyprint

dr_and_dc = {
    '^': (-1, 0),
    '>': (0, 1),
    'v': (1, 0),
    '<': (0, -1)
}

def move(dir, grid, robot_pos):
    r, c = robot_pos
    dr, dc = dr_and_dc[dir]
    next_pos = (r, c)
    
    if grid[r + dr][c + dc] == '.':
        grid[r + dr][c + dc] = '@' # move
        grid[r][c] = '.' # reset
        next_pos = (r + dr, c + dc)
        
    elif grid[r + dr][c + dc] == 'O':
        # look for the first occurence of . in the same dir
        # (while loop, as soon as we see #, we stop)
        # place O at the location
        # move: grid[r + dr][c + dc] = '@'
        # reset: grid[r][c] = '.'
        i = 1
        cannot_move = False
        while grid[r + i * dr][c + i * dc] != '.':
            if grid[r + i * dr][c + i * dc] == '#':
                cannot_move = True
                break
            i += 1 
        if not cannot_move:
            grid[r + i * dr][c + i * dc] = 'O'
            grid[r + dr][c + dc] = '@'
            grid[r][c] = '.'
            next_pos = (r + dr, c + dc)
        
    return next_pos, grid


def get_boxes_to_move(dir, grid, robot_pos):
    boxes = set()
    start = (robot_pos[0] + dr_and_dc[dir][0], robot_pos[1] + dr_and_dc[dir][1])
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


def move_2(dir, grid, robot_pos):
    r, c = robot_pos
    dr, dc = dr_and_dc[dir]
    next_pos = (r, c)
    
    if grid[r + dr][c + dc] == '.':
        grid[r + dr][c + dc] = '@' # move
        grid[r][c] = '.' # reset
        next_pos = (r + dr, c + dc)
        
    elif grid[r + dr][c + dc] in {'[', ']'} :
        # left, right share the same logic
        if dir in {'<', '>'}:
            i = 1
            cannot_move = False
            while grid[r + i * dr][c + i * dc] != '.':
                if grid[r + i * dr][c + i * dc] == '#':
                    cannot_move = True
                    break
                i += 1 
            if not cannot_move:
                for k in range(i, 0, -1):
                    grid[r + k * dr][c + k * dc] = grid[r + (k - 1) * dr][c + (k - 1)* dc]
                # [r + dr][c + dc] -> [r + i * dr][c + i * dc]: shift
                # grid[r + i * dr][c + i * dc] = 'O'
                grid[r + dr][c + dc] = '@'
                grid[r][c] = '.'
                next_pos = (r + dr, c + dc)
        
        else:
            cannot_move = False
            boxes = get_boxes_to_move(dir, grid, robot_pos)
            # check the direction of pusing is not wall
            for box_pos in boxes:
                if grid[box_pos[0] + dr][box_pos[1] + dc] == '#':
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


def get_gps_coor(grid, option='part_1') -> int:
    gps_coor = 0
    for r in range(len(grid)):
        for c in range(len(grid[0])):
            if option == 'part_1':
                if grid[r][c] == 'O':
                    gps_coor += r * 100 + c
            elif option == 'part_2':
                if grid[r][c] == '[':
                    gps_coor += r * 100 + c
                    
    return gps_coor


def run_part_1():
    input_reader = Reader('day_15/day_15_input.txt')
    grid_str, inst_str = input_reader.get_item()
    inst = inst_str.replace('\n', '')

    grid_builder = Matrix(grid_str)
    grid = grid_builder.to_list()
    robot_pos = grid_builder.get_loc('@')

    for dir in list(inst):
        next_pos, new_grid = move(dir, grid, robot_pos)
        # prettyprint(new_grid)
        robot_pos, grid = next_pos, new_grid
        
    print(get_gps_coor(grid))


def run_part_2():
    replcae_map = {
        '#': '##',
        'O': '[]',
        '.': '..',
        '@': '@.'
        }

    input_reader = Reader('day_15/day_15_input.txt')
    grid_str, inst_str = input_reader.get_item()
    inst = inst_str.replace('\n', '')
    for char in replcae_map:
        grid_str = grid_str.replace(char, replcae_map[char])
        
    grid_builder = Matrix(grid_str)
    grid = grid_builder.to_list()
    prettyprint(grid)
    robot_pos = grid_builder.get_loc('@')

    for dir in list(inst):
        # print(dir)
        next_pos, new_grid = move_2(dir, grid, robot_pos)
        # prettyprint(new_grid)
        robot_pos, grid = next_pos, new_grid
        
    print(get_gps_coor(grid, option='part_2'))

           
run_part_2()