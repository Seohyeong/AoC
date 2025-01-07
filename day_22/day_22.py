from collections import defaultdict
from tqdm import tqdm

def mix(next_num, num):
    return num ^ next_num

def prune(num):
    return num % 16777216

cache = defaultdict(int)
def get_nth_num(num: int, n: int) -> int:
    for _ in range(n):
        if num in cache:
            num = cache[num]
        else:
            next_num = prune(mix(num * 64, num))
            next_num = prune(mix(next_num // 32, next_num))
            next_num = prune(mix(next_num * 2048, next_num))
            cache[num] = next_num
            num = next_num
    return num

def get_price_changes(num: int, n: int) -> list[int]:
    
    def get_last_digit(num):
        return int(str(num)[-1])
    
    price_changes = [0]
    prices = [get_last_digit(num)]
    
    for _ in range(n):
        if num in cache:
            num = cache[num]
        else:
            next_num = prune(mix(num * 64, num))
            next_num = prune(mix(next_num // 32, next_num))
            next_num = prune(mix(next_num * 2048, next_num))
            cache[num] = next_num
            num = next_num
        price_changes.append(get_last_digit(num) - prices[-1])
        prices.append(get_last_digit(num))
    return prices, price_changes
    
    
with open('day_22/day_22_input.txt') as file:
    initial_nums = [int(line.strip()) for line in file]
    

# # Part 1
# sum_secret_nums = 0
# for num in initial_nums:
#     new_secret_num = get_nth_num(num, 2000)
#     sum_secret_nums += new_secret_num
#     print('{} -> {}'.format(num, new_secret_num))
# print(sum_secret_nums)
    
# Part 2
seq_caches = []
for num in initial_nums:
    tmp_cache = set()
    seq_cache = defaultdict(int)
    prices, price_changes = get_price_changes(num, 2000)
    for i in range(1, len(price_changes) - 3):
        if tuple(price_changes[i:i+4]) not in tmp_cache:
            seq_cache[tuple(price_changes[i:i+4])] = prices[i+3]
            tmp_cache.add(tuple(price_changes[i:i+4]))
    seq_caches.append(seq_cache)
    # print('\ninitial num: {}'.format(num))
    # print('prices: {}'.format(prices))
    # print('del prices: {}'.format(price_changes))

max_price = 0
processed = set()
for seq_cache in tqdm(seq_caches, total = len(seq_caches)):
    for seq, price in seq_cache.items():
        if seq not in processed:
            total_price = sum([seq_cache[seq] for seq_cache in seq_caches])
            if total_price > max_price:
                max_price = total_price
                max_seq = seq
            processed.add(seq)

print(max_price)
print(max_seq)