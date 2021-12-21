from itertools import count

puzzle = (4, 8)
puzzle = [8, 6]

#pos = [x-1 for x in puzzle]
pos = list(puzzle)

score = [0, 0]

roll = 1

player = 0

while max(score) < 30:
    move = 3*roll+3
    roll += 3
    pos[player] = (pos[player] + move) % 10
    # circle, so just count pos[0] as 10.
    score[player] += 10 if pos[player] == 0 else pos[player]
    # print(
    #     f"player {player+1} moves to {pos[player]} for score {score[player]}")
    player = (player+1) % 2

print("#1", (roll-1)*score[player])

# oof tribonacci recursive stuffs

# from one games state, what are the possible next ones?
# and we just need how many of those did player n win?

# combinations of 1,2,3
POSSIBLE_ROLLS = list()
for x in 1, 2, 3:
    for y in 1, 2, 3:
        for z in 1, 2, 3:
            POSSIBLE_ROLLS.append((x, y, z))

assert len(POSSIBLE_ROLLS) == 27

# but they roll 3x, and the order does not matter (for scores.
# it totally matters for # universes).

game_cache = dict()


def move(pos1, pos2, score1, score2, player):
    game_state = (pos1, pos2, score1, score2, player)
    if game_state in game_cache:
        return game_cache[game_state]

    wins = [0, 0]

    start_pos1, start_pos2 = pos1, pos2
    start_score1, start_score2 = score1, score2

    for x, y, z in POSSIBLE_ROLLS:
        pos1, pos2 = start_pos1, start_pos2
        score1, score2 = start_score1, start_score2
        if player == 0:
            pos1 += x+y+z
            pos1 %= 10

            score1 += 10 if pos1 == 0 else pos1

            if score1 >= 21:
                wins[player] += 1
            else:
                recursive_wins = move(pos1, pos2, score1,
                                      score2, (player+1) % 2)
                for p in 0, 1:
                    wins[p] += recursive_wins[p]
        else:
            pos2 += x+y+z
            pos2 %= 10

            score2 += 10 if pos2 == 0 else pos2

            if score2 >= 21:
                wins[player] += 1
            else:
                recursive_wins = move(pos1, pos2, score1,
                                      score2, (player+1) % 2)
                for p in 0, 1:
                    wins[p] += recursive_wins[p]
    game_cache[game_state] = wins
    return wins


wins = move(*puzzle, 0, 0, 0)
print("#2", max(wins))
