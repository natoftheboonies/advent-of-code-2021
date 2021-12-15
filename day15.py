from aoc import readinput

puzzle = """1163751742
1381373672
2136511328
3694931569
7463417111
1319128137
1359912421
3125421639
1293138521
2311944581""".splitlines()

puzzle = readinput(15)

DIRS = ((0, 1), (1, 0), (0, -1), (-1, 0))

maze = dict()
for y, line in enumerate(puzzle):
    for x, char in enumerate(line):
        maze[(x, y)] = int(char)

start = (0, 0)
goal = max(maze)

# hmm, what are those nice search algorithms?

visited = {start: 0}  # node : cost
explore = [start]

counter = 0

while explore:
    counter += 1
    current = explore.pop()
    cost = visited[current]
    for d in DIRS:
        move = (current[0]+d[0], current[1]+d[1])
        if move not in maze:
            continue
        move_cost = maze[move]
        if move not in visited:
            explore.append(move)
            visited[move] = cost+move_cost
        else:
            # if cost is cheaper, do re-visit
            if cost+move_cost < visited[move]:
                explore.append(move)
                visited[move] = cost+move_cost

    if counter % 5000 == 0:
        print(f"{counter} with queue {len(explore)}")

# 30131 too high
print(visited[goal])
