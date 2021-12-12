from aoc import readinput

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

# read puzzle into dictionary of { cave: [openings] }
edges = dict()

for line in puzzle:
    left, right = line.split('-')
    edges[left] = edges.get(left, []) + [right]
    # include backtracking
    if left != 'start' and right != 'end':
        edges[right] = edges.get(right, []) + [left]


def part1_rule(opening, path, _):
    """may visit small cave only once"""
    return opening.isupper() or opening not in path


def find_solutions(visit_rule, selected_cave=None):

    solutions = set()

    paths = list([['start']])
    while paths:
        path = paths.pop()
        # where can I go?
        openings = edges[path[-1]]
        valid_openings = [
            opening for opening in openings if visit_rule(opening, path, selected_cave)]
        # update paths to explore with next step, unless it is solution
        for route in valid_openings:
            new_path = path.copy() + [route]
            if route == 'end':
                solutions.add(tuple(new_path))
            else:
                paths.append(new_path)

    return solutions


print('#1', len(find_solutions(part1_rule)))


def part2_rule(opening, path, selected_cave):
    """may visit one small cave twice"""
    return opening.isupper() or \
        opening not in path or \
        (opening == selected_cave and path.count(selected_cave) < 2)


# set to prevent duplicates when considering each small cave
solutions = set()

for selected_cave in [cave for cave in edges if cave.islower() and cave != 'start']:
    solutions.update(find_solutions(part2_rule, selected_cave))

print("#2", len(solutions))
