with open('day_9_input.txt') as file:
    for line in file:
        disk_map = line.strip()


def convert(disk_map: str) -> list:
    file_system = []
    disk_id = 0
    is_file = True
    for idx in range(len(disk_map)):
        if is_file:
            file_system += [disk_id] * int(disk_map[idx])
            disk_id += 1
            is_file = False
        else:
            file_system += ['.'] * int(disk_map[idx])
            is_file = True
    return file_system


def move(file_system: list) -> list:
    left = 0
    while file_system[left] != '.':
        left += 1

    right = len(file_system) - 1
    while right == '.':
        right -= 1
        
    while left < right:
        file_system[left] = file_system[right]
        file_system[right] = '.'
        print(''.join([str(x) for x in file_system]))
    
        while file_system[left] != '.':
            left += 1
        while file_system[right] == '.':
            right -= 1
    return file_system


def get_check_sum(file_system: list) -> int:
    check_sum = 0
    for idx, item in enumerate(file_system):
        if item != '.': 
            check_sum += item * idx
    return check_sum


# 2333133121414131402
# [(0, 2), (None, 3), (1, 3), (None, 3), (2, 1), (None, 3), (3, 3), (None, 1), ..., (9, 2)]

def convert_2(disk_map: str) -> list[tuple]:
    file_system = []
    disk_id = 0
    is_file = True
    for char in disk_map:
        if is_file:
            file_system.append((disk_id, int(char)))
            disk_id += 1
            is_file = False
        else:
            if int(char) != 0:
                file_system.append((None, int(char)))
            is_file = True
    return file_system


def move_2(file_system: list[tuple], empty_idx, file_idx) -> tuple[list[tuple], bool]:

    while file_system[empty_idx][1] < file_system[file_idx][1] or file_system[empty_idx][0] is not None:
        # no large enough empty space found
        if empty_idx > file_idx:
            return (file_system, False)
        empty_idx += 1

    # empty space found
    if empty_idx < file_idx:
        if file_system[empty_idx][1] - file_system[file_idx][1] == 0:
            file_system[empty_idx], file_system[file_idx] = file_system[file_idx], file_system[empty_idx]
            flag = False
        else:
            new_file = (file_system[file_idx][0], file_system[file_idx][1])
            left_space = (None, file_system[empty_idx][1] - file_system[file_idx][1])

            file_system[file_idx] = (None, file_system[file_idx][1]) # file moves to empty_idx 
            
            file_system = file_system[:empty_idx] + \
                            [new_file, left_space] + \
                            file_system[empty_idx + 1:]
            flag = True
    else:
        flag = False
    return (file_system, flag)


file_system = convert_2(disk_map)

# get last file_idx
file_idx = len(file_system) - 1
while file_system[file_idx][0] is None:
    file_idx -= 1

# get first empty_idx
empty_idx = 0
while file_system[empty_idx][0] is not None:
    empty_idx += 1
    
while file_idx > -1:
    if file_system[file_idx][0] is not None:
        file_system, flag = move_2(file_system, empty_idx, file_idx)
        if not flag:
            file_idx -= 1
    else:
        file_idx -= 1

tmp = []
for i, j in file_system:
    if i is not None:
        tmp += [i] * j
    else:
        tmp += ['.'] * j
        
check_sum = get_check_sum(tmp)
print(check_sum) # 6488291456470


# 00...111...2...333.44.5555.6666.777.888899
# 0099.111...2...333.44.5555.6666.777.8888..
# 0099.1117772...333.44.5555.6666.....8888..
# 0099.111777244.333....5555.6666.....8888..
# 00992111777.44.333....5555.6666.....8888..

# 00...111...2...333.44.5555.6666.777.888899
# 0099.111...2...333.44.5555.6666.777.8888..
# 0099.1117772...333.44.5555.6666.....8888..
# 0099.111777244.333....5555.6666.....8888..
# 00992111777.44.333....5555.6666.....8888..