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
