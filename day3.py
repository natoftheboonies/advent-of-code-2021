from aoc import readinput

sample = """00100
11110
10110
10111
10101
01111
00111
11100
10000
11001
00010
01010""".splitlines()

puzzle = [line.strip() for line in sample]

puzzle = readinput(3)

# turn into 2d array of ints
grid = list()
for line in puzzle:
    row = tuple(int(c) for c in line)
    grid.append(row)

def max_bit(row):
    """max of bit frequency, tie returns 1"""
    return 1 if row.count(1) >= row.count(0) else 0

def min_bit(row):
    """min of bit frequency, tie returns 0"""
    return 1 if row.count(1) < row.count(0) else 0    

def dec_from_bits(bits):
    return int(''.join([str(bit) for bit in bits]),2)

# part 1, find most/least common bit for each number

tipped = list(zip(*grid))
maxes = [max_bit(row) for row in tipped]
mins = [min_bit(row) for row in tipped]

#print(maxes, mins)
print("#1", dec_from_bits(maxes)*dec_from_bits(mins))

# part 2, find most/least common, filtering each step

def diagnostic(rows, minmax = max_bit):

    # determine most/least common bit for head
    target = minmax([row[0] for row in rows])

    # keep only numbers selected by the bit criteria
    filtered = [row[1:] for row in rows if row[0] == target]

    # if one number (row) left, stop and return it
    if len(filtered) <= 1:
        return [target] + list(filtered[0])

    # otherwise, recurse
    return [target] + diagnostic(filtered, minmax)

o2_generator = diagnostic(grid, max_bit)
co2_scrubber = diagnostic(grid, min_bit)

print("#2",dec_from_bits(o2_generator)*dec_from_bits(co2_scrubber))

