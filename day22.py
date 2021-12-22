from aoc import readinput
import re


def parse_puzzle(puzzle):

    steps = list()

    for line in puzzle:
        left, right = line.split()
        coords = [int(x) for x in re.findall(r'-?\d+', right)]
        step = (left, *coords)
        steps.append(step)
        # check if left always lower
        assert step[1] <= step[2]
        assert step[3] <= step[4]
        assert step[5] <= step[6]
    return steps


def volume(box):
    return (box[1]+1-box[0])*(box[3]+1-box[2])*(box[5]+1-box[4])


def overlap(box1, box2):
    x_range = max(box1[0], box2[0]), min(box1[1], box2[1])
    y_range = max(box1[2], box2[2]), min(box1[3], box2[3])
    z_range = max(box1[4], box2[4]), min(box1[5], box2[5])
    if z_range[0] > z_range[1] or y_range[0] > y_range[1] or x_range[0] > x_range[1]:
        return None
    return x_range + y_range + z_range


def find_total_volume(boxes):
    """same as below, recursively this_volume - overlaps + remaining"""
    if len(boxes) == 0:
        return 0
    box, *remainder = boxes
    total_volume = volume(box)
    overlaps = []
    for next_box in remainder:
        box_overlap = overlap(box, next_box)
        if box_overlap is not None:
            overlaps.append(box_overlap)
    total_volume -= find_total_volume(overlaps)

    total_volume += find_total_volume(remainder)
    return total_volume


def what_is_on(steps):
    """recursively follow steps, 
    adding this box (if on) - overlaps with all remaining steps, 
    + what_is_on for remaining steps"""
    if len(steps) == 0:
        return 0
    step, *remaining_steps = steps
    if step[0] == 'off':
        # already considered with overlaps, so just continue
        return what_is_on(remaining_steps)
    # else we are on
    mine = volume(step[1:])

    overlaps = []
    for next_step in remaining_steps:
        box_overlap = overlap(step[1:], next_step[1:])
        if box_overlap is not None:
            overlaps.append(box_overlap)

    my_overlap = find_total_volume(overlaps)

    remainder = what_is_on(remaining_steps)

    return mine - my_overlap + remainder


puzzle = """on x=10..12,y=10..12,z=10..12
on x=11..13,y=11..13,z=11..13
off x=9..11,y=9..11,z=9..11
on x=10..10,y=10..10,z=10..10""".splitlines()

puzzle = readinput(22)

steps = parse_puzzle(puzzle)

# for part one let's just adjust the boxes to their overlap with the 50 limit

part1_limit = (-50, 50, -50, 50, -50, 50)
part1_steps = []
for step in steps:
    valid_box = overlap(part1_limit, step[1:])
    if valid_box is not None:
        part1_steps.append((step[0], *valid_box))


print("#1", what_is_on(part1_steps))

print("#2", what_is_on(steps))
