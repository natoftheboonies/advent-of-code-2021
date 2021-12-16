from aoc import readinput
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

goal = max(maze)

# hmm, what are those nice search algorithms?
# dijkstra's: https://www.youtube.com/watch?v=pVfj6mxhdMw


def calc_cost(node):
    """cost is base cost plus number of tiles right and down"""
    x, y = node
    base_x = x % (goal[0]+1)
    mult_x = x // (goal[0]+1)
    base_y = y % (goal[1]+1)
    mult_y = y // (goal[1]+1)
    cost = maze[(base_x, base_y)] + mult_x + mult_y
    # wrap cost after 9 to 1
    if cost > 9:
        cost -= 9
    return cost


def dijkstra(mult=1):

    max_maze = max(maze)
    goal = tuple((x+1)*mult-1 for x in max_maze)

    shortest = {(0, 0): 0}

    h = []
    heapq.heappush(h, (0, (0, 0)))

    while h:
        base_cost, last = heapq.heappop(h)
        x, y = last
        if x > goal[0] or x < 0 or y > goal[1] or y < 0:
            continue
        if last == goal:
            return base_cost
        # calc distance of each neighbor
        for d in DIRS:
            x, y = last[0]+d[0], last[1]+d[1]
            if x > goal[0] or x < 0 or y > goal[1] or y < 0:
                continue
            neighbor_cost = base_cost + calc_cost((x, y))
            if shortest.get((x, y), 99999) > neighbor_cost:
                shortest[(x, y)] = neighbor_cost
                heapq.heappush(h, (neighbor_cost, (x, y)))
    raise RuntimeError(f"never reached goal {goal}")


print("#1", dijkstra())

print("#2", dijkstra(5))
