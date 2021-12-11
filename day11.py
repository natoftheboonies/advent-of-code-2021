from aoc import readinput
from itertools import count

puzzle = """11111
19991
19191
19991
11111""".splitlines()

puzzle = """5483143223
2745854711
5264556173
6141336146
6357385478
4167524645
2176841721
6882881134
4846848554
5283751526""".splitlines()

puzzle = readinput(11)

grid = dict()
for y, line in enumerate(puzzle):
    for x, char in enumerate(line):
        grid[(x, y)] = int(char)


def print_octopi(octopi):
    for y, line in enumerate(puzzle):
        for x, _ in enumerate(line):
            print(grid[(x, y)], end='')
        print()
    print()


DIRS = {(0, 1), (1, 0), (-1, 0), (0, -1), (1, 1), (1, -1), (-1, -1), (-1, 1)}
assert len(DIRS) == 8

total_flashes = 0
all_flashed = 0

for step in count(1):

    # increment all
    to_flash = set()
    for k in grid:
        grid[k] += 1
        # collect flash
        if grid[k] > 9:
            to_flash.add(k)

    flashed = set()
    while to_flash:
        flash_me = to_flash.pop()
        # increment neighbors
        for d in DIRS:
            neighbor = (flash_me[0]+d[0], flash_me[1]+d[1])
            if neighbor in grid:
                # nobody re-flashes
                if neighbor in flashed:
                    continue
                grid[neighbor] += 1
                if grid[neighbor] > 9:
                    to_flash.add(neighbor)
        flashed.add(flash_me)

    for octopus in flashed:
        grid[octopus] = 0

    # part 1, count flashes
    if step < 100:
        total_flashes += len(flashed)

    # part 2, find all flashed
    if len(flashed) == len(grid):
        all_flashed = step+1  # start step 1 not 0
        break

#print_octopi(grid)

print('#1', total_flashes)
print('#2', all_flashed)
