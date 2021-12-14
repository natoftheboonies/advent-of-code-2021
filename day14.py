from aoc import readinput
from itertools import zip_longest

puzzle = """NNCB

CH -> B
HH -> N
CB -> H
NH -> C
HB -> C
HC -> B
HN -> C
NN -> C
BH -> H
NC -> B
NB -> B
BN -> B
BB -> N
BC -> B
CC -> N
CN -> C""".splitlines()

puzzle = readinput(14)
template = list(puzzle[0])

pairs = dict()

for line in puzzle[2:]:
    left, right = line.split(' -> ')
    pairs[left] = right

polymer = template

for step in range(40):
    to_insert = list()
    for idx in range(len(polymer)-1):
        foo = polymer[idx:idx+2]
        bar = pairs[''.join(foo)]
        to_insert.append(bar)

    poly_new = list()
    for idx in range(len(to_insert)):
        poly_new.append(polymer[idx])
        poly_new.append(to_insert[idx])
    poly_new.append(polymer[-1])

    polymer = poly_new

scores = dict()
for char in polymer:
    scores[char] = scores.get(char,0)+1

print("#1",max(scores.values())-min(scores.values()))

