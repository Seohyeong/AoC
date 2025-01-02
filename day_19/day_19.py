from collections import defaultdict

with open('day_19/day_19_input.txt') as file:
    lines = [line.strip() for line in file]

patterns = lines[0].split(', ')
designs = [list(d) for d in lines[2:]]

patterns_dict = defaultdict(list)
for p in patterns:
    patterns_dict[p[0]].append(p)
    
    
cache = dict()
def memo(design, pt):
    n = cache.get(''.join(design[pt:]), None)
    if n is not None:
        return n
    else:
        result = match_design_2(design, pt)
        cache[''.join(design[pt:])] = result
        return result
    
def match_design(design: list, pt: int):
    for pattern in patterns_dict[design[pt]]:
        if len(pattern) > len(design[pt:]):
            continue
        if pattern == ''.join(design[pt:pt+len(pattern)]):
            new_pt =  pt + len(pattern)
            if new_pt == len(design):
                return True
            else:
                result = memo(design, new_pt)
                if result:
                    return result
    return False

def match_design_2(design: list, pt: int):
    count = 0
    for pattern in patterns_dict[design[pt]]:
        if len(pattern) > len(design[pt:]):
            continue
        if pattern == ''.join(design[pt:pt+len(pattern)]):
            new_pt =  pt + len(pattern)
            if new_pt == len(design):
                count = count + 1
            else:
                count = count + memo(design, new_pt)
    return count
        

count = 0
total_matches = 0
for d in designs:
    matches = memo(d, 0)
    if matches > 0:
        count += 1
        total_matches += matches
    
print(count)
print(total_matches)