from aoc import readinput

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

polymer_template = list(puzzle[0])

rules = dict()

for line in puzzle[2:]:
    left, right = line.split(' -> ')
    rules[left] = right


def compute_difference(pair_counts):
    """hint from tamas: only count first character of pairs, plus very end"""

    global polymer_template
    char_counts = dict()
    for pair in pair_counts:
        char_counts[pair[0]] = char_counts.get(pair[0], 0) + pair_counts[pair]
    # the very end remains the same
    char_counts[polymer_template[-1]] += 1

    return (max(char_counts.values()) - min(char_counts.values()))


# construct pairs from template. NNCB -> [NN, NC, CB]
pair_counts = dict()
for pair in [''.join(polymer_template[n:n+2]) for n in range(len(polymer_template)-1)]:
    pair_counts[pair] = pair_counts.get(pair, 0)+1

for step in range(40):
    # record the starting counts for this iter before we start changing them
    working_pairs = {k: v for k, v in pair_counts.items() if v > 0}
    for pair in working_pairs:
        # remove the divided one
        pair_counts[pair] -= working_pairs[pair]
        # add the new ones, as many times as we started with.
        left = pair[0] + rules[pair]
        pair_counts[left] = pair_counts.get(left, 0) + working_pairs[pair]
        right = rules[pair] + pair[1]
        pair_counts[right] = pair_counts.get(right, 0) + working_pairs[pair]

    if step == 9:
        # part1, after 10 steps
        print("#1", compute_difference(pair_counts))

print("#2", compute_difference(pair_counts))
