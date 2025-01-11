import copy

def run(vals: dict[str: int], insts: list[str]) -> dict[str: int]:
    insts_to_process = copy.deepcopy(insts)
    
    while insts_to_process:
        insts_tmp = []
        
        for inst in insts_to_process:
            wire_1, logic, wire_2, write_to = inst
            
            if wire_1 in vals and wire_2 in vals:
                if logic == 'AND':
                    vals[write_to] = vals[wire_1] and vals[wire_2]
                elif logic == 'OR':
                    vals[write_to] = vals[wire_1] or vals[wire_2]
                elif logic == 'XOR':
                    vals[write_to] = (vals[wire_1] or vals[wire_2]) and not (vals[wire_1] and vals[wire_2])
            
            else:
                insts_tmp.append(inst)
        
        insts_to_process = insts_tmp
                
    return vals

def construct_wires(vals, type='z') -> int:
    decimal_z_val = 0
    for k, v in vals.items():
        if k.startswith(type) and v == 1:
            decimal_z_val += 2 ** int(k[1:])
    return decimal_z_val

def decimal_to_binary(n): 
    return bin(n).replace("0b", "") 

def binary_to_decimal(n):
    return int(n,2)

with open('day_24/day_24_input.txt') as file:
    context = ''.join(line for line in file)
    init_vals, insts = context.split('\n\n')
    
    # initialization values
    init_vals = {line.split(': ')[0]: int(line.split(': ')[1]) for line in init_vals.split('\n')}

    # instructions
    insts = insts.split('\n')
    insts = [
        (read.split(' ') + [write]) 
        for line in insts 
        for read, write in [line.split(' -> ')]
    ]

# # PART 1
# vals = run(init_vals, insts)
# decimal_z = construct_wires(vals, type='z')
# print(decimal_z)


# PART 2
result_to_inst = dict()
inst_to_result = dict()
for inst in insts:
    result_to_inst[inst[-1]] = inst[:-1]
    inst_tuple = tuple(sorted(inst[:-1]))
    inst_to_result[inst_tuple] = inst[-1]


def get_gt_inst(i, result_to_inst, inst_to_result) -> tuple:
    # zn = (xn XOR yn) XOR [(xn-1 AND yn-1) OR (zn-1 >> AND)]
    xn = ('x0' + str(i)) if len(str(i)) == 1 else ('x' + str(i))
    yn = ('y0' + str(i)) if len(str(i)) == 1 else ('y' + str(i))
    xn_1 = ('x0' + str(i - 1)) if len(str(i - 1)) == 1 else ('x' + str(i - 1))
    yn_1 = ('y0' + str(i - 1)) if len(str(i - 1)) == 1 else ('y' + str(i - 1))
    zn_1 = ('z0' + str(i - 1)) if len(str(i - 1)) == 1 else ('z' + str(i - 1))
    
    first_part = inst_to_result[tuple(sorted([xn, 'XOR', yn]))]
    second_part = inst_to_result[tuple(sorted([xn_1, 'AND', yn_1]))]
    tmp = result_to_inst[zn_1]
    if 'XOR' in tmp:
        tmp.remove('XOR')
        tmp.append('AND')
    third_part = inst_to_result[tuple(sorted(tmp))]
    another_tmp = inst_to_result[tuple(sorted([second_part, 'OR', third_part]))]
    gt_inst = (first_part, 'XOR', another_tmp)
    return gt_inst


def build_inst_to_result(result_to_inst):
    inst_to_result = dict()
    for k, v in result_to_inst.items():
        inst_to_result[tuple(sorted(v))] = k
    return inst_to_result


def fix_result_to_inst(result_to_inst, o1, o2):
    new_result_to_inst = copy.deepcopy(result_to_inst)
    new_result_to_inst[o2] = result_to_inst[o1]
    new_result_to_inst[o1] = result_to_inst[o2]
    return new_result_to_inst
        

ANS = []
def fix_bit(i, result_to_inst, inst_to_result):
    new_result_to_inst = dict()
    new_inst_to_result = dict()
    
    current_z = ('z0' + str(i)) if len(str(i)) == 1 else ('z' + str(i))
    current_inst = tuple(result_to_inst[current_z])
    gt_inst = get_gt_inst(i, result_to_inst, inst_to_result)
    
    if set(current_inst) == set(gt_inst):
        new_result_to_inst = result_to_inst
        new_inst_to_result = inst_to_result
    else:
        U = set(current_inst).union(set(gt_inst))
        I = set(current_inst).intersection(set(gt_inst))
        output = list(U - I)
        
        # if all there is different are two logic gates, swap current_z with what gt_inst is
        if all([x in ('AND', 'XOR', 'OR') for x in output]):
            output = [current_z, inst_to_result[tuple(sorted(gt_inst))]]
            
        # if more than two wires are different, swap current_z with what gt_inst is
        elif len(output) != 2:
            output = [current_z, inst_to_result[tuple(sorted(gt_inst))]]
        
        # default: if two wires are different, swap two
        new_result_to_inst = fix_result_to_inst(result_to_inst, output[0], output[1])
        new_inst_to_result = build_inst_to_result(new_result_to_inst)

        ANS.extend(output)
            
    return new_result_to_inst, new_inst_to_result


for i in range(2, (len(init_vals) // 2)):
    result_to_inst, inst_to_result = fix_bit(i, result_to_inst, inst_to_result)
    
print(','.join(sorted(ANS)))