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


def packet_decoder(packet, ptr=0):
    """well then"""

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

    version_sum = 0

    if ptr > len(packet):
        return (0,), ptr

    (ver, type), ptr = decode_header(packet, ptr)
    print(f"ver {ver}")
    version_sum += ver
    if type == 4:
        literal, ptr = decode_literal(packet, ptr)
        print(f"lit {literal}")
        # return literal, ptr
    else:
        # operators
        length_type = int(packet[ptr])
        ptr += 1
        print(f"op type {type}-{length_type}")
        if length_type == 0:
            # 15-bit number indicating length of subpackets
            sub_bits = int(packet[ptr:ptr+15], 2)
            ptr += 15
            print(f"read {sub_bits} bits")
            print(f"{len(packet)-ptr} bits available")
            if sub_bits > (len(packet)-ptr):
                return (version_sum,), ptr
            end = ptr+sub_bits
            bug = packet[ptr:end]
            print(f"sub {sub_bits}", len(bug))
            while ptr < end:
                if len(bug) == 0:
                    break
                header, ptr = packet_decoder(packet, ptr)
                version_sum += header[0]

        elif length_type == 1:
            # 11-bit number representing the number of sub-packets
            sub_packets = int(packet[ptr:ptr+11], 2)
            ptr += 11
            for _ in range(sub_packets):
                header, ptr = packet_decoder(packet, ptr)
                version_sum += header[0]

    return (version_sum,), ptr


#lit1, ptr = packet_decoder(hex_to_bin("D2FE28"))

#sample2 = packet_decoder(hex_to_bin("38006F45291200"))
#sample2 = packet_decoder(hex_to_bin("EE00D40C823060"))

puzzle = "8A004A801A8002F478"

puzzle = readinput(16)[0]
result = packet_decoder(hex_to_bin(puzzle))
# 886 too low
print("#1", result[0][0])
