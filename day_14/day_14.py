import matplotlib.pyplot as plt
import numpy as np

def parse(file_path):
    with open(file_path) as file:
        robots = []
        for line in file:
            p, v = line.strip().split(' ')
            px, py = [int(x) for x in p[2:].split(',')]
            vx, vy = [int(x) for x in v[2:].split(',')]
            robots.append(((px, py), (vx, vy)))
    return robots
    

def to_grid(robots, tile_dim):
    wide, tall = tile_dim
    grid = [[0] * wide for _ in range(tall)] # [[v]*n]*n is a trap
    for robot in robots:
        px, py = robot[0]
        grid[py][px] += 1
    return grid


def to_img_array(grid):
    w, h = len(grid[0]), len(grid)
    # img_array dim: [h, w, d]
    img_array = np.zeros((h, w, 3))
    for i in range(h):
        for j in range(w):
            val = grid[i][j]
            if val > 0:
                img_array[i, j, :] = [255, 255, 255]
    return img_array    
    
    
def vis(robots: list[tuple[tuple[int, int]]], tile_dim:tuple[int, int]):
    wide, tall = tile_dim
    grid = [[0] * wide for _ in range(tall)] # [[v]*n]*n is a trap
    for robot in robots:
        px, py = robot[0]
        grid[py][px] += 1
    for line in grid:
        string = ''
        for item in line:
            if item == 0:
                string += '⬛'
            else:
                string += '⬜'
        print(string)
    print('\n')
    
    
def after_n_step(robots: list[tuple[tuple[int, int]]], n_step: int, tile_dim: tuple[int, int]):
    new_robots = []
    for robot in robots:
        px, py = robot[0]
        vx, vy = robot[1]
        wide, tall = tile_dim
        new_px = (px + n_step * vx) % wide
        new_py = (py + n_step * vy) % tall
        new_robots.append(((new_px, new_py), robot[1]))
    return new_robots


def after_one_step(robots: list[tuple[tuple[int, int]]], tile_dim: tuple[int, int]):
    new_robots = []
    for robot in robots:
        px, py = robot[0]
        vx, vy = robot[1]
        wide, tall = tile_dim
        new_px = (px + vx) % wide
        new_py = (py + vy) % tall
        new_robots.append(((new_px, new_py), robot[1]))
    return new_robots
    

def get_safety_factor(robots, tile_dim) -> int:
    quadrants = [0, 0, 0, 0]
    
    wide, tall = tile_dim
    ignore_x = wide // 2
    ignore_y = tall // 2
    
    for robot in robots:
        px, py = robot[0]
        if px < ignore_x and py < ignore_y:
            quadrants[0] += 1
        elif px > ignore_x and py < ignore_y:
            quadrants[1] += 1
        elif px < ignore_x and py > ignore_y:
            quadrants[2] += 1
        elif px > ignore_x and py > ignore_y:
            quadrants[3] += 1
    sf = 1
    for q in quadrants:
        sf *= q
    return sf


def does_straight_line_exist(grid: list[list[int]], target_len: int) -> bool:
    for row in grid:
        line_len = 0
        for item in row:
            if item != 0:
                line_len += 1
                if line_len >= target_len:
                    return True
            else:
                line_len = 0
    return False
        

# Part 1
robots = parse('day_14/day_14_input.txt')
tile_dim = (101, 103)
robots = after_n_step(robots, 100, tile_dim)
print(get_safety_factor(robots, tile_dim))


# Part 2
robots = parse('day_14/day_14_input.txt')
tile_dim = (101, 103)

i = 0
while True:
    i += 1
    robots = after_one_step(robots, tile_dim)
    grid = to_grid(robots, tile_dim)
    if does_straight_line_exist(grid, target_len=20):
        break
print(i)

img_array = to_img_array(grid)
plt.imshow(img_array, aspect='auto')
plt.show()