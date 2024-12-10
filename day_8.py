from collections import defaultdict

antennas = defaultdict(list)
total_antenna_locs = set() # 242
with open('day_8_input.txt') as file:
    y = 0
    for line in file:
        x = 0
        for char in line.strip():
            if char != '.':
                antennas[char].append((x, y))
                total_antenna_locs.add((x, y))
            x += 1
        y -= 1
    y_range = y
    x_range = x
        
        
def is_in_range(loc: tuple[int, int]) -> bool:
    x, y = loc
    return 0 <= x < x_range and y_range < y <= 0


def get_antinode(loc_1: tuple[int, int], loc_2: tuple[int, int]) -> tuple[int, int]:
    dx, dy = loc_2[0] - loc_1[0], loc_2[1] - loc_1[1]
    antinode = (loc_2[0] + dx, loc_2[1] + dy)
    if is_in_range(antinode):
        antinodes.add(antinode)
        if FLAG_RESONANCE:
            get_antinode(loc_2, antinode)


antinodes = set()
FLAG_RESONANCE = True
for antenna_type, locs in antennas.items():
    for i in range(len(locs)):
        for j in range(i+1, len(locs)):
            get_antinode(locs[i], locs[j])
            get_antinode(locs[j], locs[i])
                

antinodes.update(total_antenna_locs)
print(len(antinodes))
