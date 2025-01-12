    
def convert_to_heights(schematic):
    if schematic[-1] == '#####':
        schematic.reverse()
    
    pins = [0, 0, 0, 0, 0]
    for row_idx, row in enumerate(schematic):
        if row_idx != 0:
            for col_idx, item in enumerate(row):
                if item == '#':
                    pins[col_idx] += 1
    return pins
    
    
with open('day_25/day_25_input.txt') as file:
    context = [line.strip() for line in file]
    locks, keys, tmp = [], [], []
    for line in context:
        if line == '':
            if tmp[0] == '#####':
                locks.append(tmp)
            elif tmp[-1] == '#####':
                keys.append(tmp)
            tmp = []
        else:
            tmp.append(line)
    # append the last one
    if tmp[0] == '#####':
        locks.append(tmp)
    elif tmp[-1] == '#####':
        keys.append(tmp)
        
lock_pins = list(map(convert_to_heights, locks))
key_pins = list(map(convert_to_heights, keys))

num_possible = 0
for lock_pin in lock_pins:
    for key_pin in key_pins:
        lock_key_combined = [l + k for l, k in zip(lock_pin, key_pin)]
        num_possible += 1 if all([item <= 5 for item in lock_key_combined]) else 0

print(num_possible)