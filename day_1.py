# Part 1
array_1 = []
array_2 = []

with open('day_1_input.txt') as file:
    for line in file:
        loc_1, loc_2 = line.strip().split('   ')
        array_1.append(int(loc_1))
        array_2.append(int(loc_2))

array_1.sort()
array_2.sort()

ans = 0
for loc_1, loc_2 in zip(array_1, array_2):
    ans += abs(loc_1 - loc_2)
    
print(ans) # 2378066


# Part 2
from collections import Counter

sim_score = 0
counter = Counter(array_2)
for loc_1 in array_1:
    sim_score += loc_1 * counter[loc_1]
    
print(sim_score) # 18934359