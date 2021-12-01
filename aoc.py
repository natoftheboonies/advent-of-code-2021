def readinput(idx):
    with open(f"input{idx}",'r') as fp:
        lines = [line.strip() for line in fp.readlines()]
    # removes blank ending line
    if lines[-1] == '':
        lines.pop()
    return lines