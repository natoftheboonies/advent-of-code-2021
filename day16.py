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

hex2bin = {}
for line in rules:
    left, right = line.split(" = ")
    hex2bin[left] = right


def hex_to_bin(input):
    result = ""
    for char in input:
        result += hex2bin[char]
    return result


version_sum = 0


def packet_decoder(packet, ptr=0):
    """well then"""
    global version_sum

    def decode_literal(stream, ptr):
        bits = ''
        while True:
            group = stream[ptr:ptr+5]
            ptr += 5
            bits += group[1:]
            if group[0] == '0':
                break
        literal = int(bits, 2)
        return literal, ptr

    def decode_header(stream, ptr):
        # print(stream)
        # literal packet
        ver = int(stream[ptr:ptr+3], 2)
        ptr += 3
        type = int(stream[ptr:ptr+3], 2)
        ptr += 3
        stream = stream[3:]
        return (ver, type), ptr

    # if ptr > len(packet):
    #     return (0,), ptr

    value = 0

    (ver, type), ptr = decode_header(packet, ptr)
    print(f"ver {ver}")
    version_sum += ver
    if type == 4:
        literal, ptr = decode_literal(packet, ptr)
        print(f"lit {literal}")
        value = literal
    else:
        # operators with sub-packets
        sub_packets = []
        length_type = int(packet[ptr])
        ptr += 1
        print(f"op type {type}-{length_type}")
        if length_type == 0:
            # 15-bit number indicating length of subpackets
            len_subs = int(packet[ptr:ptr+15], 2)
            ptr += 15
            end = ptr+len_subs
            while ptr < end:
                sub_value, ptr = packet_decoder(packet, ptr)
                sub_packets.append(sub_value)

        elif length_type == 1:
            # 11-bit number representing the number of sub-packets
            num_subs = int(packet[ptr:ptr+11], 2)
            ptr += 11
            for _ in range(num_subs):
                sub_value, ptr = packet_decoder(packet, ptr)
                sub_packets.append(sub_value)

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

    return value, ptr


puzzle = readinput(16)[0]
result = packet_decoder(hex_to_bin(puzzle))
print("#1", version_sum)
print("#2", result[0])
