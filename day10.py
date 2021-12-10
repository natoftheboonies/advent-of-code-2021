from aoc import readinput

puzzle = """[({(<(())[]>[[{[]{<()<>>
[(()[<>])]({[<{<<[]>>(
{([(<{}[<>[]}>{[]{[(<()>
(((({<>}<{<{<>}{[]{[]{}
[[<[([]))<([[{}[[()]]]
[{[{({}]{}}([{[{{{}}([]
{<[[]]>}<{[{[{[]{()[[[]
[<(<(<(<{}))><([]([]()
<{([([[(<>()){}]>(<<{{
<{([{{}}[<[[[<>{}]]]>[]]""".splitlines()

SCORE = {')': 3,
    ']': 57,
    '}': 1197,
    '>': 25137
}

PAIRS = {'(': ')', '{':'}', '[':']', '<':'>'}

COSTS = {')':1, ']':2, '}':3, '>':4}

puzzle = readinput(10)

total_score = 0
costs = list()

for id, line in enumerate(puzzle):
    score = 0
    cost = 0
    stack = list()
    for char in line:
        if char in PAIRS.keys():
            stack.append(char)
        elif char in PAIRS.values():
            left = stack.pop()
            if PAIRS[left] != char:
                score += SCORE[char]   
                break             
    else:
        print(stack)
        while stack:
            left = stack.pop()
            cost *= 5
            cost += COSTS[PAIRS[left]]
        print(cost)
    if cost > 0:
        costs.append(cost)
    if score > 0:
        #print(id, score)
        total_score += score

print("#1",total_score)
print("#2",sorted(costs)[len(costs)//2])




