from aoc import readinput
import re

puzzle = "target area: x=20..30, y=-10..-5"

puzzle = readinput(17)[0]
x1, x2, y1, y2 = [int(i) for i in re.findall(r"-?\d+", puzzle)]
top_left = (min(x1, x2), max(y1, y2))
bottom_right = (max(x1, x2), min(y1, y2))

print("target box", top_left, bottom_right)

# to go high, we aim up.  gravity pulls us down 1 each step.
# y_velocity of 5 takes 5 steps to stop going up.  5+4+3+2+1 is that n*(n+1)/2 stuff
# coming down, back at 0 with a velocity of -5-1, so next step goes down -6.
# to land in the box, we need n < bottom_right.y, so n = bottom_right.y-1
print("#1", (abs(bottom_right[1])-1)*abs(bottom_right[1])//2)


def fire_probe(aim):
    # angry birds go!
    velocity = list(aim)
    pos = (0, 0)
    while True:
        if pos[0] > bottom_right[0] or pos[1] < bottom_right[1]:
            return False
        if (top_left[0] <= pos[0] <= bottom_right[0]) and \
                (top_left[1] >= pos[1] >= bottom_right[1]):
            return True
        pos = (pos[0]+velocity[0], pos[1]+velocity[1])
        # drag
        if velocity[0] > 0:
            velocity[0] -= 1
        elif velocity[0] < 0:
            velocity[0] += 1
        # gravity
        velocity[1] -= 1


valid = 0
for x in range(1, bottom_right[0]+1):
    for y in range(bottom_right[1]-1, abs(bottom_right[1])):
        if fire_probe((x, y)):
            valid += 1

print("#2", valid)
