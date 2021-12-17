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
    print("guess", guess)
    score, over_right, over_down = fire_probe(guess)
    if over_right and over_down:
        print("rd")
        # aim up
        guess[1] *= 2
        guess[0] //= 2
    elif over_right:
        print("r")
        if toggle_right:
            guess[0] -= 2
        else:
            guess[1] += 1
        toggle_right = not toggle_right
    elif over_down:
        print("d")
        if toggle_down or guess[1] < 0:
            guess[0] += 1
        else:
            guess[1] -= 2
        toggle_down = not toggle_down
    else:
        break

print(guess, score)
