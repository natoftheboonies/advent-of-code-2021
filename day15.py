from aoc import readinput
from collections import deque
import heapq

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
# dijkstra's: https://www.youtube.com/watch?v=pVfj6mxhdMw

shortest = {start: 0}

h = []
heapq.heappush(h, (0, (0, 0)))

while h:
    base_cost, last = heapq.heappop(h)
    x, y = last
    if x > goal[0] or x < 0 or y > goal[1] or y < 0:
        continue
    if last == goal:
        break
    neighbors = dict()
    # calc distance of each neighbor
    for d in DIRS:
        x, y = last[0]+d[0], last[1]+d[1]
        if (x, y) not in maze:
            continue
        neighbor_cost = base_cost + maze[(x, y)]
        if shortest.get((x, y), 99999) > neighbor_cost:
            shortest[(x, y)] = neighbor_cost
            heapq.heappush(h, (neighbor_cost, (x, y)))

print("#1", base_cost)

print(goal)


def part2_cost(node):
    #global goal
    x, y = node
    base_x = x % (goal[0]+1)
    #print(f"{base_x} for {x}")
    mult_x = x // (goal[0]+1)
    base_y = y % (goal[1]+1)
    mult_y = y // (goal[1]+1)
    #print(maze[(base_x, base_y)], base_x, mult_x)
    cost = maze[(base_x, base_y)] + mult_x + mult_y
    if cost > 9:
        cost -= 9
    return cost


#assert part2_cost((49, 49)) == 9

goal2 = tuple((x+1)*5-1 for x in goal)
print(goal2)

shortest = {start: 0}

h2 = []
heapq.heappush(h2, (0, (0, 0)))

while h2:
    base_cost, last = heapq.heappop(h2)
    x, y = last
    if x > goal2[0] or x < 0 or y > goal2[1] or y < 0:
        continue
    if last == goal2:
        break
    neighbors = dict()
    # calc distance of each neighbor
    for d in DIRS:
        x, y = last[0]+d[0], last[1]+d[1]
        if x > goal2[0] or x < 0 or y > goal2[1] or y < 0:
            continue
        neighbor_cost = base_cost + part2_cost((x, y))
        if shortest.get((x, y), 999999) > neighbor_cost:
            shortest[(x, y)] = neighbor_cost
            heapq.heappush(h2, (neighbor_cost, (x, y)))

print("#2", base_cost)
