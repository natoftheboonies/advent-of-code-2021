from aoc import readinput

from pprint import pprint

sample = """00100
11110
10110
10111
10101
01111
00111
11100
10000
11001
00010
01010""".splitlines()

puzzle = [line.strip() for line in sample]

puzzle = readinput(3)

# turn into 2d array of ints
grid = list()
for line in puzzle:
    row = tuple(int(c) for c in line)
    grid.append(row)

tipped = list(zip(*grid[::-1]))

#pprint(tipped)

def max_bin(row):
    return 1 if row.count(1) >= row.count(0) else 0

maxes = mins = ''

for row in tipped:
    maxes += '0' if row.count(0) > row.count(1) else '1'
    mins += '1' if row.count(0) > row.count(1) else '0'

#print(maxes, mins)
print("#1", int(maxes,2)*int(mins,2))

def filter_oxygen(rows, target):
    print("recurse", rows[0], len(rows))
    if len(rows) == 1:
        return rows[0]
    filtered = list()
    for row in rows:
        if row[0]==target:
            filtered.append(row[1:])

    if len(filtered[0])==0:
        return [target]
    new_target = max_bin([row[0] for row in filtered])
    
    return [target] + filter_oxygen(filtered, new_target)


def filter_co2(rows, target):
    print("recurse", rows[0], len(rows))
    if len(rows) == 1:
        return list(rows[0])
    filtered = list()
    for row in rows:
        if row[0]==target:
            filtered.append(row[1:])

    if len(filtered[0])==0:
        return [target]
    new_target = (max_bin([row[0] for row in filtered])+1)%2
    
    return [target] + filter_co2(filtered, new_target)


oxygen = filter_oxygen(grid, int(maxes[0]))

print(oxygen)

co2 = filter_co2(grid, int(mins[0]))

print(co2)

oxy_rating = int(''.join([str(x) for x in oxygen]),2)
co2_rating = int(''.join([str(x) for x in co2]),2)

print("#2",oxy_rating*co2_rating)

