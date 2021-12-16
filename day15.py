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

max_maze = max(maze)
cols, rows = (i+1 for i in max_maze)


def dijkstra(mult=0):
    # dijkstra's: https://www.youtube.com/watch?v=pVfj6mxhdMw

    # goal is bottom-right of maze or expanded maze
    goal = (max_maze[0]+cols*mult, max_maze[1]+rows*mult)

    # keep track of minimum cost to each node
    shortest = {(0, 0): 0}

    h = []
    # heap queue of cost with position to order by minimum cost
    heapq.heappush(h, (0, (0, 0)))

    while h:
        base_cost, last = heapq.heappop(h)
        # if last in shortest and base_cost > shortest[last]:
        #     continue
        # don't need the above because we return upon finding goal
        if last == goal:
            return base_cost
        # calc distance of each neighbor
        for d in DIRS:
            x, y = last[0]+d[0], last[1]+d[1]
            if x > goal[0] or x < 0 or y > goal[1] or y < 0:
                continue

            # compute adjusted cost for nodes beyond maze
            cost = maze[(x % rows, y % cols)] + x // rows + y // cols
            # wrap cost after 9 to 1
            if cost > 9:
                cost -= 9

            # new cost for this node
            neighbor_cost = base_cost + cost
            if shortest.get((x, y), 99999) > neighbor_cost:
                # update if new low cost
                shortest[(x, y)] = neighbor_cost
                # may already have this node in the queue, but with lower cost goes in front.
                heapq.heappush(h, (neighbor_cost, (x, y)))
    # return shortest[goal]
    raise RuntimeError(f"never reached goal {goal}")


print("#1", dijkstra())

print("#2", dijkstra(4))
