from aoc import readinput

puzzle = """2199943210
3987894921
9856789892
8767896789
9899965678""".splitlines()

puzzle = readinput(9)

maze = dict()

for y, line in enumerate(puzzle):
    for x, char in enumerate(line):
        maze[(x,y)] = int(char)

low_points = set()

dirs = [(1,0), (-1,0), (0,1), (0,-1)]

for k, v in maze.items():
    for d in dirs:
        neighbor = (k[0]+d[0],k[1]+d[1])
        if maze.get(neighbor,999) <= v:
            break
    else:
        low_points.add(k)

risk_level = sum([maze[low]+1 for low in low_points])

# 1685 too high
print("#1", risk_level)


def print_basin(basin):
    for y, line in enumerate(puzzle):
        for x, char in enumerate(line):
            if (x,y) in basin:
                print(maze[x,y], end='')
            else:
                print('.', end='')
        print()


# part 2, find basins
basin_sizes = list()
for point in list(low_points):
    #print(point)
    basin = set()
    queue = set()
    queue.add(point)
    visited = set()
    while queue:        
        visit = queue.pop()
        visited.add(visit)
        # check if visit is part of basin:
        for d in dirs:
            neighbor = (visit[0]+d[0],visit[1]+d[1])
            # no problem if our neighbor is 9
            if neighbor in basin or maze.get(neighbor,9) == 9: # ok
                continue
            # if neighbor is lower
            if maze.get(neighbor,9) < maze[visit]:
                break
        else:
            # did not break, add it and enque neighbors
            basin.add(visit)

            for d in dirs:
                neighbor = (visit[0]+d[0],visit[1]+d[1])
                if not neighbor in basin and maze.get(neighbor,9) < 9:
                    queue.add(neighbor)

    #print(len(basin))
    basin_sizes.append(len(basin))
    #print_basin(basin)  

blah = sorted(basin_sizes)

print("#2", blah[-1]*blah[-2]*blah[-3])
          
