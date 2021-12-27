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


# find rotations of scanners relative to other scanner
scanner_rots = dict()
scanner_ids = list(scanners.keys())

scanner_pos = dict()

print("scanners", scanner_ids)
home = scanner_ids.pop(0)
scanner_pos[home] = (0, 0, 0)
all_beacons = set(scanners[home])

while scanner_ids:
    s = scanner_ids.pop(0)
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
        scanner_ids.append(s)
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
