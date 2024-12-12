from collections import defaultdict

stone_to_cnt = defaultdict(int)
with open('day_11/day_11_input.txt') as file:
    for line in file:
        for x in line.strip().split(' '):
            stone_to_cnt[int(x)] += 1

memo = {0: [1]}
def blink(stone_to_cnt: dict[int: int]) -> dict[int: int]:
    next_stone_to_cnt = defaultdict(int)
    for stone, cnt in stone_to_cnt.items():
        if stone in memo:
            for next_stone in memo[stone]:
                next_stone_to_cnt[next_stone] += cnt
        else:
            if len(str(stone)) % 2 == 0:
                len_stone = len(str(stone))
                first_half, second_half = str(stone)[:len_stone//2], str(stone)[len_stone//2:]
                next_stone_to_cnt[int(first_half)] += cnt
                next_stone_to_cnt[int(second_half)] += cnt
                memo[stone] = [int(first_half), int(second_half)]
            else:
                next_stone_to_cnt[stone * 2024] += cnt
                memo[stone] = [stone * 2024]
    return next_stone_to_cnt

num_blinks = 75
for i in range(num_blinks):
    stone_to_cnt = blink(stone_to_cnt)
print(sum(stone_to_cnt.values())) # 182081, 216318908621637
