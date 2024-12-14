
def parse(file_path: str) -> list[tuple[tuple[int, int]]]:
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
        claws.append((a_inst, b_inst, prize))
    return claws
    
claws = parse('day_13/day_13_ex.txt')

# given x_1(dx of machine a), x_2(dx of machine b)
# num_1 = prize_x // max(x_1, x_2), num_2 = 0, remainder = prize_x - (x_1 * num_1)
# while remainder !=0, decrease num_1 by 1 and increase num_2 by 1
# repeat with min(x_1, x_2), then it gives the range 


# if x_1 > x_2 -> min, if x_2 > x_1 -> max
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

for claw in claws:
    a_x, a_y = claw[0]
    b_x, b_y = claw[1]
    prize_x, prize_y = claw[2]

    range_x_1, range_x_2 = get_range(a_x, b_x, prize_x), get_range(b_x, a_x, prize_x)
    range_y_1, range_y_2 = get_range(a_y, b_y, prize_y), get_range(b_y, a_y, prize_y)

    if None in range_x_1 or None in range_x_2 or None in range_y_1 or None in range_y_2:
        print("NOT POSSIBLE")
        print('\n')
    else:
        possible_a_times = [max(min(range_x_1), min(range_y_1)), min(max(range_x_1), max(range_y_1))]
        possible_b_times = [max(min(range_x_2), min(range_y_2)), min(max(range_x_2), max(range_y_2))]

        print('machine a press times: {}'.format(possible_a_times))
        print('machine b press times: {}'.format(possible_b_times))
        print('\n')
