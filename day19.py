import sys
from os import read
from pprint import pprint
from aoc import readinput
import re

puzzle = """--- scanner 0 ---
0,2
4,1
3,3

--- scanner 1 ---
-1,-1
-5,0
-2,1""".splitlines()


def parse(puzzle):
    scanners = dict()
    scanner = ""
    points = []
    for line in puzzle:
        if line == "":
            continue
        if line.startswith("--- scanner"):
            if scanner:
                scanners[scanner] = points
            scanner = re.findall("\d+", line)[0]
            points = []
        else:
            points.append(tuple([int(y) for y in re.findall("-?\d+", line)]))
            scanners[scanner] = points
    return scanners


scanners = parse(puzzle)
# pprint(scanners)


"""
no rotation
x,y =   [ 1,  0]
        [ 0,  1]

90 deg right (counter-clockwise): (1, 3) => (3,-1)
y,-x =  [ 0,  1]
        [-1,  0]

180 deg: (1,3) => (-1, -3)
-x,-y = [-1,  0]
        [ 0, -1]

90 deg left (270 right, clockwise): (1, 3) => (-3, 1)
-y,x =  [ 0, -1]
        [ 1,  0]

"""

# https://en.wikipedia.org/wiki/Rotation_matrix
ROTATE_2D = [
    ((1, 0), (0, 1)),
    ((0, -1), (1, 0)),
    ((-1, 0), (0, -1)),
    ((0, 1), (-1, 0))
]


def rotate2d(point, matrix):
    x, y = point
    x_new = x*matrix[0][0] + y*matrix[1][0]
    y_new = x*matrix[0][1] + y*matrix[1][1]
    return x_new, y_new


assert rotate2d((1, 3), ROTATE_2D[0]) == (1, 3)
assert rotate2d((1, 3), ROTATE_2D[1]) == (3, -1)
assert rotate2d((1, 3), ROTATE_2D[2]) == (-1, -3)
assert rotate2d((1, 3), ROTATE_2D[3]) == (-3, 1)


def dist_vector_2d(a, b):
    ax, ay = a
    bx, by = b
    return ax-bx, ay-by


def compute_distances(points):
    distances = set()
    for point in points:
        for point2 in points:
            if point == point2:
                continue
            distances.add(dist_vector_2d(point, point2))

    return distances

# compute distance vectors between nodes
# for scanner in scanners:
#     print("scanner", scanner)
#     print(compute_distances(scanners[scanner]))


# https://www.reddit.com/r/adventofcode/comments/rjpf7f/comment/hp5nnej/?utm_source=reddit&utm_medium=web2x&context=3

ROTATE_3D = [
    #   ([x, y, z]) => [x, y, z],
    #   ([x, y, z]) => [y, z, x],
    #   ([x, y, z]) => [z, x, y],
    ((1, 0, 0), (0, 1, 0), (0, 0, 1)),
    ((0, 1, 0), (0, 0, 1), (1, 0, 0)),
    ((0, 0, 1), (1, 0, 0), (0, 1, 0)),
    #   ([x, y, z]) => [-x, z, y],
    #   ([x, y, z]) => [z, y, -x],
    #   ([x, y, z]) => [y, -x, z],
    ((-1, 0, 0), (0, 0, 1), (0, 1, 0)),
    ((0, 0, 1), (0, 1, 0), (-1, 0, 0)),
    ((0, 1, 0), (-1, 0, 0), (0, 0, 1)),
    #   ([x, y, z]) => [x, z, -y],
    #   ([x, y, z]) => [z, -y, x],
    #   ([x, y, z]) => [-y, x, z],
    ((1, 0, 0), (0, 0, 1), (0, -1, 0)),
    ((0, 0, 1), (0, -1, 0), (1, 0, 0)),
    ((0, -1, 0), (1, 0, 0), (0, 0, 1)),
    #   ([x, y, z]) => [x, -z, y],
    #   ([x, y, z]) => [-z, y, x],
    #   ([x, y, z]) => [y, x, -z],
    ((1, 0, 0), (0, 0, -1), (0, 1, 0)),
    ((0, 0, -1), (0, 1, 0), (1, 0, 0)),
    ((0, 1, 0), (1, 0, 0), (0, 0, -1)),
    #   ([x, y, z]) => [-x, -y, z],
    #   ([x, y, z]) => [-y, z, -x],
    #   ([x, y, z]) => [z, -x, -y],
    ((-1, 0, 0), (0, -1, 0), (0, 0, 1)),
    ((0, -1, 0), (0, 0, 1), (-1, 0, 0)),
    ((0, 0, 1), (-1, 0, 0), (0, -1, 0)),
    #   ([x, y, z]) => [-x, y, -z],
    #   ([x, y, z]) => [y, -z, -x],
    #   ([x, y, z]) => [-z, -x, y],
    ((-1, 0, 0), (0, 1, 0), (0, 0, -1)),
    ((0, 1, 0), (0, 0, -1), (-1, 0, 0)),
    ((0, 0, -1), (-1, 0, 0), (0, 1, 0)),
    #   ([x, y, z]) => [x, -y, -z],
    #   ([x, y, z]) => [-y, -z, x],
    #   ([x, y, z]) => [-z, x, -y],
    ((1, 0, 0), (0, -1, 0), (0, 0, -1)),
    ((0, -1, 0), (0, 0, -1), (1, 0, 0)),
    ((0, 0, -1), (1, 0, 0), (0, -1, 0)),
    #   ([x, y, z]) => [-x, -z, -y],
    #   ([x, y, z]) => [-z, -y, -x],
    #   ([x, y, z]) => [-y, -x, -z],
    ((-1, 0, 0), (0, 0, -1), (0, -1, 0)),
    ((0, 0, -1), (0, -1, 0), (-1, 0, 0)),
    ((0, -1, 0), (-1, 0, 0), (0, 0, -1)),
]

