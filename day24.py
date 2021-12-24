from aoc import readinput


prog = """inp w
add z w
mod z 2
div w 2
add y w
mod y 2
div w 2
add x w
mod x 2
div w 2
mod w 2""".splitlines()




def runprog(program, inputs):

    memory = {'w' : 0, 'x' : 0, 'y' : 0, 'z' : 0}

    for inst in program:
        op, *arg = inst
        var = arg[0]
        assert var in memory
        if op == 'inp':
            memory[var] = inputs.pop(0)
            #print('read', memory)
            continue
        var_b = arg[1]
        if var_b.isnumeric() or var_b.startswith('-') and var_b[1:].isnumeric():
            b = int(var_b)
        else:
            assert var_b in memory
            b = memory[var_b]
        if op == 'mul':
            memory[var] *= b
        elif op == 'add':
            memory[var] += b
        elif op == 'div':
            if b == 0:
                print('divide by 0')
            memory[var] //= b
        elif op == 'mod':
            if b <= 0:
                print('negative mod')
            if memory[var] < 0:
                print('negative mod a')
            memory[var] = memory[var]%b
        elif op == 'eql':
            memory[var] = 1 if memory[var] == b else 0
    return memory['z']

prog = """inp w
mul x 0
add x z
mod x 26
div z 1
add x 11
eql x w
eql x 0
mul y 0
add y 25
mul y x
add y 1
mul z y
mul y 0
add y w
add y 5
mul y x
add z y
inp w
mul x 0
add x z
mod x 26
div z 1
add x 13
eql x w
eql x 0
mul y 0
add y 25
mul y x
add y 1
mul z y
mul y 0
add y w
add y 5
mul y x
add z y""".splitlines()

program = [line.split() for line in prog]


# min_z = 999999
# for x in range(1,10):
#     for y in range(1,10):
#         result = runprog(program, [x,y])
#         if result < min_z:
#             print(x, y, result)
#             min_z = result

prog = readinput(24)
program = [line.split() for line in prog]

groups = []
group = []
for i, inst in enumerate(program):
    if inst[0] == 'inp':
        #print(i)
        assert i%18 == 0
    # lines 4, 5, 15 differ
    # line 4 is dividing by 26, or 1 (7 of each
    # lines 5 and 15 are both adding numbers
    if i%18 in (4, 5, 15):
        #print(i, i%18, inst)
        group.append(int(inst[2]))
    if i%18 == 15:
        groups.append(tuple(group))
        group = []

print(groups)
        

"""
for the last input:

0 inp w
1 mul x 0
2 add x z
3 mod x 26 -> x is set to z%26
4 div z 26 -> z //= 26
5 add x -13 -> x -= 13
6 eql x w  -> when is x == w? (z%26+add) == w <-- goal
7 eql x 0 -> flip x to 1
8 mul y 0 ----
9 add y 25 
0 mul y x
1 add y 1 -> y = 25 * x + 1, or 26 when x is 1. 
2 mul z y -> z *= y, if x is 0 then no-op
3 mul y 0 ----
4 add y w
5 add y 6
6 mul y x -> y = (w+add)*x
7 add z y => z += y
"""
# massive help from https://notes.dt.in.th/20211224T121217Z7595 :-D

def new_program(groups):
    x = y = z = 0

    for d, a, a2, w in groups:
        x = 0 if (z % 26) + a == w else 1
        y = 25 * x + 1
        z = y * (z // d)
        y = (w + a2) * x
        z = z + y
    return z

def new_program2(groups):
    x = y = z = 0

    for d, a, a2, w in groups:
        if (z % 26) + a == w:
            z //= d
        else:
            z //= d
            z *= 26
            z += (w + a2)
    return z

def new_program3(groups):
    stack = [0]
    for d, a, a2, w in groups:
        #print(stack)
        if stack[-1] == w - a:
            if d == 26:
                stack.pop()
        else:
            if d == 26:
                stack.pop()
            stack.append(w+a2)
    result = 0

    for s in stack:
       result *= 26
       result += s
    return result

inputs = [int(c) for c in "13579246899999"]


foo = []
for i, group in enumerate(groups):
    group_with_input = tuple([*group, inputs[i]])
    foo.append(group_with_input)

assert runprog(program, inputs.copy()) == new_program(foo)
assert new_program(foo) == new_program2(foo)
print(new_program3(foo))
assert new_program(foo) == new_program3(foo)


def search(w, i, stack, digits):
    global groups
    if i == 14:
        return int(''.join(str(x) for x in digits[:-1]))
        
    d, a, a2 = groups[i]
    if d == 26:
        # reducing!
        if (w - a) != stack[-1]:
            return None
        else:
            for digit in range(9,0,-1):
                result = search(digit, i+1, stack[:-1], digits.copy()+[digit])
                if result is not None:
                    return result
    else:
        for digit in range(9,0,-1):
            result = search(digit, i+1, stack.copy() + [w+a2], digits.copy()+[digit])
            if result is not None:
                return result


def search2(w, i, stack, digits):
    global groups
    if i == 14:
        return int(''.join(str(x) for x in digits))
        
    d, a, a2 = groups[i]
    if d == 26:
        # reducing!
        if (w - a) != stack[-1]:
            return None
        else:
            for digit in range(1,10):
                result = search(digit, i+1, stack[:-1], digits.copy()+[digit])
                if result is not None:
                    return result
    else:
        for digit in range(1,10):
            result = search(digit, i+1, stack.copy() + [w+a2], digits.copy()+[digit])
            if result is not None:
                return result

def search3():

    stack = []
    result = [0]*14
    result_part2 = [0]*14
    for i, group in enumerate(groups):
        d, a, a2 = group        
        #print(i, stack)

        if d == 1:
            assert a2 > 0
            stack.append((i, a2))
        else:
            
            assert d == 26
            j, x = stack.pop()
            diff = x + a
            print(i, diff, j)
            if diff < 0:
                i, j, diff = j, i, -diff
            result[i] = 9
            result[j] = 9 - diff
            result_part2[i] = 1 + diff
            result_part2[j] = 1
            print(result)

    return int(''.join(str(x) for x in result)), int(''.join(str(x) for x in result_part2))   

max_model, min_model = search3()          

print("#1", max_model)
print("#2", min_model)