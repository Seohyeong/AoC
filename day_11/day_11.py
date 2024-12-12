from tqdm import tqdm

with open('day_11/day_11_input.txt') as file:
    for line in file:
        stones = [int(x) for x in line.strip().split(' ')]

memo = {0: [1]}
def blink(stones: list[int]) -> list[int]:  
    next_stones = []
    for idx, s in enumerate(stones):
        if s in memo:
            next_stones.extend(memo[s])
        else:
            if len(str(s)) % 2 == 0:
                len_stone = len(str(s))
                first_half, second_half = str(s)[:len_stone//2], str(s)[len_stone//2:]
                next_stones.append(int(first_half))
                next_stones.append(int(second_half))
                memo[s] = [int(first_half), int(second_half)]
            else:
                next_stones.append(stones[idx] * 2024)
                memo[s] = [stones[idx] * 2024]
    return next_stones

num_blinks = 25
print(stones)
for i in tqdm(range(num_blinks), total = num_blinks):
    stones = blink(stones)
    # print(stones)
print(len(stones)) # 182081