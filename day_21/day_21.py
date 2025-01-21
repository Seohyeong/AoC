
NUMPAD = {
    '7': (0, 0), '8': (0, 1), '9': (0, 2), 
    '4': (1, 0), '5': (1, 1), '6': (1, 2),
    '1': (2, 0), '2': (2, 1), '3': (2, 2),
    'X': (3, 0), '0': (3, 1), 'A': (3, 2)
    }

DIRPAD = {
    'X': (0, 0), '^': (0, 1), 'A': (0, 2), 
    '<': (1, 0), 'v': (1, 1), '>': (1, 2)
    }


MEMO = dict()
def memo(curr, dest, avoid, level):
    if (curr, dest, level) in MEMO:
        return MEMO[(curr, dest, level)]
    else:
        result = helper(curr, dest, avoid, level)
        MEMO[(curr, dest, level)] = result
        return result

def helper(curr: tuple[int, int], dest: tuple[int, int], avoid: tuple[int, int], level: int):
    curr_r, curr_c = curr
    dest_r, dest_c = dest
    avoid_r, avoid_c = avoid
    
    # basecase
    if level == 26:
        return 1
    
    # get possible sequences of curr -> dest
    left_right_moves = '>' * (dest_c - curr_c) if dest_c > curr_c else '<' * (curr_c - dest_c)
    up_down_moves = 'v'* (dest_r - curr_r) if dest_r > curr_r else '^' * (curr_r - dest_r)
    
    if curr_c == avoid_c and dest_r == avoid_r:
        seq = [left_right_moves + up_down_moves + 'A']
    elif dest_c == avoid_c and curr_r == avoid_r:
        seq = [up_down_moves + left_right_moves + 'A']
    else:
        seq = list(set([left_right_moves + up_down_moves + 'A', up_down_moves + left_right_moves + 'A']))
    
    # recursively cummulate the result
    result = float('inf')
    for path in seq:
        child_curr = DIRPAD['A']
        count = 0
        for char in path:
            # count += helper(child_curr, DIRPAD[char], DIRPAD['X'], level+1)
            count += memo(child_curr, DIRPAD[char], DIRPAD['X'], level+1)
            child_curr = DIRPAD[char]
        result = min(result, count)
    return result


with open('day_21/day_21_input.txt') as file:
    codes = [line.strip() for line in file]
    
ans = 0
for code in codes:
    prev = 'A'
    len_shortest_path = 0
    for char in code:
        len_shortest_path += helper(NUMPAD[prev], NUMPAD[char], NUMPAD['X'], 0)
        prev = char
    print(code, ': ', len_shortest_path)
    ans += int(code[:-1]) * len_shortest_path
print(ans)