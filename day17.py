from aoc import readinput
import re

puzzle = "target area: x=20..30, y=-10..-5"

puzzle = readinput(17)[0]
x1, x2, y1, y2 = [int(i) for i in re.findall(r"-?\d+", puzzle)]
top_left = (min(x1, x2), max(y1, y2))
bottom_right = (max(x1, x2), min(y1, y2))

print("target box", top_left, bottom_right)

# angry birds go!


def fire_probe(aim):
    velocity = list(aim)
    path = [(0, 0)]
    while True:
        pos = path[-1]
        if pos[0] > bottom_right[0] or pos[1] < bottom_right[1]:
            # overshot
            return None, pos[0] > bottom_right[0], pos[1] < bottom_right[1]
        if (top_left[0] <= pos[0] <= bottom_right[0]) and \
                (top_left[1] >= pos[1] >= bottom_right[1]):
            #print("score!", pos)
            return max([y for (x, y) in path]), False, False
        pos_next = (pos[0]+velocity[0], pos[1]+velocity[1])
        path.append(pos_next)
        # drag
        if velocity[0] > 0:
            velocity[0] -= 1
        elif velocity[0] < 0:
            velocity[0] += 1
        # gravity
        velocity[1] -= 1


# assert fire_probe((6, 9))[0] == 45
# assert fire_probe((17, -4)) == (None, True, False)

# let's try a binary search something
guess = [500, 500]  # none false true
toggle_down = toggle_right = False
for _ in range(5000):
    #print("guess", guess)
    score, over_right, over_down = fire_probe(guess)
    if over_right and over_down:
        # print("rd")
        # aim up
        guess[1] *= 2
        guess[0] //= 2
    elif over_right:
        # print("r")
        if toggle_right:
            guess[0] -= 2
        else:
            guess[1] += 1
        toggle_right = not toggle_right
    elif over_down:
        # print("d")
        if toggle_down or guess[1] < 0:
            guess[0] += 1
        else:
            guess[1] -= 2
        toggle_down = not toggle_down
    else:
        break

print(guess, score)

valid = 0
for x in range(200):
    for y in range(-125, 500):
        if fire_probe((x, y))[0] is not None:
            valid += 1

# 235 too low
print("#2", valid)

pairs = """23,-10  25,-9   27,-5   29,-6   22,-6   21,-7   9,0     27,-7   24,-5
25,-7   26,-6   25,-5   6,8     11,-2   20,-5   29,-10  6,3     28,-7
8,0     30,-6   29,-8   20,-10  6,7     6,4     6,1     14,-4   21,-6
26,-10  7,-1    7,7     8,-1    21,-9   6,2     20,-7   30,-10  14,-3
20,-8   13,-2   7,3     28,-8   29,-9   15,-3   22,-5   26,-8   25,-8
25,-6   15,-4   9,-2    15,-2   12,-2   28,-9   12,-3   24,-6   23,-7
25,-10  7,8     11,-3   26,-7   7,1     23,-9   6,0     22,-10  27,-6
8,1     22,-8   13,-4   7,6     28,-6   11,-4   12,-4   26,-9   7,4
24,-10  23,-8   30,-8   7,0     9,-1    10,-1   26,-5   22,-9   6,5
7,5     23,-6   28,-10  10,-2   11,-1   20,-9   14,-2   29,-7   13,-3
23,-5   24,-8   27,-9   30,-7   28,-5   21,-10  7,9     6,6     21,-5
27,-10  7,2     30,-9   21,-8   22,-7   24,-9   20,-6   6,9     29,-5
8,-2    27,-8   30,-5   24,-7""".splitlines()
