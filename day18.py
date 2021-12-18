from aoc import readinput


def parse(snail):
    leaf = list()
    deep = list()
    depth = 0
    for c in snail:
        if c.isdigit():
            leaf.append(int(c))
            deep.append(depth)
        elif c == '[':
            depth += 1
        elif c == ']':
            depth -= 1
        elif c == ',':
            pass
        else:
            raise RuntimeError(f"Unexpected char {c}")
    return leaf, deep

def needs_explode(sn):
    leaf, deep = sn
    return any([d for d in deep if d > 4])

def needs_split(sn):
    leaf, deep = sn
    return any([l for l in leaf if l >= 10])    

def explode(sn):
    leaf, deep = sn
    idx = deep.index(5)
    assert deep[idx] == deep[idx+1] == 5
    left, right = leaf[idx:idx+2]
    if idx > 0:
        leaf[idx-1]+=left
    if idx+2 < len(leaf):
        leaf[idx+2]+=right
    leaf[idx] = 0
    deep[idx] -= 1
    leaf.pop(idx+1)
    deep.pop(idx+1)
    return leaf, deep

def split(sn):
    leaf, deep = sn
    idx = [i for i, n in enumerate(leaf) if n >= 10][0]
    #print(leaf[idx])
    left = leaf[idx]//2
    right = left if leaf[idx]%2 == 0 else left+1
    leaf.insert(idx+1, right)
    deep.insert(idx+1, deep[idx]+1)
    leaf[idx] = left
    deep[idx] += 1
    return leaf, deep

def add(left, right):
    leaf = left[0] + right[0]
    deep = left[1] + right[1]
    deep = [d+1 for d in deep]
    return leaf, deep

def reduce(sn):
    while needs_explode(sn) or needs_split(sn):
        if needs_explode(sn):
            sn = explode(sn)
        else:
            sn = split(sn)
    return sn

def score(sn):
    leaf, deep = sn
    
    #print("score",leaf)
    idx = deep.index(max(deep))
    left, right = leaf[idx:idx+2]
    mag = 3*left + 2*right
    leaf[idx] = mag
    leaf.pop(idx+1)
    deep[idx] -= 1
    deep.pop(idx+1)
    if len(leaf) == 1:
        return leaf[0]
    else:
        return score((leaf, deep))


sn = parse('[[[[[4,3],4],4],[7,[[8,4],9]]],[1,1]]')
sn = reduce(sn)
assert sn == parse('[[[[0,7],4],[[7,8],[6,0]]],[8,1]]')

left = parse('[1,2]')
right = parse('[[3,4],5]')
assert add(left, right) == parse('[[1,2],[[3,4],5]]')

puzzle = """[[[0,[4,5]],[0,0]],[[[4,5],[2,6]],[9,5]]]
[7,[[[3,7],[4,3]],[[6,3],[8,8]]]]
[[2,[[0,8],[3,4]]],[[[6,7],1],[7,[1,6]]]]
[[[[2,4],7],[6,[0,5]]],[[[6,8],[2,8]],[[2,1],[4,5]]]]
[7,[5,[[3,8],[1,4]]]]
[[2,[2,2]],[8,[8,1]]]
[2,9]
[1,[[[9,3],9],[[9,0],[0,7]]]]
[[[5,[7,4]],7],1]
[[[[4,2],2],6],[8,7]]""".splitlines()

snails = [parse(line) for line in puzzle]

snail_sum = snails[0]
for sn in snails[1:]:
    snail_sum = add(snail_sum, sn)
    snail_sum = reduce(snail_sum)

print(snail_sum)
assert snail_sum == parse('[[[[8,7],[7,7]],[[8,6],[7,7]]],[[[0,7],[6,6]],[8,7]]]')

print(score(parse('[[1,2],[[3,4],5]]')))
assert score(parse('[[1,2],[[3,4],5]]'))==143

puzzle = """[[[0,[5,8]],[[1,7],[9,6]]],[[4,[1,2]],[[1,4],2]]]
[[[5,[2,8]],4],[5,[[9,9],0]]]
[6,[[[6,2],[5,6]],[[7,6],[4,7]]]]
[[[6,[0,7]],[0,9]],[4,[9,[9,0]]]]
[[[7,[6,4]],[3,[1,3]]],[[[5,5],1],9]]
[[6,[[7,3],[3,2]]],[[[3,8],[5,7]],4]]
[[[[5,4],[7,7]],8],[[8,3],8]]
[[9,3],[[9,9],[6,[4,9]]]]
[[2,[[7,7],7]],[[5,8],[[9,3],[0,2]]]]
[[[[5,2],5],[8,[3,7]]],[[5,[7,5]],[4,4]]]""".splitlines()

snails = [parse(line) for line in puzzle]

snail_sum = snails[0]
for sn in snails[1:]:
    snail_sum = add(snail_sum, sn)
    snail_sum = reduce(snail_sum)

assert score(snail_sum)==4140

snails = [parse(line) for line in readinput(18)]

snail_sum = snails[0]
for sn in snails[1:]:
    snail_sum = add(snail_sum, sn)
    snail_sum = reduce(snail_sum)

print("#1", score(snail_sum))

max_score = 0

for i, left in enumerate(snails):
    for j, right in enumerate(snails):
        if i == j:
            continue
        sn = add(left, right)
        sn_score = score(reduce(sn))
        if sn_score > max_score:
            max_score = sn_score

print("#2", max_score)