assert len(ROTATE_3D) == 24
assert len(set(ROTATE_3D)) == 24


def rotate3d(point, matrix):
    x, y, z = point
    x_new = x*matrix[0][0] + y*matrix[1][0] + z*matrix[2][0]
    y_new = x*matrix[0][1] + y*matrix[1][1] + z*matrix[2][1]
    z_new = x*matrix[0][2] + y*matrix[1][2] + z*matrix[2][2]
    return x_new, y_new, z_new


assert rotate3d((1, 2, 3), ROTATE_3D[0]) == (1, 2, 3)


def inverse_3d(matrix):
    return tuple([[-1*i for i in row] for row in matrix])


def dist_vector_3d(a, b):
    ax, ay, az = a
    bx, by, bz = b
    return ax-bx, ay-by, az-bz


def shift_vector_3d(a, b):
    ax, ay, az = a
    bx, by, bz = b
    return ax+bx, ay+by, az+bz


def compute_distances_3d(points):
    distances = set()
    for point in points:
        for point2 in points:
            if point == point2:
                continue
            distances.add(dist_vector_3d(point, point2))

    return distances


puzzle = readinput('19ex')
puzzle = readinput(19)
scanners = parse(puzzle)
total_obs = sum(len(x) for x in scanners.values())
print("total obs", total_obs)


# find rotations of scanners relative to other scanner
scanner_rots = dict()
scanner_ids = list(scanners.keys())
scanner_relative = dict()

scanner_pos = dict()

print("scanners", scanner_ids)
home = '0'
all_beacons = set()
all_beacons.update(scanners[home])

to_match = list(scanner_ids)

while to_match:
    s = to_match.pop(0)
    if s == home:
        continue
    s0_dist = compute_distances_3d(all_beacons)
    # print(f"test {s0} vs {s}")
    best_rot = None
    best_matches = 0
    # find rotation
    for i, rot in enumerate(ROTATE_3D):
        s_dist = [rotate3d(p, rot)
                  for p in compute_distances_3d(scanners[s])]
        matches = len(s0_dist.intersection(s_dist))
        # print(s, i, matches)
        if matches >= 12*11:
            #print(f"{home} overlaps with {s}")
            best_rot = rot
            best_matches = matches
            scanner_rots[(home, s)] = best_rot
            break
        # points

    if best_rot is None:
        to_match.append(s)
        continue

    rot = best_rot
    # rotate points
    s1_rotated_points = set()
    for s1_point in scanners[s]:
        s1_point_s0_basis = rotate3d(s1_point, rot)
        # print(f"{s1} point {s1_point} rotated to {s1_point_s0_basis}")
        s1_rotated_points.add(s1_point_s0_basis)

    # find position of s1
    for s0_point in all_beacons:
        dists = {dist_vector_3d(s0_point, p) for p in all_beacons}
        matched = False
        for s1_point in s1_rotated_points:
            s1_dists = {dist_vector_3d(s1_point, p)
                        for p in s1_rotated_points}
            if len(dists.intersection(s1_dists)) >= 12:
                #print(f"{s0_point} matches {s1_point}")
                relative_distance = dist_vector_3d(s0_point, s1_point)
                if (home, s) in scanner_pos:
                    assert relative_distance == scanner_pos[home, s]
                else:
                    scanner_pos[home, s] = relative_distance
    # add new beacons
    for s1_point in s1_rotated_points:
        all_beacons.add(shift_vector_3d(s1_point, relative_distance))

