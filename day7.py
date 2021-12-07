from aoc import readinput

puzzle = '16,1,2,0,4,2,7,1,2,14'

puzzle = readinput(7)[0]

crabs = [int(x) for x in puzzle.split(",")]

# find average as a starting point
average = sum(crabs)//len(crabs)
print(f"average {average}")

def fuel(crabs, goto):
    return sum([abs(crab - goto) for crab in crabs])

min_fuel = None
best_goto = None
for goto in range(min(crabs), max(crabs)):
    goto_fuel = fuel(crabs,goto)
    #print(f"goto {goto} fuel {goto_fuel}")
    if not min_fuel or goto_fuel < min_fuel:
        min_fuel = goto_fuel
        best_goto = goto
    if goto_fuel > min_fuel:
        break

print("#1",min_fuel, best_goto)


def fuel2(crabs, goto):
    # 5 = 1+2+3+4+5 => n*(n+1)/2
    total_fuel = 0
    for crab in crabs:
        n = abs(crab - goto)
        total_fuel += n*(n+1)//2

    return total_fuel

min_fuel = None
best_goto = None
for goto in range(min(crabs), max(crabs)):
    goto_fuel = fuel2(crabs,goto)
    #print(f"goto {goto} fuel {goto_fuel}")
    if not min_fuel or goto_fuel < min_fuel:
        min_fuel = goto_fuel
        best_goto = goto
    if goto_fuel > min_fuel:
        break

print("#2",min_fuel, best_goto)