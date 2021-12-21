from itertools import count

puzzle = [4, 8]
puzzle = [8, 6]

pos = [x-1 for x in puzzle]

score = [0, 0]

roll = 1

player = 0

while max(score) < 1000:
    move = 3*roll+3
    roll += 3
    pos[player] += move
    pos[player] %= 10
    score[player] += pos[player]+1
    print(
        f"player {player+1} moves to {pos[player]+1} for score {score[player]}")
    player = (player+1) % 2


print("#1", (roll-1)*score[player])
