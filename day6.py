from aoc import readinput
from itertools import count
from collections import deque

puzzle = "3,4,3,1,2"

puzzle = readinput(6)[0]

timers = [int(t) for t in puzzle.split(',')]

queue = deque([0]*9)

for timer in timers:
    queue[timer] += 1

for x in range(80):
    to_breed = queue[0]
    queue.rotate(-1)
    queue[6] += to_breed

print("#1", sum(queue))

for x in range(256-80):
    to_breed = queue[0]
    queue.rotate(-1)
    queue[6] += to_breed

print("#2", sum(queue))
