from aoc import readinput
from collections import deque
from copy import copy

puzzle = """start-A
start-b
A-c
A-b
b-d
A-end
b-end""".splitlines()

puzzle = """dc-end
HN-start
start-kj
dc-start
dc-HN
LN-dc
HN-end
kj-sa
kj-HN
kj-dc""".splitlines()

puzzle = readinput(12)

edges = dict()

for line in puzzle:
    left, right = line.split('-')
    edges[left] = edges.get(left,[]) + [right]
    if left != 'start' and right != 'end':
        edges[right] = edges.get(right,[]) + [left]

solutions = set()

paths = deque([['start']])
while paths:
    path = paths.pop()
    # where can I go?
    openings = edges[path[-1]]
    valid_openings = [opening for opening in openings if opening.isupper() or opening not in path]
    for route in valid_openings:
        new_path = path.copy() + [route]
        if route == 'end':
            solutions.add(tuple(new_path))
        else:
            paths.append(new_path)

print('#1',len(solutions))

solutions = set()

small_caves = [cave for cave in edges if cave.islower()]
small_caves.remove('start')
#print(small_caves)

for cave in small_caves:

    paths = deque([['start']])
    while paths:
        path = paths.pop()
        # where can I go?
        openings = edges[path[-1]]
        valid_openings = [opening for opening in openings if opening.isupper() or opening not in path or opening == cave and path.count(opening) < 2]
        for route in valid_openings:
            new_path = path.copy() + [route]
            if route == 'end':
                solutions.add(tuple(new_path))
            else:
                paths.append(new_path)

print("#2", len(solutions))