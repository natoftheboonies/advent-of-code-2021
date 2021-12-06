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

def print_sample(grid):
    for y in range(10):
        for x in range(10):
            print(grid.get((x,y),'.'),end='')
        print()

puzzle = readinput(5)

lines = list()
for line in puzzle:
    x1, y1, x2, y2 = [int(d) for d in re.findall(r"\d+",line)]
    points = ((x1,y1),(x2,y2))
    lines.append(points)

grid = dict()

for (x1, y1), (x2, y2) in lines:
    # if line is horizontal or vertical
    if x1==x2 or y1==y2:
        x_dir = 1 if x1 < x2 else -1
        y_dir = 1 if y1 < y2 else -1
        for x in range(x1, x2+x_dir, x_dir):
            for y in range(y1, y2+y_dir, y_dir):
                grid[(x,y)] = grid.get((x,y),0)+1

part1 = len([n for n in grid.values() if n > 1])
print("#1", part1)

for (x1, y1), (x2, y2) in lines:
    # diagonal lines
    if x1!=x2 and y1!=y2:
        x_dir = 1 if x1 < x2 else -1
        y_dir = 1 if y1 < y2 else -1        
        for dist in range(abs(x2-x1)+1):            
            x = x1 + dist*x_dir
            y = y1 + dist*y_dir
            grid[(x,y)] = grid.get((x,y),0)+1

part2 = len([n for n in grid.values() if n > 1])
print("#2", part2)