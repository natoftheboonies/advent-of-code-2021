from aoc import readinput

puzzle = """be cfbegad cbdgef fgaecd cgeb fdcge agebfd fecdb fabcd edb | fdgacbe cefdb cefbgd gcbe
edbfga begcd cbg gc gcadebf fbgde acbgfd abcde gfcbed gfec | fcgedb cgb dgebacf gc
fgaebd cg bdaec gdafb agbcfd gdcbef bgcad gfac gcb cdgabef | cg cg fdcagb cbg
fbegcd cbd adcefb dageb afcb bc aefdc ecdab fgdeca fcdbega | efabcd cedba gadfec cb
aecbfdg fbg gf bafeg dbefa fcge gcbea fcaegb dgceab fcbdga | gecf egdcabf bgf bfgea
fgeab ca afcebg bdacfeg cfaedg gcfdb baec bfadeg bafgc acf | gebdcfa ecba ca fadegcb
dbcfg fgd bdegcaf fgec aegbdf ecdfab fbedc dacgb gdcebf gf | cefg dcbef fcge gbcadfe
bdfegc cbegaf gecbf dfcage bdacg ed bedf ced adcbefg gebcd | ed bcgafe cdgba cbgef
egadfb cdbfeg cegd fecab cgb gbdefca cg fgcdab egfdb bfceg | gbdfcae bgc cg cgb
gcafb gcf dcaebfg ecagb gf abcdeg gaef cafbge fdbac fegbdc | fgae cfgab fg bagce""".splitlines()

puzzle = readinput(8)

entries = list()

for line in puzzle:
    left, right = [x.strip() for x in line.split('|')]
    entries.append((left.split(), right.split()))

# digits 1, 4, 7, and 8 have signal lengths 2, 4, 3, and 7
count_simple = 0
for left, right in entries:
    count_simple += len([obs for obs in right if len(obs) in (2, 4, 3, 7)])

print('#1', count_simple)

def decoder(patterns, output):

    signals = [set(list(c)) for c in patterns]
    output_values = [set(list(x)) for x in output]

    # compute sets indicating each signal, 0-9
    sig = [None]*10

    # length : [possible signals]
    # 2: [1], 3: [7], 4: [4], 5: [2, 3, 5], 6: [0, 6, 9], 7: [8]

    len7 = [s for s in signals if len(s)==7]
    assert len(len7) == 1
    sig[8] = len7 = len7.pop()

    len4 = [s for s in signals if len(s)==4]
    assert len(len4) == 1
    sig[4] = len4 = len4.pop()

    len3 = [s for s in signals if len(s)==3]
    assert len(len3) == 1
    sig[7] = len3 = len3.pop()

    len2 = [s for s in signals if len(s)==2]
    assert len(len2) == 1
    sig[1] = len2 = len2.pop()

    len6 = [s for s in signals if len(s)==6]
    assert len(len6) == 3
    len5 = [s for s in signals if len(s)==5]
    assert len(len5) == 3

    # top is present in 7 but not in 1
    t = sig[7] - sig[1]

    # middle and left-upper are in 4 but not in 1
    m_or_lu = sig[4]-sig[1]

    # from len5 possibilities (2, 3, 5) only 3 contains 1
    for cand in len5:
        if sig[1].issubset(cand):
            sig[3] = cand

    # len6 are each missing one: middle, right-upper, or left-down
    m_or_ru_or_ld = set()
    for cand in len6:
        missing = sig[8]-cand
        m_or_ru_or_ld.add(missing.pop())

    # identify middle by intersection
    m = m_or_lu.intersection(m_or_ru_or_ld)
    # and left-upper by subtraction
    lu = m_or_lu - m

    # now find left-upper and right-down with what we know:
    ru_or_ld = m_or_ru_or_ld - m
    ru = ru_or_ld.intersection(sig[1])
    ld = ru_or_ld - ru

    # to complete positions:
    rd = sig[1] - ru
    d = sig[3] - sig[7] - m

    # resolve 0, 6, 9 as we know middle, right-upper and left-down
    for cand in len6:
        # subset because m is set, not char
        if not m.issubset(cand):
            sig[0] = cand
        elif not ru.issubset(cand):
            sig[6] = cand
        elif not ld.issubset(cand):
            sig[9] = cand

    # resolve 2, 3, 5 using missing sides
    for cand in len5:
        if not lu.issubset(cand):
            if not ld.issubset(cand):
                # already identified
                assert sig[3] == cand
            else:
                sig[2] = cand
        else:
            sig[5] = cand

    # all signals resolved. decode the display
    display = [str(sig.index(digit)) for digit in output_values]

    return int(''.join(display))

total_output = sum([decoder(*entry) for entry in entries])

print("#2",total_output)
