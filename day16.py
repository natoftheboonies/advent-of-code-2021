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

def packet_decoder(packet):
    """well then"""

    def decode_literal(stream):
        bits = ''
        for _ in range(4):
            group = stream[0:5]
            stream = stream[5:]
            bits += group[1:]
            if group[0] == '0':
                break
        literal = int(bits,2)
        return literal, stream

    def decode_header(stream):
        # literal packet
        ver = int(stream[0:3], 2)
        stream = stream[3:]
        type = int(stream[0:3], 2)
        stream = stream[3:]
        return ver, type, stream

    ver, type, packet = decode_header(packet)
    if type == 4:
        literal, packet = decode_literal(packet)
        return literal, packet
    elif type in (3, 6):
        # operators
        length_type = int(packet[0])
        packet = packet[1:]
        if length_type == 0:
            # 15-bit number indicating length of subpackets
            sub_bits = int(packet[0:15],2)
            packet = packet[15:]
            sub = packet[0:sub_bits]
        elif length_type == 1:
            # 11-bit number representing the number of sub-packets
            sub_packets = int(packet[0:11],2)
            packet = packet[11:]
        
    else:
        raise RuntimeError(f"unknown type {type}")


sample1 = packet_decoder(hex_to_bin("D2FE28"))
assert sample1 == (2021, '000')

sample2 = packet_decoder(hex_to_bin("38006F45291200"))




