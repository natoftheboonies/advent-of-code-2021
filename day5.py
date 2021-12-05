from aoc import readinput
import re

puzzle = """0,9 -> 5,9
8,0 -> 0,8
9,4 -> 3,4
2,2 -> 2,1
7,0 -> 7,4
6,4 -> 2,0
0,9 -> 2,9
3,4 -> 1,4
0,0 -> 8,8
5,5 -> 8,2""".splitlines()

puzzle = readinput(5)

grid = dict()
for line in puzzle:
    x1, y1, x2, y2 = [int(d) for d in re.findall(r"\d+",line)]
    if x1==x2 or y1==y2:
        #print(x1,y1,x2,y2)
        x_min = min(x1, x2)
        x_max = max(x1, x2)
        y_min = min(y1, y2)
        y_max = max(y1, y2)
        for x in range(x_min,x_max+1):
            for y in range(y_min,y_max+1):
                #print("p",x,y)
                grid[(x,y)] = grid.get((x,y),0)+1

part1 = len([n for n in grid.values() if n > 1])

print("#1", part1)

for line in puzzle:
    x1, y1, x2, y2 = [int(d) for d in re.findall(r"\d+",line)]
    # diagonal lines
    if x1!=x2 and y1!=y2:
        start = (x1, y1)
        end = (x2, y2)
        # print(x1,y1,x2,y2)
        point1 = min(start, end)
        point2 = max(start, end)
        x1, y1 = point1
        x2, y2 = point2
        print("heading", point1, "->", point2)
        tilt = 1
        if y2 < y1:
            # / instead of \
            tilt = -1
        for dist in range(x2-x1+1):            
            x = x1 + dist
            y = y1 + dist*tilt
            # print(x,y)
            grid[(x,y)] = grid.get((x,y),0)+1


for y in range(10):
    for x in range(10):
        print(grid.get((x,y),'.'),end='')
    print()

# 19635 too low
part2 = len([n for n in grid.values() if n > 1])

print("#2", part2)