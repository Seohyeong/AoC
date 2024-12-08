# Part 1
reports = []
with open('day_2_input.txt') as file:
    for line in file:
        l = line.strip().split(' ')
        l = [int(x) for x in l]
        reports.append(l)
        
        
def is_safe(report):
    
    if len(report) == 1:
        return True
    
    # set the monotonically increasing/decreasing flag
    if report[0] < report[1]:
        is_increasing = True
    elif report[0] > report[1]:
        is_increasing = False
    else:
        return False
    
    for idx in range(1, len(report)):
        diff = report[idx-1] - report[idx]
        if abs(diff) == 0 or abs(diff) > 3:
            return False
        else:
            curr_is_increasing = True if diff < 0 else False
            if is_increasing != curr_is_increasing:
                return False
    return True


count_safe = 0
for report in reports:
    count_safe += 1 if is_safe(report) else 0
    
print(count_safe) # 224


# Part 2
count_new_safe = 0
for report in reports:
    if is_safe(report):
        count_new_safe += 1
    else:
        if len(report) == 2:
            count_new_safe += 1
        else:
            for idx in range(len(report)):
                if is_safe(report[:idx] + report[idx+1:]):
                    count_new_safe += 1
                    break

print(count_new_safe)
