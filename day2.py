from aoc import readinput

sample = """forward 5
down 5
forward 8
up 3
down 8
forward 2
""".splitlines()

puzzle = sample
puzzle = readinput(2)

instructions = list()

for line in puzzle:
    direction, distance = line.split()
    distance = int(distance)
    instructions.append((direction,distance))

forward = 0
depth = 0

for direction, distance in instructions:
    if direction == 'forward':
        forward += distance
    elif direction == 'down':
        depth += distance
    elif direction == 'up':
        depth -= distance
    else:
        raise RuntimeError(f"unexpected {direction}")

print("#1", forward*depth)

forward = 0
depth = 0
aim = 0

for direction, distance in instructions:
    if direction == 'forward':
        forward += distance
        depth += distance*aim
    elif direction == 'down':
        aim += distance
    elif direction == 'up':
        aim -= distance
    else:
        raise RuntimeError(f"unexpected {direction}")

print("#2", forward*depth)