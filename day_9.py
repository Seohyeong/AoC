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
            file_system += [None] * int(disk_map[idx])
            is_file = True
    return file_system


def move(file_system: list) -> list:
    left = 0
    while file_system[left] is not None:
        left += 1

    right = len(file_system) - 1
    while right is None:
        right -= 1
        
    while left < right:
        file_system[left] = file_system[right]
        file_system[right] = None
        
        while file_system[left] is not None:
            left += 1
        while file_system[right] is None:
            right -= 1
    return file_system
    

def get_check_sum(file_system: list) -> int:
    check_sum = 0
    for idx, item in enumerate(file_system):
        if item is not None: 
            check_sum += item * idx
    return check_sum


file_system = convert(disk_map)
file_system = move(file_system)
check_sum = get_check_sum(file_system)

print(check_sum) 
# 92092395920 too low
# 6461289671426
