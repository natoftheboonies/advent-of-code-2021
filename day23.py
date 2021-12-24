
"""
#############
#...........#
###B#C#B#D###
  #A#D#C#A#
  #########"""
maze = (('',)*11,('B','A'),('C','D'),('B','C'),('D','A'))
# doors at 2,4,6,8

print(maze)

COSTS = {'A': 1, 'B': 10, 'C': 100, 'D': 1000}
DESTS = {'A': 2, 'B': 4, 'C': 6, 'D': 8}

"""moves, if not blocked
top of a burrow can move 2: up-left, up-right
bottom of a burrow (if top vacant) can move 3: up-up-left/right
hallway can move twice: left-left/right-right if not blocked, or left/right-down if burrow unoccupied
- or left/right-down-down

total possile moves
"""

# this should be an a* search, with estimate of how far each dude needs to move to their room
import heapq  
# (dist, estimate, state)


from functools import cache

@cache
def estimate(maze):
    hallway, *rooms = maze
    total_cost = 0
    for i, c in enumerate(hallway):
        if c.isalpha():
            cost = COSTS[c]
            dest = DESTS[c]
            # move to column and enter
            total_cost += cost * (3 + abs(i-dest))
    for r, room in enumerate(rooms):
        for i, c in enumerate(room):
            if c.isalpha():
                cost = COSTS[c]
                dest = DESTS[c]
                c_room = (r+1)*2
                #print(f'{c} is in {c_room}')
                if c_room != dest:
                    # move to room: up (+up?), lateral, down
                    total_cost += cost * (2 + 2 + abs(c_room - dest))
    return total_cost

#print('estimate', estimate(maze))

goal = (('',)*11,('A','A'),('B','B'),('C','C'),('D','D'))

assert estimate(goal) == 0
almost = (('','D','','','','','','','','',''),('A','A'),('B','B'),('C','C'),('','D'))
#assert estimate(almost) == 8000
 

def next_moves(maze):
    hallway, *rooms = maze
    possible = []

    # dudes in hallway can move to their room if not blocked and space
    for i, c in enumerate(hallway):
        if c.isalpha():
            #move_cost = 0
            cost = COSTS[c]
            dest = DESTS[c]
            # move to column and enter
            dir = 1 if i < dest else -1
            blocked = False
            for step in range(i+dir, dest+dir, dir):
                #print(hallway[step])
                if hallway[step].isalpha():
                    blocked = True
            if blocked:
                #cannot move
                #print('blocked')
                continue

            room_id = dest//2-1
            if all(x in (c,'') for x in rooms[room_id]):
                down = 0
                if c in rooms[room_id]:
                    c_at = rooms[room_id].index(c)
                    if c_at > 0:
                        new_room = list(rooms[room_id])
                        new_room[c_at-1] = c
                        down = c_at
                        new_room = tuple(new_room) 
                    else:
                        continue 
                else:
                    new_room = list(rooms[room_id])
                    new_room[-1] = c
                    down = len(new_room)
                    new_room = tuple(new_room)    

                move_cost = cost*(down + abs(dest-i))

                new_hallway = []
                for j, d in enumerate(hallway):
                    if j == i:
                        new_hallway.append('')
                    else:
                        new_hallway.append(d)
                new_rooms = list(rooms)
                new_rooms[room_id] = new_room
                next_state = (tuple(new_hallway), *new_rooms)
                #print(move_cost, next_state)
                possible.append((move_cost, next_state))

    # dudes in rooms can move to their room if path is free
    for j, room in enumerate(rooms):
        room_id = (j+1)*2
        for k, c in enumerate(room):
            if c == '':
                continue
            if c.isalpha() and DESTS[c] != room_id:
                up = k+1
                new_room = list(room)
                new_room[k] = ''
                new_room = tuple(new_room)

                dest_room_id = DESTS[c]//2-1
                dest_room = rooms[dest_room_id]
                # move if hallway and destination free
                extra = 1 if room_id < DESTS[c] else -1
                if extra == -1:
                    hall_to_check = hallway[min(room_id,DESTS[c])+extra:max(room_id,DESTS[c])]
                else:
                    hall_to_check = hallway[min(room_id,DESTS[c]):max(room_id,DESTS[c])+extra]
                if dest_room[0] == '' and all(d in ('', c) for d in dest_room) and all(h == '' for h in hall_to_check):
                    #print('hallway', hall_to_check)
                    cost = COSTS[c]
                    if c in dest_room:
                        c_at = dest_room.index(c)
                        if c_at > 0:
                            new_dest_room = list(dest_room)
                            new_dest_room[c_at-1] = c
                            down = c_at
                        else:
                            continue 
                    else:
                        new_dest_room = list(dest_room)
                        new_dest_room[-1] = c
                        down = len(new_dest_room)
                    new_dest_room = tuple(new_dest_room) 

                    lateral = abs(DESTS[c]-room_id)
                    move_cost = cost * (up+lateral+down) 
                    
                    new_rooms = list(rooms)
                    new_rooms[j] = new_room
                    new_rooms[dest_room_id] = new_dest_room
                    new_state = (hallway, *new_rooms)
                    possible.append((move_cost, new_state))  
    # if we have a move into the right room, just do that!
    if len(possible) > 0:
        return possible
    # dudes in wrong rooms (or if any guy below is wrong) can move to the hallway
    for j, room in enumerate(rooms):
        room_id = (j+1)*2
        # find the first dude
        for k, c in enumerate(room):
            if c.isalpha():
                up = k+1
                break  
        # bottom or both good

        if c != '':
            if DESTS[c] == room_id and all(below == c for below in room[k:]):
                # c is in the right place
                continue
            else:
                # we need to move to hallway
                new_room = list(room)
                new_room[k] = ''
                for lateral_dest in (0,1,3,5,7,9,10):
                    dir = 1 if room_id < lateral_dest else -1
                    blocked = False
                    for step in range(room_id+dir, lateral_dest+dir, dir):
                        #print(hallway[step])
                        if hallway[step].isalpha():
                            blocked = True
                    if not blocked:
                        lateral = abs(room_id - lateral_dest)
                        move_cost = COSTS[c]*(up+lateral)
                        new_hallway = list(hallway)
                        new_hallway[lateral_dest] = c 
                        new_rooms = list(rooms)
                        new_rooms[j] = tuple(new_room)
                        new_state = (tuple(new_hallway),*new_rooms)
                        possible.append((move_cost, new_state))


    return possible
                

