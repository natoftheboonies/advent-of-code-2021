from aoc import readinput
from math import prod

DIRS = [(1, 0), (-1, 0), (0, 1), (0, -1)]

puzzle = """2199943210
3987894921
9856789892
8767896789
9899965678""".splitlines()

puzzle = readinput(9)

maze = dict()

for y, line in enumerate(puzzle):
    for x, char in enumerate(line):
        maze[(x, y)] = int(char)

# part 1, find local low points
low_points = set()

for k, v in maze.items():
    for d in DIRS:
        neighbor = (k[0]+d[0], k[1]+d[1])
        if maze.get(neighbor, 9) <= v:
            break
    else:
        low_points.add(k)

# risk level is 1 + height
risk_level = sum([maze[low]+1 for low in low_points])

print("#1", risk_level)


def print_basin(basin):
    for y, line in enumerate(puzzle):
        for x, char in enumerate(line):
            if (x, y) in basin:
                print(maze[x, y], end='')
            else:
                print('.', end='')
        print()


# part 2, find basins around low points
basin_sizes = list()
for point in low_points:
    basin = set()
    queue = set()
    queue.add(point)
    while queue:
        visit = queue.pop()
        # check if visit is part of basin:
        for d in DIRS:
            neighbor = (visit[0]+d[0], visit[1]+d[1])
            # valid if our neighbor is in basin or edge (9)
            if neighbor in basin or maze.get(neighbor, 9) == 9:
                continue
            # invalid if neighbor is lower
            if maze.get(neighbor, 9) < maze[visit]:
                break
        else:
            # did not break, add to basin and enqueue neighbors
            basin.add(visit)

            for d in DIRS:
                neighbor = (visit[0]+d[0], visit[1]+d[1])
                if not neighbor in basin and maze.get(neighbor, 9) < 9:
                    queue.add(neighbor)

    # basin found, record size
    basin_sizes.append(len(basin))

# multiply size of 3 largest basins
print("#2", prod(sorted(basin_sizes)[-3:]))
