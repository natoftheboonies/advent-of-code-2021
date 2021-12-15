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

#puzzle = readinput(15)

DIRS = ((0, 1), (1, 0), (0, -1), (-1, 0))

maze = dict()
for y, line in enumerate(puzzle):
    for x, char in enumerate(line):
        maze[(x, y)] = int(char)

start = (0, 0)
goal = max(maze)

# hmm, what are those nice search algorithms?

# floyd-warshall via #https://www.hackerearth.com/practice/algorithms/graphs/shortest-path-algorithms/tutorial/

dists = dict()


def find_dist(node_i, node_j):
    global dists, maze
    if node_i == node_j:
        return 0
    for d in DIRS:
        if (node_i[0]+d[0], node_i[1]+d[1]) == node_j:
            return maze.get(node_j, 99999)
    if (node_i, node_j) in dists:
        return dists[(node_i, node_j)]
    return 99999


n = len(maze)
for k in range(n):
    for i in range(n):
        for j in range(n):
            node_i = (i//10, (i % 10))
            node_j = (j//10, (j % 10))
            node_k = (k//10, (k % 10))
            dists[(node_i, node_j)] = min(find_dist(node_i, node_j),
                                          find_dist(node_i, node_k)+find_dist(node_k, node_j))

print(dists[(start, goal)])
# 30131 too high
# correct: 769
# print(visited[goal])
