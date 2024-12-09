from collections import deque
import copy

input = dict()
with open('day_7_input.txt') as file:
    for line in file:
        result, elements = line.strip().split(':')
        elements = [int(e) for e in elements.strip().split(' ')]
        input[int(result)] = elements
        
    
def is_result_possible(result, queue, cal_so_far):
    if cal_so_far > result:
        return False
    if not queue:
        print("cal_so_far: ", cal_so_far)
        if cal_so_far == result:
            return True
        else:
            return False
    
    num = queue.popleft()
    
    print("cal_so_far: {}, num: {}, queue: {}".format(cal_so_far, num, queue))
    
    return (is_result_possible(result, copy.deepcopy(queue), cal_so_far * num) or 
            is_result_possible(result, copy.deepcopy(queue), cal_so_far + num))
    
ans = 0
sum_results = 0
for result, elements in input.items():
    print('\n')
    print('result: {}, queue: {}'.format(result, elements))
    queue = deque(elements)
    cal_so_far = queue.popleft()
    if is_result_possible(result, queue, cal_so_far):
        print("POSSIBLE!")
        ans += 1
        sum_results += result

print(sum_results) # 4364915411238