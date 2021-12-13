from aoc import readinput

puzzle = """6,10
0,14
9,10
0,3
10,4
4,11
6,0
6,12
4,1
0,13
10,12
3,4
3,0
8,4
1,10
2,14
8,10
9,0

fold along y=7
fold along x=5""".splitlines()

puzzle = readinput(13)

dots = set()
folds = list()
for line in puzzle:
    if ',' in line:
        x, y = line.split(',')
        dots.add(tuple([int(x), int(y)]))
    if line.startswith('fold'):
        _, _, inst = line.split()
        axis, fold = inst.split('=')
        folds.append(tuple([axis, int(fold)]))

# print(dots)
# print(folds)


def fold_dots(dots, fold):
    axis, fold = fold
    index = 0 if axis == 'x' else 1

    to_move = list()
    for dot in dots:
        if dot[index] > fold:
            to_move.append(dot)

    for dot in to_move:
        dots.remove(dot)
        new_dot = list(dot)
        dist = dot[index] - fold
        new_dot[index] -= 2*dist
        dots.add(tuple(new_dot))

    return dots


dots = fold_dots(dots, folds[0])

print("#1", len(dots))

for fold in folds[1:]:
    dots = fold_dots(dots, fold)

min_x = min([x for x, y in dots])
max_x = max([x for x, y in dots])
min_y = min([y for x, y in dots])
max_y = max([y for x, y in dots])

for y in range(min_y, max_y+1):
    for x in range(min_x, max_x+1):
        print("#", end='') if (x, y) in dots else print(".", end='')
    print()
