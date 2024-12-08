# Part 1
from collections import defaultdict

# build hash map for the ordering
# build two sets; one for numbers prior the anchor, one for numbers after the anchor

order_map = defaultdict(set)
seqs = []
is_first_part = True

with open('day_5_input.txt') as file:
    for line in file:
        if line == '\n':
            is_first_part = False
        else:
            if is_first_part:
                num_first, num_after = (int(x) for x in line.strip().split('|'))
                order_map[num_first].add(num_after)
            else:
                seq = [int(x) for x in line.strip().split(',')]
                seqs.append(seq)
            
def is_correct_order(seq):
    seen = set()
    for num in seq:
        for x in order_map[num]:
            if x in seen:
                return False
        seen.add(num)
    return True

sum_mid = 0
for seq in seqs:
    mid_idx = len(seq) // 2
    sum_mid += seq[mid_idx] if is_correct_order(seq) else 0

print(sum_mid) # 5275


# Part 2
def custom_sort(seq):
    for i in range(len(seq)-1, 1, -1):
        for j in range(i):
            if seq[j] in order_map[seq[j+1]]:
                tmp = seq[j]
                seq[j] = seq[j+1]
                seq[j+1] = tmp
    return seq

sum_mid = 0
for seq in seqs:
    if not is_correct_order(seq):
        mid_idx = len(seq) // 2
        sorted_seq = custom_sort(seq)
        sum_mid += seq[mid_idx]
        print('{} -> {}'.format(seq, sorted_seq))
        
print(sum_mid) # 6191