
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
            total_cost += cost * (1 + abs(i-dest))
    for r, room in enumerate(rooms):
        for i, c in enumerate(room):
            if c.isalpha():
                cost = COSTS[c]
                dest = DESTS[c]
                c_room = (r+1)*2
                #print(f'{c} is in {c_room}')
                if c_room != dest:
                    # move to room: up (+up?), lateral, down
                    total_cost += cost * (2 + i + abs(c_room - dest))
    return total_cost

print('estimate', estimate(maze))

goal = (('',)*11,('A','A'),('B','B'),('C','C'),('D','D'))

assert estimate(goal) == 0
almost = (('','D','','','','','','','','',''),('A','A'),('B','B'),('C','C'),('','D'))
assert estimate(almost) == 8000

                
def next_moves(maze):
    hallway, *rooms = maze
    possible = []
    # dudes in hallway are stuck until path to their room
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
            if rooms[room_id][0] == '' and rooms[room_id][1] in (c, ''):
                if rooms[room_id][1] == '':
                    down = 2
                    new_room = ('',c)
                else:
                    down = 1
                    new_room = (c, rooms[room_id][1])
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
        if room[0].isalpha() or room[0] == '' and room[1].isalpha():
            up = 1
            c = room[0]
            new_room = ('',room[1])
            if room[0] == '':
                up = 2
                c = room[1]
                new_room = ('','')

            if DESTS[c] != room_id:
                dest_room_id = DESTS[c]//2-1
                dest_room = rooms[dest_room_id]
                # move if hallway and destination free
                extra = 1 if room_id < DESTS[c] else -1
                if extra == -1:
                    hall_to_check = hallway[min(room_id,DESTS[c])+extra:max(room_id,DESTS[c])]
                else:
                    hall_to_check = hallway[min(room_id,DESTS[c]):max(room_id,DESTS[c])+extra]
                if dest_room[0] == '' and dest_room[1] in ('', c) and all(h == '' for h in hall_to_check):
                    #print('hallway', hall_to_check)
                    cost = COSTS[c]
                    down = 1
                    new_dest_room = (c, dest_room[1])
                    if dest_room[1] == '':
                        down = 2
                        new_dest_room = ('', c)
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
    # dudes in wrong rooms (or if guy below is wrong) can move to the hallway
    for j, room in enumerate(rooms):
        room_id = (j+1)*2
        c = room[0]
        up = 1
        # bottom or both good
        # blocking bad
        # bad
        if c == '':
            up = 2
            c = room[1]
            if c == '' or DESTS[c] == room_id:
                # top empty, bottom empty or good, stay put
                continue
            else:
                #print("top empty, bottom bad", room_id, DESTS[c])
                # top empty, bottom bad, move top
                new_room = ('','')
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
                        new_rooms[j] = new_room
                        new_state = (tuple(new_hallway),*new_rooms)
                        possible.append((move_cost, new_state))


        elif c == room[1] and DESTS[c] == room_id:
            # both good, stay put
            continue
        else:
            # bad or bottom bad, move top
            new_room = ('',room[1])
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
                    new_rooms[j] = new_room
                    new_state = (tuple(new_hallway),*new_rooms)
                    possible.append((move_cost, new_state))

    return possible
                

# ok let's try the search

print(' --- for reals ---')
# print(maze)

# for move in next_moves(maze):
#     print(move, estimate(move[1]))

def search(maze):
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

search(maze)

