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

#puzzle = readinput('19ex')

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
        points.append(([int(y) for y in re.findall("-?\d+", line)]))
        scanners[scanner] = points

pprint(scanners)


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

# https://en.wikipedia.org/wiki/Rotation_matrix


def dist_vector(a, b):
    ax, ay = a
    bx, by = b
    return ax-bx, ay-by

def compute_distances(points):
    distances = set()
    for point in points:
        for point2 in points:
            if point == point2:
                continue
            distances.add(dist_vector(point, point2))

    return distances

dists_for_scanner0 = None


# compute distance vectors between nodes
for scanner in scanners:
    print("scanner", scanner)
    print(compute_distances(scanners[scanner]))


# https://www.reddit.com/r/adventofcode/comments/rjpf7f/comment/hp5nnej/?utm_source=reddit&utm_medium=web2x&context=3

ROTATE_3D = [
#   ([x, y, z]) => [x, y, z],
#   ([x, y, z]) => [y, z, x],
#   ([x, y, z]) => [z, x, y],
    ((1, 0, 0), (0, 1, 0), (0, 0, 1)), 
    ((0, 1, 0), (0, 0, 1), (1, 0, 0)), 
    ((0, 0, 1), (1, 0, 0), (0, 1, )), 
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

