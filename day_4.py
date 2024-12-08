# Part 1

inputs = []
with open('day_4_input.txt') as file:
    for line in file:
        inputs.append([x for x in line.strip()])

num_rows, num_cols = len(inputs), len(inputs[0])

# S     S     S
#   A   A   A
#     M M M
# S A M X M A S
#     M M M
#   A   A   A
# S     S     S

# 0 < r - 3: SAMX vertical case
#   and 0 < c - 3: SAMX diagonal case (\) 
#   and c + 3 < num_cols: XMAS diagonal case (/)
# r + 3 < num_rows: XMAS vertical case
#   and c + 3 < num_cols: XMAS diagonal case(\)
#   and 0 < c - 3: SAMX diagonal case (/)

# 0 < c - 3: SAMX horizontal case
# c + 3 < num_cols: XMAS horizontal case
            
ans = 0
for r in range(num_rows):
    for c in range(num_cols):
        if inputs[r][c] == 'X':
            
            if 0 < r - 2:
                cond = inputs[r-3][c] == 'S' and inputs[r-2][c] == 'A' and inputs[r-1][c] == 'M'     
                if cond:
                    print("[row: {}][col: {}]".format(r, c))
                ans += 1 if cond else 0
                if  0 < c - 2:
                    cond = inputs[r-3][c-3] == 'S' and inputs[r-2][c-2] == 'A' and inputs[r-1][c-1] == 'M'
                    if cond:
                        print("[row: {}][col: {}]".format(r, c))
                    ans += 1 if cond else 0
                if c + 3 < num_cols:
                    cond = inputs[r-3][c+3] == 'S' and inputs[r-2][c+2] == 'A' and inputs[r-1][c+1] == 'M'
                    if cond:
                        print("[row: {}][col: {}]".format(r, c))
                    ans += 1 if cond else 0
                    
            if r + 3 < num_rows:
                cond = inputs[r+1][c] == 'M' and inputs[r+2][c] == 'A' and inputs[r+3][c] == 'S'
                if cond:
                    print("[row: {}][col: {}]".format(r, c))
                ans += 1 if cond else 0
                if c + 3 < num_cols:
                    cond = inputs[r+1][c+1] == 'M' and inputs[r+2][c+2] == 'A' and inputs[r+3][c+3] == 'S'
                    if cond:
                        print("[row: {}][col: {}]".format(r, c))
                    ans += 1 if cond else 0
                if 0 < c - 2:
                    cond = inputs[r+1][c-1] == 'M' and inputs[r+2][c-2] == 'A' and inputs[r+3][c-3] == 'S'
                    if cond:
                        print("[row: {}][col: {}]".format(r, c))
                    ans += 1 if cond else 0
            
            if 0 < c - 2:
                cond = inputs[r][c-1] == 'M' and inputs[r][c-2] == 'A' and inputs[r][c-3] == 'S'
                if cond:
                    print("[row: {}][col: {}]".format(r, c))
                ans += 1 if cond else 0
                
            if c + 3 < num_cols:
                cond = inputs[r][c+1] == 'M' and inputs[r][c+2] == 'A' and inputs[r][c+3] == 'S'
                if cond:
                    print("[row: {}][col: {}]".format(r, c))
                ans += 1 if cond else 0

print(ans) # 2567
                    
                    
# Part 2

# S   S 
#   A   
# M   M

ans = 0
for r in range(1, num_rows-1):
    for c in range(1, num_cols-1):
        if inputs[r][c] == 'A':
            cond_1 = (inputs[r-1][c-1] == 'S' and inputs[r+1][c+1] == 'M') or (inputs[r-1][c-1] == 'M' and inputs[r+1][c+1] == 'S')
            cond_2 = (inputs[r-1][c+1] == 'S' and inputs[r+1][c-1] == 'M') or (inputs[r-1][c+1] == 'M' and inputs[r+1][c-1] == 'S')
            if cond_1 and cond_2:
                print("[row: {}][col: {}]".format(r, c))
            ans += 1 if cond_1 and cond_2 else 0
            
print(ans) # 2029