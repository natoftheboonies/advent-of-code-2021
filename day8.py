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

count_simple = 0
for left, right in entries:
    count_simple += len([obs for obs in right if len(obs) in (2, 3, 4, 7)])

print('#1', count_simple)


# so we figure out which characters make which number with left
# and then decode value with right.

"""
 dddd
e    a
e    a
 ffff
g    b
g    b
 cccc
"""

example = 'acedgfb cdfbe gcdfa fbcad dab cefabd cdfgeb eafb cagedb ab'
# known
# 1 = ab
# 7 = dab
# 4 = eafb
# 8 = acdegfb (ignore)

# 'd' is the top from 7 dab - 1 ab


def decoder(patterns, output):


    signals = [set(list(c)) for c in patterns]
    "cdfeb fcadb cdfeb cdbaf"
    decode_me = [set(list(x)) for x in output]

    len7 = [s for s in signals if len(s)==7]
    assert len(len7) == 1
    sig8 = len7 = len7.pop()

    len4 = [s for s in signals if len(s)==4]
    assert len(len4) == 1
    sig4 = len4 = len4.pop()

    len3 = [s for s in signals if len(s)==3]
    assert len(len3) == 1
    sig7 = len3 = len3.pop()

    len2 = [s for s in signals if len(s)==2]
    assert len(len2) == 1
    sig1 = len2 = len2.pop()

    len6 = [s for s in signals if len(s)==6]
    assert len(len6) == 3
    len5 = [s for s in signals if len(s)==5]
    assert len(len5) == 3


    t = len3 - len2
    print(f"t is {t}")

    # 'e' or 'f' is m and lu
    m_or_lu = len4-len2
    print(f"m_or_lu is {m_or_lu}")

    # 2: [1], 3: [7], 4: [4], 5: [2, 3, 5], 6: [0, 6, 9], 7: [8]
    # len7 - len6 indiates middle, left-down, right-down. 
    # len2 indicates left-down, then 4 indicates middle, and remaining is right-down
    # then remaining is len5 set. 
    # len5 containing len2 indicates 3
    for cand in len5:
        if len2.issubset(cand):
            sig3 = cand
            print(f"sig3: {sig3}")

    # len4 - len1 indicates m OR lu
    # len6 unique indicates m, ru, OR ld
    # then we find m. and then lu
    # known t, m, lu, rd, ru

    # len6 missing m, ru, ld
    m_or_ru_or_ld = set()
    for cand in len6:
        asdf = len7-cand
        m_or_ru_or_ld.add(asdf.pop())

    m = m_or_lu.intersection(m_or_ru_or_ld)
    lu = m_or_lu - m

    print(f"t {t}, m {m}, lu {lu}")

    ru_or_ld = m_or_ru_or_ld - m
    ru = ru_or_ld.intersection(len2)
    ld = ru_or_ld - ru
    rd = len2 - ru

    print(f"ru {ru}, rd {rd},  ld {ld}")

    d = sig3 - len3 - m
    print(f"d {d}")

    # resolve 0, 6, 9
    for cand in len6:
        print("decode6",lu,cand)
        if not m.issubset(cand):
            sig0 = cand
        elif not ld.issubset(cand):
            sig9 = cand
        elif not ru.issubset(cand):
            sig6 = cand

    # resolve 2, 3, 5
    for cand in len5:
        if not lu.issubset(cand):
            if not ld.issubset(cand):
                print(lu, cand, sig3)
                assert sig3 == cand
            else:
                sig2 = cand
        else:
            sig5 = cand



    answer = list()
    for blah in decode_me:
        if blah == sig0:
            answer.append(0)
        elif blah == sig1:
            answer.append(1)
        elif blah == sig2:
            answer.append(2)
        elif blah == sig3:
            answer.append(3)
        elif blah == sig4:
            answer.append(4)
        elif blah == sig5:
            answer.append(5)
        elif blah == sig6:
            answer.append(6)
        elif blah == sig7:
            answer.append(7)
        elif blah == sig8:
            answer.append(8)
        elif blah == sig9:
            answer.append(9)        
        else:
            raise RuntimeError(f'unknown signal {blah}')


    print(answer)
    return int(''.join([str(a) for a in answer]))

total_output = 0
for a, b in entries:
    total_output += decoder(a, b)

print("#2",total_output)
