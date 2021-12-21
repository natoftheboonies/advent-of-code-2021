
puzzle = (4, 8)
puzzle = (8, 6)

# part 1
pos = list(puzzle)

score = [0, 0]

roll = 1

player = 0

while max(score) < 1000:
    move = 3*roll+3
    roll += 3
    pos[player] = (pos[player] + move) % 10
    # circle, so just count pos[0] as 10.
    score[player] += 10 if pos[player] == 0 else pos[player]
    # print(
    #     f"player {player+1} moves to {pos[player]} for score {score[player]}")
    player = (player+1) % 2

print("#1", (roll-1)*score[player])

# part 2

# combinations of 1,2,3
POSSIBLE_ROLLS = list()
for x in 1, 2, 3:
    for y in 1, 2, 3:
        for z in 1, 2, 3:
            POSSIBLE_ROLLS.append((x, y, z))

assert len(POSSIBLE_ROLLS) == 27

# but they roll 3x, and the order does not matter (for scores.
# it totally matters for # universes).

game_memo = dict()


def move(pos, score, player):
    game_state = (pos, score, player)
    if game_state in game_memo:
        return game_memo[game_state]

    wins = [0, 0]

    start_pos = pos
    start_score = score

    for x, y, z in POSSIBLE_ROLLS:
        pos = list(start_pos)
        score = list(start_score)

        pos[player] += x+y+z
        pos[player] %= 10

        score[player] += 10 if pos[player] == 0 else pos[player]

        if score[player] >= 21:
            wins[player] += 1
        else:
            recursive_wins = move(tuple(pos), tuple(score),
                                  (player+1) % 2)
            for p in 0, 1:
                wins[p] += recursive_wins[p]

    game_memo[game_state] = wins
    return wins


wins = move(puzzle, (0, 0), 0)
print("#2", max(wins))
