# Part 1
import re

string = ''
with open('day_3_input.txt') as file:
    for line in file:
        string += line
    
pattern = r'mul\([0-9]+,[0-9]+\)'
match = re.findall(pattern, string)

ans = 0
for mul in match:
    nums = mul[4:-1].split(',')
    ans += int(nums[0]) * int(nums[1])
    
print(ans) # 165225049


# Part 2
new_pattern = r'(mul\([0-9]+,[0-9]+\))|(do\(\))|(don\'t\(\))'
new_match = re.findall(new_pattern, string)

new_ans = 0
flag = True

for mul in new_match:
    if mul[1] == "do()":
        flag = True
    elif mul[2] == "don't()":
        flag = False
    else:
        if flag:
            nums = mul[0][4:-1].split(',')
            new_ans += int(nums[0]) * int(nums[1])
    
print(new_ans) # 108830766
        
    
