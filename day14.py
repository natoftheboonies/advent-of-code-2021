from aoc import readinput
from pprint import pprint

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

for step in range(10):
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
        scores[char] = scores.get(char, 0)+1

    max_char = max(scores, key=scores.get)
    min_char = min(scores, key=scores.get)

    print(
        f"max {max_char} min {min_char} : {scores[max_char]}, {scores[min_char]}")

print("#1", max(scores.values())-min(scores.values()))

# part2, to 40.  lets look for repeating sections instead.

# on second thought, let's not.
# print(''.join(polymer))

# let's look at the growth of scores
# or just the growth of biggest and smallest?

# both curving up.
# well crap, max changes at like round 17.

# next let's try math on the pairs.  which pairs produce a B or H?
# in sample, 6 produce B, and 2 produce H

# bah. instead we count how many pairs we have maybe?
"""
NNCB has NN, NC, CB
NN -> C : add NC, CN and lose NN
NC -> B : add NB, BC and lose NC
CB -> H : add CH, HB and lose CB

NCNBCHB

NC -> B : add NB, BC and lose NC
CN -> C : add CC, CN and lose CN
NB
BC 
CH
HB


"""

pair_counts = dict()
polymer = template

for pair in [''.join(polymer[n:n+2]) for n in range(len(polymer)-1)]:
    pair_counts[pair] = pair_counts.get(pair, 0)+1
print(pair_counts)

for step in range(40):
    working_pairs = {k: v for k, v in pair_counts.items() if v > 0}
    #print("work", working_pairs)
    for pair in working_pairs:
        inserted = pairs[pair]
        # remove the divided one
        #print("delete", pair, mult)
        assert pair_counts[pair] >= working_pairs[pair]
        pair_counts[pair] -= working_pairs[pair]
        # add the new ones
        left = pair[0]+inserted
        pair_counts[left] = pair_counts.get(left, 0)+working_pairs[pair]
        right = inserted+pair[1]
        pair_counts[right] = pair_counts.get(right, 0)+working_pairs[pair]
        #print("add", left, right)

    # print(pair_counts)

char_counts = dict()
for pair in pair_counts:
    char_counts[pair[0]] = char_counts.get(pair[0], 0)+pair_counts[pair]/2
    char_counts[pair[1]] = char_counts.get(pair[1], 0)+pair_counts[pair]/2

# 3447389044529 too low
print(max(char_counts.values())-min(char_counts.values()))
