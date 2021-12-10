from aoc import readinput

depths = [int(depth) for depth in readinput(1)]

count_increasing = 0
last = depths[0]
for depth in depths[1:]:
    if depth > last:
        count_increasing += 1
    last = depth

print("#1", count_increasing)

count_increasing = 0
last = depths[:3]
for depth in depths[3:]:
    last_sum = sum(last)
    last = last[1:] + [depth]
    if sum(last) > last_sum:
        count_increasing += 1

print("#2", count_increasing)