print("#1", len(all_beacons))
max_dist = 0
for a in scanner_pos.values():
    for b in scanner_pos.values():
        dist = sum(abs(i) for i in dist_vector_3d(a, b))
        if dist > max_dist:
            max_dist = dist
print("#2", max_dist)

sys.exit()

# print("rots:")
# pprint(scanner_rots) # (source_id, dest_id) : rot_matrix

# now what? i guess we gotta figure out *which* beacons overlap.
# we know which pairs overlap,


all_points = set()
for s, v in scanners.items():
    for p in v:
        all_points.add((s, p))

print("ap", len(all_points))

# let's just collect all beacons as we find them.
relative_points = dict()

for s0, s1 in scanner_rots:
    # print("checking", s0, s1)
    equivalences = set()
    rot = scanner_rots[(s0, s1)]
    # print("rot", rot)

    # rotate all s1 points to s0 basis
    s1_rotated_points = set()
    for s1_point in scanners[s1]:
        s1_point_s0_basis = rotate3d(s1_point, rot)
        # print(f"{s1} point {s1_point} rotated to {s1_point_s0_basis}")
        s1_rotated_points.add(s1_point_s0_basis)

    for s0_point in scanners[s0]:
        dists = {dist_vector_3d(s0_point, p) for p in scanners[s0]}
        matched = False
        for s1_point in s1_rotated_points:
            s1_dists = {dist_vector_3d(s1_point, rotate3d(p, rot))
                        for p in scanners[s1]}
            if len(dists.intersection(s1_dists)) >= 12:
                # print(f"{s0_point} matches {s1_point}")
                equivalences.add(((s0, s0_point), (s1, s1_point)))
                relative_distance = dist_vector_3d(s0_point, s1_point)
                if (s0, s1) in scanner_pos:
                    assert relative_distance == scanner_pos[s0, s1]
                scanner_pos[s0, s1] = relative_distance

                matched = True

    s0_relative_points = set()
    for s1_point in s1_rotated_points:
        s0_relative_points.add(shift_vector_3d(s1_point, scanner_pos[s0, s1]))

    relative_points[(s0, s1)] = s0_relative_points

    # print(s0_relative_points.intersection(scanners[s0]))

    print("eq", s0, s1, len(equivalences))

print("pos", scanner_pos)
print("rot", scanner_rots)

# if 0-1 is -1, 1, -1 then 1-0 is 1,-1, 1
# given (0,1), (1,3), (1,4), (2,4) find path from 0 to each scanner
print()


# find scanner 3
foo = rotate3d(scanner_pos[('1', '3')], scanner_rots[('0', '1')])
print("3", shift_vector_3d(scanner_pos['0', '1'], foo))

# find scanner 4
foo = rotate3d(scanner_pos[('1', '4')], scanner_rots[('0', '1')])
print("4", shift_vector_3d(scanner_pos['0', '1'], foo))
s4 = shift_vector_3d(scanner_pos['0', '1'], foo)

# find scanner 2
print("2", shift_vector_3d(s4, scanner_pos['4', '2']))
# 1105, -1205, 1229

print()


visited = set()
unique = 0
# print(scanner_pos)

for s in scanners:
    for p in scanners[s]:
        matches = [eq for eq in equivalences if eq[0]
                   == (s, p) or eq[1] == (s, p)]
        # print("for",(s,p),"found",matches)

        already_counted = False
        for m in matches:
            if m[0][0] in visited or m[1][0] in visited:
                # print("already counted",m)
                already_counted = True
                if (s, p) in all_points:
                    all_points.remove((s, p))
        if not already_counted:
            unique += 1
    visited.add(s)

# i don't know why this overcounts.
print("#1,", unique, len(all_points))

"""

say 0 has a, b, c
and 1 has d, e, f
and 2 has g, h, i

and further that a == d, b == f
and d == h and e == i

how do we count the uniques?
store 0-a, 0-b, 0-c
1-d ? no because == 0-a
1-e ? yes
1-f ? no because == 0-b
2-g ? yes
2-h ? no because == 1-d, even though 1-d is also not counted.
2-i ? no because == 1-e

"""


# scanner_rots['0','0'] = ROTATE_3D[0]

# relative_to_s0 = {'0': (0,0,0)}

# for s0, s1 in scanner_pos:
#     rot = scanner_rots['0',s0]
#     if s0 in relative_to_s0:
#         relative_pos = rotate3d(scanner_pos[s1,s0],rot)
#         print("relative_pos", relative_pos)
#         relative_to_s0[s1] = dist_vector_3d(relative_to_s0[s0], relative_pos)

# pprint(relative_to_s0)
