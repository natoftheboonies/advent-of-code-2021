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
#pprint(scanners)


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
    ((0, 0, 1), (1, 0, 0), (0, 0, 1)), 
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

def rotate3d(point, matrix):
    x, y, z = point
    x_new = x*matrix[0][0] + y*matrix[1][0] + z*matrix[2][0]
    y_new = x*matrix[0][1] + y*matrix[1][1] + z*matrix[2][1]
    z_new = x*matrix[0][2] + y*matrix[1][2] + z*matrix[2][2]
    return x_new, y_new, z_new

assert rotate3d((1,2,3),ROTATE_3D[0])==(1,2,3)

def dist_vector_3d(a, b):
    ax, ay, az = a
    bx, by, bz = b
    return ax-bx, ay-by, az-bz

def compute_distances_3d(points):
    distances = set()
    for point in points:
        for point2 in points:
            if point == point2:
                continue
            distances.add(dist_vector_3d(point, point2))

    return distances

puzzle = readinput('19ex')
#puzzle = readinput(19)
scanners = parse(puzzle)
print("total obs", sum(len(x) for x in scanners.values()))

# find rotations of scanners relative to other scanner
scanner_rots = dict()
scanner_ids = list(scanners.keys())
for i, s0 in enumerate(scanner_ids):
    s0_dist = compute_distances_3d(scanners[s0])
    for s in scanner_ids[i:]:
        if s == s0:
            continue
        #print(f"test {s0} vs {s}")
        best_rot = None
        best_matches = 0
        for i, rot in enumerate(ROTATE_3D):
            s_dist = [rotate3d(p, rot) for p in compute_distances_3d(scanners[s])]
            matches = len(s0_dist.intersection(s_dist))
            #print(s, i, matches)
            if matches >= 12*11:
                print(f"{s0} overlaps with {s}")
                best_rot = rot
                best_matches = matches
                scanner_rots[(s0,s)] = best_rot
                break

print("rots:")
pprint(scanner_rots)

# now what? i guess we gotta figure out *which* beacons overlap.
# we know which pairs overlap, 

scanner_pos = dict()

all_points = set()
for k,v in scanners.items():
    for p in v:
        all_points.add((k, p))

for s0, s1 in scanner_rots:
    rot = scanner_rots[(s0,s1)]
    for s0_point in scanners[s0]:
        dists = {dist_vector_3d(s0_point, p) for p in scanners[s0]}
        matched = False
        for s1_point in scanners[s1]: 
            s1_dists = {rotate3d(dist_vector_3d(s1_point, p),rot) for p in scanners[s1]}
            if len(dists.intersection(s1_dists)) >= 12:
                #print(f"{s0_point} matches {s1_point}")
                relative_distance = dist_vector_3d(s0_point, rotate3d(s1_point,rot))
                scanner_pos[s0,s1] = relative_distance
                matched = True



print(scanner_pos)

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




