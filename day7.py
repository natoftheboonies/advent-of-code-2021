from aoc import readinput

puzzle = '16,1,2,0,4,2,7,1,2,14'

puzzle = readinput(7)[0]

crabs = [int(x) for x in puzzle.split(",")]

fuel_memo = dict()

def fuel(crabs, goto):
    global fuel_memo
    if goto not in fuel_memo:        
        fuel_memo[goto] = sum([abs(crab - goto) for crab in crabs])
    return fuel_memo[goto]

fuel2_memo = dict()

def fuel2(crabs, goto):
    global fuel2_memo
    if goto not in fuel2_memo:     
        # 5 = 1+2+3+4+5 => n*(n+1)/2
        total_fuel = 0
        for crab in crabs:
            n = abs(crab - goto)
            total_fuel += n*(n+1)//2
        fuel2_memo[goto] = total_fuel
    return fuel2_memo[goto]

def solver(crabs, fuel_func):
    # find average as a starting point
    guess = sum(crabs)//len(crabs)

    min_fuel = None
    best_goto = None

    while True:
        # compute fuel at this position
        guess_fuel = fuel_func(crabs,guess)

        # retain position if best so far
        if not best_goto or guess_fuel < min_fuel:
            min_fuel = guess_fuel
            best_goto = guess

        # if +1/-1 is better, go there
        if fuel_func(crabs, guess+1) < min_fuel:
            guess = guess+1
        elif fuel_func(crabs, guess-1) < min_fuel:
            guess = guess-1
        else:
            # we are done
            break

    return (min_fuel, best_goto)

print('#1', solver(crabs, fuel)[0])
    
print('#2', solver(crabs, fuel2)[0])