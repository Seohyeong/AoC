inputs = []
with open('day_7_input.txt') as file:
    for line in file:
        result, elements = line.strip().split(':')
        inputs.append([int(result)] + [int(e) for e in elements.strip().split(' ')])
    
    
def is_result_possible(idx, cal_so_far, op={'+', '*', '||'}):
    if cal_so_far > result:
        return False
    if idx >= len(elements):
        print("cal_so_far: ", cal_so_far)
        if cal_so_far == result:
            return True
        else:
            return False
    
    num = elements[idx]
    idx += 1
    
    print("result: {}, cal_so_far: {}, num: {}, idx: {}".format(result, cal_so_far, num, idx))
    
    if '||' in op:
        return (is_result_possible(idx, cal_so_far * num, op) or
                is_result_possible(idx, cal_so_far + num, op) or
                is_result_possible(idx, int(str(cal_so_far) + str(num)), op))
    else:
        return (is_result_possible(idx, cal_so_far * num, op) or
                is_result_possible(idx, cal_so_far + num, op))
    
    
count_possible, total_sum = 0, 0
for input in inputs:
    print('\ninput: {}'.format(input))
    result, elements = input[0], input[1:]
    idx = 1
    cal_so_far = input[1]
    if is_result_possible(idx, cal_so_far, op={'+', '*', '||'}):
        count_possible += 1
        total_sum += input[0]
        print('SUCCESS!')

print(count_possible)
print(total_sum) # 4364915411363, 38322057216320