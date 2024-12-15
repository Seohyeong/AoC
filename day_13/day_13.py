def parse(file_path: str, inc=0) -> list[tuple[tuple[int, int]]]:
    claws = [] # list[tuple(int, int), tuple(int, int), tuple(int, int)]
    string = ''
    with open(file_path) as file:
        for line in file:
            string += line
    machines = string.split('\n\n')
    for mac in machines:
        instructions = mac.split('\n')
        a_inst = tuple(int(x[2:]) for x in instructions[0].split(':')[-1].strip().split(', '))
        b_inst = tuple(int(x[2:]) for x in instructions[1].split(':')[-1].strip().split(', '))
        prize = tuple(int(x[2:]) for x in instructions[2].split(':')[-1].strip().split(', '))
        prize = (inc + prize[0], inc + prize[1])
        claws.append((a_inst, b_inst, prize))
    return claws


def run_brute_force(claw, limit=None):
    tokens = dict()
    a_x, a_y = claw[0]
    b_x, b_y = claw[1]
    prize_x, prize_y = claw[2]
    # TODO: set custom min and max range
    if limit is not None:
        a_limit, b_limit = limit, limit
    for a_times in range(0, a_limit + 1):
        rmd_x = prize_x - (a_times * a_x)
        rmd_y = prize_y - (a_times * a_y)
        b_times = rmd_x / b_x
        if b_times <= b_limit and rmd_y / b_y == b_times:
            if b_times % 1 == 0:
                tokens[a_times * 3 + b_times] = (a_times, b_times)
    if tokens:
        min_cost = min(list(tokens.keys()))
        return tokens[min_cost]
    else:
        return (None, None)


def get_range(x_1, x_2, target):
    num_1 = target // x_1
    rmd = target % x_1
    num_2 = rmd // x_2
    rmd = rmd - (x_2 * num_2)
    while rmd != 0:
        if num_1 < 0:
            break
        num_1 -= 1
        rmd = rmd + x_1 + (x_2 * num_2) # from num_2 at the prev stage
        # print(rmd) 
        num_2 = rmd // x_2
        rmd = rmd - (x_2 * num_2)
        # print('num_1: {}, num_2: {}, x_1: {}, x_2: {}, rmd: {}'.format(num_1, num_2, x_1, x_2, rmd))
        assert num_1 * x_1 + num_2 * x_2 + rmd == target
    
    if num_1 * x_1 + num_2 * x_2 == target:
        range = (num_1, num_2)
    else:
        range = (None, None)
    return range


def get_intersect(range_1, range_2):
    if range_2[0] > range_1[1] or range_1[0] > range_2[1]:
        return (None, None)
    else:
        return (max(range_1[0], range_2[0]), max(range_1[1], range_2[1]))
    

# claws = parse('day_13/day_13_input.txt', inc=0)
# total_cost = 0
# for claw in claws:
#     a_x, a_y = claw[0]
#     b_x, b_y = claw[1]
#     prize_x, prize_y = claw[2]
    
#     ans_num_a, ans_num_b = run_brute_force(claw, limit=100)
#     if ans_num_a is not None and ans_num_b is not None:
#         total_cost += ans_num_a * 3 + ans_num_b
    
#     # range by x
#     num_a_1, num_b_1 = get_range(a_x, b_x, prize_x) 
#     num_b_2, num_a_2 = get_range(b_x, a_x, prize_x)
#     try:
#         num_a_range_by_x = (min(num_a_1, num_a_2), max(num_a_1, num_a_2))
#         num_b_range_by_x = (min(num_b_1, num_b_2), max(num_b_1, num_b_2))
#     except:
#         num_a_range_by_x = (None, None)
#         num_b_range_by_x = (None, None)
#     # range by y
#     num_b_1, num_a_1 = get_range(b_y, a_y, prize_y)
#     num_a_2, num_b_2 = get_range(a_y, b_y, prize_y)
#     try:
#         num_a_range_by_y = (min(num_a_1, num_a_2), max(num_a_1, num_a_2))
#         num_b_range_by_y = (min(num_b_1, num_b_2), max(num_b_1, num_b_2))
#     except:
#         num_a_range_by_y = (None, None)
#         num_b_range_by_y = (None, None)
    
#     # get the intersections
#     if None not in num_a_range_by_x and None not in num_a_range_by_y:
#         num_a_range = get_intersect(num_a_range_by_x, num_a_range_by_y)
#     else: 
#         num_a_range = (None, None)
#     if None not in num_b_range_by_x and None not in num_b_range_by_y:
#         num_b_range = get_intersect(num_b_range_by_x, num_b_range_by_y)
#     else:
#         num_b_range = (None, None)
    
#     print("num_a_range: ", num_a_range)
#     print("num_b_range: ", num_b_range)
#     if ans_num_a is not None and ans_num_b is not None:
#         assert num_a_range[0] <= ans_num_a <= num_a_range[1]
#         assert num_b_range[0] <= ans_num_b <= num_b_range[1]
#         print("[answer] A: {}, B: {}".format(int(ans_num_a), int(ans_num_b)))
#     else:
#         print("[answer] A: None, B: None")
#     print('\n')
    
# print("TOTAL COST: {}".format(total_cost))


total_cost = 0
claws = parse('day_13/day_13_input.txt', inc=10000000000000)
for claw in claws:
    ax, ay = claw[0]
    bx, by = claw[1]
    px, py = claw[2]
    det = ax * by - bx * ay
    if det != 0:
        na_multiples = by * px - bx * py
        nb_multiples = ax * py - ay * px
        if na_multiples % det == 0 and nb_multiples % det == 0:
            na = na_multiples // det
            nb = nb_multiples // det
            total_cost += 3 * na + nb

print(total_cost) # 99968222587852
