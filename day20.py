from aoc import readinput

puzzle = """..#.#..#####.#.#.#.###.##.....###.##.#..###.####..#####..#....#..#..##..###..######.###...####..#..#####..##..#.#####...##.#.#..#.##..#.#......#.###.######.###.####...#.##.##..#..#..#####.....#.#....###..#.##......#.....#..#..#..##..#...##.######.####.####.#.#...#.......#..#.#.#...####.##.#......#..#...##.#.##..#...##.#.##..###.#......#.#.......#.#.#.####.###.##...#.....####.#..#..#.##.#....##..#.####....##...##..#...#......#.#.......#.......##..####..#...#.#.#...##..#.#..###..#####........#..####......#..#

#..#.
#....
##..#
..#..
..###""".splitlines()

puzzle = readinput(20)

algorithm = list()
for char in puzzle[0]:
    algorithm.append(1 if char == '#' else 0)
assert len(algorithm) == 512

image = dict()
for y, line in enumerate(puzzle[2:]):
    for x, char in enumerate(line):
        image[x,y] = 1 if char == '#' else 0

def print_image(image):
    max_y = max([y for x,y in image])
    min_y = min([y for x,y in image])
    max_x = max([x for x,y in image])
    min_x = min([x for x,y in image])    

    for y in range(min_y-1, max_y+1):
        for x in range(min_x-1,max_x+1):
            print('#' if image.get((x,y),0)==1 else '.',end='')
        print()

#print_image(image)

DIRS = [(-1,-1),(0,-1),(1,-1),(-1,0),(0,0),(1,0),(-1,1),(0,1),(1,1)]
assert len(DIRS)==9

background = 0

for i in range(50):

    if i == 2: 
        print("#1",sum(image.values()) )

    next_image = dict()
    max_y = max([y for x,y in image])
    min_y = min([y for x,y in image])
    max_x = max([x for x,y in image])
    min_x = min([x for x,y in image])    

    for x in range(min_x-1, max_x+2):
        for y in range(min_y-1, max_y+2):
            
            bits = ''
            for d in DIRS:
                bits += str(image.get((x+d[0],y+d[1]),background))
            assert len(bits)==9
            idx = int(bits,2)
            next_image[x,y] = algorithm[idx]

    background = algorithm[int(str(background)*9,2)]

    image = next_image


print("#2",sum(image.values()))

