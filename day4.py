from aoc import readinput
from pprint import pprint

input = """7,4,9,5,11,17,23,2,0,14,21,24,10,16,13,6,15,25,12,22,18,20,8,19,3,26,1

22 13 17 11  0
 8  2 23  4 24
21  9 14 16  7
 6 10  3 18  5
 1 12 20 15 19

 3 15  0  2 22
 9 18 13 17  5
19  8  7 25 23
20 11 10 24  4
14 21 16 12  6

14 21 17 24  4
10 16 15  9 19
18  8 23 26 20
22 11 13  6  5
 2  0 12  3  7""".splitlines()

input = readinput(4)

draw = [int(x) for x in input[0].split(",")]

boards = []
for line in input[1:]:
    
    if line.strip() == '':
        board = list()
        boards.append(board)
    else:
        board.append([int(x) for x in line.split()])


game_boards = list() # of tuple (rows, cols)
for board in boards:
    # UGH last bug was a bad tipped
    tipped = list(list(tup) for tup in zip(*board))
    game_boards.append((board, tipped))


playing_boards = set(range(len(boards)))
winning_boards = set()

score = 0
for play in draw:
    #print("play", play)
    for rows, cols in game_boards:
        for row in rows:
            if play in row:
                row.remove(play)
        for col in cols:
            if play in col:
                col.remove(play)

    for b, (rows, cols) in enumerate(game_boards):
        for idx, row in enumerate(rows):
            if len(row) == 0:
                print(f"board {b} won on row {idx}")
                winning_boards.add(b)
        for idx, col in enumerate(cols):
            if len(col) == 0:
                print(f"board {b} won on col {idx}")
                winning_boards.add(b)
    if winning_boards:
        winner = list(winning_boards)[0]
        print(f"scoring {winner}")
        rows, cols = game_boards[winner]
        score = sum([sum(row) for row in rows])
        print("won on play",play)
        break      

print("#1",score*play)

last = None
for play in draw[draw.index(play)+1:]:
    print("continue",play)

    for b, (rows, cols) in enumerate(game_boards):
        if b in winning_boards:
            continue
        for row in rows:
            if play in row:
                row.remove(play)
        for col in cols:
            if play in col:
                col.remove(play)
    
    for b, (rows, cols) in enumerate(game_boards):
        if b in winning_boards:
            continue        
        for idx, row in enumerate(rows):
            if len(row) == 0:
                print(f"board {b} won on row {idx}")
                winning_boards.add(b)
        for idx, col in enumerate(cols):
            if len(col) == 0:
                print(f"board {b} won on col {idx}")
                winning_boards.add(b)        
    print("players",len(playing_boards),"winners",len(winning_boards))
    print("game_boards",len(game_boards))

    print("playing_boards",playing_boards)
    print("winner_boards",winning_boards)
    
    if len(playing_boards - winning_boards) == 0:
        print("everyone won")
        break
    
    losers = (playing_boards - winning_boards)
    print("losers", losers)


# 27160 too high
# 38412 too high
print("losers",len(losers))
pprint(game_boards[list(losers)[0]])

score = sum([sum(row) for row in game_boards[losers.pop()][0]])
print("#2",score*play)

