import sys
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


maze = dict()
for y, line in enumerate(puzzle):
    for x, char in enumerate(line):
        maze[(x, y)] = int(char)

start = (0, 0)
goal = max(maze)

# let's just recurse with cache

dists = dict()


def cost_to_node(node_i):
    global dists, maze
    if node_i in dists:
        return dists[node_i]
    # if we have arrived, go no further. return cost of goal
    if node_i == goal:
        return maze[goal]
    # if we are out of bounds, return wall
    if node_i not in maze:
        return 99999
    # otherwise, cost plus minimum cost of right or below
    cost_right = cost_to_node((node_i[0]+1, node_i[1]))
    cost_below = cost_to_node((node_i[0], node_i[1]+1))
    min_cost = min(cost_right, cost_below)
    # start is free
    if node_i == start:
        return min_cost
    dists[node_i] = maze[node_i] + min_cost
    return dists[node_i]


print("#1", cost_to_node(start))
# 30131 too high
# correct: 769
# print(visited[goal])

sys.setrecursionlimit(10000)

# expand the grid
max_x = max([x for x, y in maze])+1
max_y = max([y for x, y in maze])+1
print(f"max {max_x} {max_y}")

goal = (max_x*5-1, max_y*5-1)
print(goal)

dists = dict()


def computed_cost(node_i):
    base = (node_i[0] % max_x, node_i[1] % max_y)
    inc_x = node_i[0]//max_x
    inc_y = node_i[1]//max_y
    cost = maze[base]+inc_x+inc_y
    # never cost 0
    if cost > 9:
        return cost-9
    return cost


#assert computed_cost((49, 49)) == 9


def cost_to_node(node_i):
    global dists, maze
    if node_i in dists:
        return dists[node_i]

    # new out of bounds
    if node_i[0] >= max_x*5 or node_i[1] >= max_y*5:
        return 999999

    # if we have arrived, go no further. return cost of goal
    if node_i == goal:
        return computed_cost(node_i)

    # otherwise, cost plus minimum cost of right or below
    cost_right = cost_to_node((node_i[0]+1, node_i[1]))
    cost_below = cost_to_node((node_i[0], node_i[1]+1))
    cost_above = cost_to_node((node_i[0], node_i[1]-1))
    cost_left = cost_to_node((node_i[0]-1, node_i[1]))
    min_cost = min(cost_right, cost_below, cost_above, cost_left)
    # start is free
    if node_i == start:
        return min_cost
    dists[node_i] = computed_cost(node_i) + min_cost
    return dists[node_i]


# 2970 too high
print("#2", cost_to_node(start))
