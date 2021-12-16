from aoc import readinput

rules = """0 = 0000
1 = 0001
2 = 0010
3 = 0011
4 = 0100
5 = 0101
6 = 0110
7 = 0111
8 = 1000
9 = 1001
A = 1010
B = 1011
C = 1100
D = 1101
E = 1110
F = 1111""".splitlines()

hex_rules = {}
for line in rules:
    left, right = line.split(" = ")
    hex_rules[left] = right


def hex2bin(input):
    result = ""
    for char in input:
        result += hex_rules[char]
    return result


def read_packet(packet, ptr=0):

    global version_sum

    ver = int(packet[ptr:ptr+3], 2)
    version_sum += ver

    type = int(packet[ptr+3:ptr+6], 2)
    assert type in range(8)
    ptr += 6

    if type == 4:
        # literal
        bits = ''
        while True:
            group = packet[ptr:ptr+5]
            ptr += 5
            bits += group[1:]
            if group[0] == '0':
                break
        value = int(bits, 2)
    else:
        # operators with sub-packets
        sub_packets = []
        length_type = int(packet[ptr])
        ptr += 1
        if length_type == 0:
            # 15-bit number indicating length of subpackets
            len_subs = int(packet[ptr:ptr+15], 2)
            ptr += 15
            end = ptr+len_subs
            while ptr < end:
                sub_value, ptr = read_packet(packet, ptr)
                sub_packets.append(sub_value)
        elif length_type == 1:
            # 11-bit number representing the number of sub-packets
            num_subs = int(packet[ptr:ptr+11], 2)
            ptr += 11
            for _ in range(num_subs):
                sub_value, ptr = read_packet(packet, ptr)
                sub_packets.append(sub_value)

        else:
            raise RuntimeError(
                f"Unexpected length_type {length_type} at {ptr-1}")

        # now do operator math
        if type == 0:
            # sum
            value = sum(sub_packets)
        elif type == 1:
            # product
            value = 1
            for i in sub_packets:
                value *= i
        elif type == 2:
            # minimum
            value = min(sub_packets)
        elif type == 3:
            # maximum
            value = max(sub_packets)
        elif type == 5:
            # greater than
            assert len(sub_packets) == 2
            value = 1 if sub_packets[0] > sub_packets[1] else 0
        elif type == 6:
            # less than
            assert len(sub_packets) == 2
            value = 1 if sub_packets[0] < sub_packets[1] else 0
        elif type == 7:
            # equal to
            assert len(sub_packets) == 2
            value = 1 if sub_packets[0] == sub_packets[1] else 0
        else:
            raise RuntimeError(
                f"Unexpected operator {type}")

    return value, ptr


puzzle = readinput(16)[0]

# part1, record sum of versions as we explore packets
version_sum = 0
result, ptr = read_packet(hex2bin(puzzle))
print("#1", version_sum)
print("#2", result)