almost = (('D','','','','','','','','','',''),('A','A'),('B','B'),('C','C'),('','D'))
print(next_moves(almost))

# ok let's try the search

print(' --- for reals ---')
# print(maze)

# for move in next_moves(maze):
#     print(move, estimate(move[1]))

def search(maze, goal):
    # keep track of minimum cost to each node
    shortest = {maze: 0+estimate(maze)}


    h = []
    # heap queue of cost with position to order by minimum cost
    heapq.heappush(h, (0, estimate(maze), maze))

    counter = 0
    while h:
        counter += 1

        base_cost, est, last = heapq.heappop(h)
        if counter%100000 == 0:
            print(est, last)
            pass
        if last == goal:
            print("we win!!!", base_cost)
            return base_cost

        for move in next_moves(last):
            move_cost, next_state = move
            a_star = base_cost+move_cost+estimate(next_state)
            if next_state in shortest and a_star > shortest[next_state]:
                continue
            shortest[next_state] = a_star           
            heapq.heappush(h, (base_cost+move_cost, estimate(next_state), next_state))

    raise RuntimeError(f"never reached goal {goal}")


foo = """#############
#...B.......#
###B#.#C#D###
  #A#D#C#A#
  #########""".splitlines()

def parse(input):
    hallway = []
    for c in input[1][1:-1]:
        if c.isalpha():
            hallway.append(c)
        else:
            hallway.append('')
    rooms = []
    for idx in (3,5,7,9):
        top = input[2][idx]
        top = '' if top == '.' else top
        bottom = input[3][idx]
        bottom = '' if bottom == '.' else bottom
        new_room = (top, bottom)
        rooms.append(new_room)
    return (tuple(hallway),*rooms)


real = """#############
#...........#
###D#A#C#D###
  #B#C#B#A#
  #########""".splitlines()

sample = """#############
#...........#
###B#C#B#D###
  #A#D#C#A#
  #########""".splitlines()


maze = parse(real)
#print('start', blah)

goal = (('',)*11,('A',)*2,('B',)*2,('C',)*2,('D',)*2)
result = search(maze, goal)
print("#1", result)
assert result == 14148

sample = """#############
#...........#
###B#C#B#D###
  #D#C#B#A#
  #D#B#A#C#
  #A#D#C#A#
  #########""".splitlines()

# sample : 44169, i get 42169
maze2 = (('',)*11,('B','D','D','A'), ('C','C','B','D'), ('B','B','A','C'),('D','A','C','A'))
# real : 43814
#maze2 = (('',)*11,('D','D','D','B'), ('A','C','B','C'), ('C','B','A','B'),('D','A','C','A'))

goal2 = (('',)*11,('A',)*4,('B',)*4,('C',)*4,('D',)*4)
result = search(maze2, goal2)
print("#2", result)
# 40840 too low
