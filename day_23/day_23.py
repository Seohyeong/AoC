from collections import defaultdict
import copy
from tqdm import tqdm

connection = defaultdict(set)
with open('day_23/day_23_input.txt') as file:
    for line in file:
        pc_1, pc_2 = line.strip().split('-')
        connection[pc_1].add(pc_2)
        connection[pc_2].add(pc_1)
        
# PART 1
triples = set()

for pc, adj_pcs in connection.items():
    for adj_pc in adj_pcs:
        for another_pc in connection[adj_pc]:
            if another_pc in adj_pcs:
                triple = tuple(sorted([pc, adj_pc, another_pc]))
                if any([pc.startswith('t') for pc in triple]):
                    triples.add(triple)

print(len(triples))

# PART 2
groups = set()

for pc, adj_pcs in tqdm(connection.items(), total=len(connection)): 
    # init 
    if not groups:
        for adj_pc in adj_pcs:
            new_group = frozenset({pc, adj_pc})
            groups.add(new_group)
    else: 
        tmp_groups = set()
        # add to the existing group
        for group in groups:
            if group.issubset(adj_pcs):
                new_group = frozenset(list(group) + [pc])
            tmp_groups.add(new_group)
        for item in tmp_groups:
            groups.add(item)
        
        # create new group
        for adj_pc in adj_pcs:
            new_group = frozenset({pc, adj_pc})
            groups.add(new_group)
            
                
max_len, max_len_idx = 0, 0
for idx, group in enumerate(groups):
    if len(group) > max_len:
        max_len = len(group)
        max_len_idx = idx
        
print(','.join(sorted(list(groups)[max_len_idx])))