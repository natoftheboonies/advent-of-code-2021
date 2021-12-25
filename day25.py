from aoc import readinput

puzzle = """v...>>.vv>
.vv>>.vv..
>>.>v>...v
>>v>>.>.v.
v>v.vv.v..
>.>>..v...
.vv..>.>v.
v.v..>>v.v
....v..v.>""".splitlines()

puzzle = readinput(25)

seafloor = dict()

max_y = len(puzzle)
max_x = len(puzzle[0])

for y, line in enumerate(puzzle):
    for x, char in enumerate(line):
        if char in 'v>':
            seafloor[(x,y)] = char
        
print(max_y, max_x)

def next_seafloor(seafloor):
    moved = 0
    new_seafloor = dict()
    for x,y in seafloor:
        if seafloor[(x,y)] == '>':
            dest = (x+1) % max_x, y
            if dest not in seafloor:
                moved += 1
                new_seafloor[dest] = '>'
            else:
                new_seafloor[(x,y)] = '>'
    for x,y in seafloor:
        if seafloor[(x,y)] == 'v':
            dest = x, (y+1) % max_y
            if seafloor.get(dest,'') != 'v' and dest not in new_seafloor:
                moved += 1
                new_seafloor[dest] = 'v'
            else:
                new_seafloor[(x,y)] = 'v'
    return moved, new_seafloor

def print_seafloor(seafloor):
    for y in range(max_y):
        for x in range(max_x):
            if (x,y) in seafloor:
                print(seafloor[(x,y)], end='')
            else:
                print('.',end='')
        print()
    print()

for x in range(1000):

    moved, seafloor = next_seafloor(seafloor)
    # print(f"After {x+1} step{'s' if x > 0 else ''}:")
    # print_seafloor(seafloor)
    if moved == 0:
        break

print("#1", x+1)

