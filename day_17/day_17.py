from enum import Enum


class Inst(Enum):
    ADV = 0
    BXL = 1
    BST = 2
    JNZ = 3
    BXC = 4
    OUT = 5
    BDV = 6
    CDV = 7


class State:
    def __init__(self, A, B, C, program):
        self.registers = [A, B, C]
        self.program = program
        self.inst_pt = 0
        self.outputs = []
        
    def get_inst(self):
        if self.inst_pt < len(self.program):
            # print("get_inst: Some")
            return self.program[self.inst_pt]
        else:
            # print("get_inst: None: {}: {}".format(self.inst_pt, len(self.program)))
            return None
        # return self.program[self.inst_pt] if self.inst_pt < len(self.program) else None
    
    def get_operand(self):
        return self.program[self.inst_pt + 1] if self.inst_pt < len(self.program) else None
    
    def combo(self, operand):
        if 0 <= operand <= 3:
            return operand
        elif operand == 4:
            return self.registers[0]
        elif operand == 5:
            return self.registers[1]
        elif operand == 6:
            return self.registers[2]
        
    def debug_print(self):
        print("[R] PT: {:<5} A: {:<10} B: {:<10} C: {:<10} OUT: {}".format(self.state.inst_pt,
                                                            self.state.registers[0], 
                                                            self.state.registers[1], 
                                                            self.state.registers[2], 
                                                            self.state.outputs))
        
    def run_inst(self, inst, operand):
        if inst == Inst.ADV.value:
            self.registers[0] = self.registers[0] // (2 ** self.combo(operand)) # A >> combo(operand)
            # print('ADV: A <- A // 2**{}'.format(self.combo(operand)))

        elif inst == Inst.BXL.value:
            self.registers[1] = self.registers[1] ^ operand
            # print('BXL: B <- B ^ {}'.format(operand))
            
        elif inst == Inst.BST.value:
            self.registers[1] = self.combo(operand) % 8
            # print('BST: B <- {} % 8'.format(self.combo(operand)))
            
        elif inst == Inst.JNZ.value:
            inst_pt_before = self.inst_pt
            if self.registers[0] != 0:
                self.inst_pt = operand - 2
            # print('JNZ: A: {}, PT: {} -> {}'.format(self.registers[0], inst_pt_before, operand))
                
        elif inst == Inst.BXC.value:
            self.registers[1] = self.registers[1] ^ self.registers[2]
            # print('BXC: B <- B ^ C')
            
        elif inst == Inst.OUT.value:
            self.outputs.append(self.combo(operand) % 8) # combo(operand) & 7
            # print('OUT: {} % 8'.format(self.combo(operand)))
            
        elif inst == Inst.BDV.value:
            self.registers[1] = self.registers[0] // (2 ** self.combo(operand))
            # print('BDV: B <- A // 2**{}'.format(self.combo(operand)))
            
        elif inst == Inst.CDV.value:
            self.registers[2] =  self.registers[0] // (2 ** self.combo(operand))
            # print('CDV: C <- A // 2 **{}'.format(self.combo(operand)))
            
        self.inst_pt += 2
        # self.debug_print()
    
    def run_program(self):
        while self.state.get_inst() is not None:
            inst = self.state.get_inst()
            operand = self.state.get_operand()
            self.state.run_inst(inst, operand)
        return self.state.output
            

with open('day_17/day_17_input.txt') as file:
    context = [line.strip() for line in file]
    
A, B, C = (int(item[12:]) for item in context[:3])
program = [int(x) for x in context[-1][9:].split(',')]


######################################## PART 1

# for a in range(32, 40, 1):
#     state = State(a, B, C, program)
#     print("[S] A: {}, B: {}, C: {}".format(A, B, C))
#     while state.get_inst() is not None:
#         inst = state.get_inst()
#         operand = state.get_operand()
#         state.run_inst(inst, operand)
        
#     print("[E] A: {}, B: {}, C: {}".format(state.registers[0], state.registers[1], state.registers[2]))
#     print(state.outputs)



######################################## PART 2
# for the loop to end, A has to be 0 after A // 8, A has to be in [0, 7]
# then multipy A by 8

def helper(start_a):
    
    print('\nSTART SEARCHING FROM {}'.format(start_a))

    for i in range(8):
        try_a = start_a + i

        state = State(try_a, B, C, program)
        
        while state.get_inst() is not None:
            inst = state.get_inst()
            operand = state.get_operand()
            state.run_inst(inst, operand)

        success = state.outputs == program[-len(state.outputs):]
        if success:
            # base case
            if state.outputs == program:
                return try_a
            else:
                print('[SUCCESS] i: {}, try_a: {}'.format(i, try_a))
                result = helper(try_a * 8)
                if result is not None:
                    return result

        else:
            print('[FAIL] i: {}, try_a: {}'.format(i, try_a))
            continue

    return None
    
    
print(helper(4))


# A = 0
# for i in reversed(range(n)):
#     A <<= 3
#     while run_program(A) != program[i:]:
#         A += 1

# return A