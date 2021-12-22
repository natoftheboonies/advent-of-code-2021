from aoc import readinput
import re

puzzle = """on x=10..12,y=10..12,z=10..12
on x=11..13,y=11..13,z=11..13
off x=9..11,y=9..11,z=9..11
on x=10..10,y=10..10,z=10..10""".splitlines()

puzzle = """on x=-20..26,y=-36..17,z=-47..7
on x=-20..33,y=-21..23,z=-26..28
on x=-22..28,y=-29..23,z=-38..16
on x=-46..7,y=-6..46,z=-50..-1
on x=-49..1,y=-3..46,z=-24..28
on x=2..47,y=-22..22,z=-23..27
on x=-27..23,y=-28..26,z=-21..29
on x=-39..5,y=-6..47,z=-3..44
on x=-30..21,y=-8..43,z=-13..34
on x=-22..26,y=-27..20,z=-29..19
off x=-48..-32,y=26..41,z=-47..-37
on x=-12..35,y=6..50,z=-50..-2
off x=-48..-32,y=-32..-16,z=-15..-5
on x=-18..26,y=-33..15,z=-7..46
off x=-40..-22,y=-38..-28,z=23..41
on x=-16..35,y=-41..10,z=-47..6
off x=-32..-23,y=11..30,z=-14..3
on x=-49..-5,y=-3..45,z=-29..18
off x=18..30,y=-20..-8,z=-3..13
on x=-41..9,y=-7..43,z=-33..15
on x=-54112..-39298,y=-85059..-49293,z=-27449..7877
on x=967..23432,y=45373..81175,z=27513..53682""".splitlines()

puzzle = """on x=-5..47,y=-31..22,z=-19..33
on x=-44..5,y=-27..21,z=-14..35
on x=-49..-1,y=-11..42,z=-10..38
on x=-20..34,y=-40..6,z=-44..1
off x=26..39,y=40..50,z=-2..11
on x=-41..5,y=-41..6,z=-36..8
off x=-43..-33,y=-45..-28,z=7..25
on x=-33..15,y=-32..19,z=-34..11
off x=35..47,y=-46..-34,z=-11..5
on x=-14..36,y=-6..44,z=-16..29
on x=-57795..-6158,y=29564..72030,z=20435..90618
on x=36731..105352,y=-21140..28532,z=16094..90401
on x=30999..107136,y=-53464..15513,z=8553..71215
on x=13528..83982,y=-99403..-27377,z=-24141..23996
on x=-72682..-12347,y=18159..111354,z=7391..80950
on x=-1060..80757,y=-65301..-20884,z=-103788..-16709
on x=-83015..-9461,y=-72160..-8347,z=-81239..-26856
on x=-52752..22273,y=-49450..9096,z=54442..119054
on x=-29982..40483,y=-108474..-28371,z=-24328..38471
on x=-4958..62750,y=40422..118853,z=-7672..65583
on x=55694..108686,y=-43367..46958,z=-26781..48729
on x=-98497..-18186,y=-63569..3412,z=1232..88485
on x=-726..56291,y=-62629..13224,z=18033..85226
on x=-110886..-34664,y=-81338..-8658,z=8914..63723
on x=-55829..24974,y=-16897..54165,z=-121762..-28058
on x=-65152..-11147,y=22489..91432,z=-58782..1780
on x=-120100..-32970,y=-46592..27473,z=-11695..61039
on x=-18631..37533,y=-124565..-50804,z=-35667..28308
on x=-57817..18248,y=49321..117703,z=5745..55881
on x=14781..98692,y=-1341..70827,z=15753..70151
on x=-34419..55919,y=-19626..40991,z=39015..114138
on x=-60785..11593,y=-56135..2999,z=-95368..-26915
on x=-32178..58085,y=17647..101866,z=-91405..-8878
on x=-53655..12091,y=50097..105568,z=-75335..-4862
on x=-111166..-40997,y=-71714..2688,z=5609..50954
on x=-16602..70118,y=-98693..-44401,z=5197..76897
on x=16383..101554,y=4615..83635,z=-44907..18747
off x=-95822..-15171,y=-19987..48940,z=10804..104439
on x=-89813..-14614,y=16069..88491,z=-3297..45228
on x=41075..99376,y=-20427..49978,z=-52012..13762
on x=-21330..50085,y=-17944..62733,z=-112280..-30197
on x=-16478..35915,y=36008..118594,z=-7885..47086
off x=-98156..-27851,y=-49952..43171,z=-99005..-8456
off x=2032..69770,y=-71013..4824,z=7471..94418
on x=43670..120875,y=-42068..12382,z=-24787..38892
off x=37514..111226,y=-45862..25743,z=-16714..54663
off x=25699..97951,y=-30668..59918,z=-15349..69697
off x=-44271..17935,y=-9516..60759,z=49131..112598
on x=-61695..-5813,y=40978..94975,z=8655..80240
off x=-101086..-9439,y=-7088..67543,z=33935..83858
off x=18020..114017,y=-48931..32606,z=21474..89843
off x=-77139..10506,y=-89994..-18797,z=-80..59318
off x=8476..79288,y=-75520..11602,z=-96624..-24783
on x=-47488..-1262,y=24338..100707,z=16292..72967
off x=-84341..13987,y=2429..92914,z=-90671..-1318
off x=-37810..49457,y=-71013..-7894,z=-105357..-13188
off x=-27365..46395,y=31009..98017,z=15428..76570
off x=-70369..-16548,y=22648..78696,z=-1892..86821
on x=-53470..21291,y=-120233..-33476,z=-44150..38147
off x=-93533..-4276,y=-16170..68771,z=-104985..-24507""".splitlines()

puzzle = readinput(22)


def parse_puzzle(puzzle):

    steps = list()

    for line in puzzle:
        left, right = line.split()
        coords = [int(x) for x in re.findall(r'-?\d+', right)]
        step = (left, *coords)
        steps.append(step)
        # check if left always lower
        assert step[1] <= step[2]
        assert step[3] <= step[4]
        assert step[5] <= step[6]
    return steps

# can we find overlap with prior?


def part1_slow(puzzle):

    # this isn't gonna work for part 2, but let's just track nodes.
    lights = dict()

    for step in parse_puzzle(puzzle):
        for x in range(max(-50, step[1]), min(50, step[2])+1):
            for y in range(max(-50, step[3]), min(50, step[4])+1):
                for z in range(max(-50, step[5]), min(50, step[6])+1):
                    if step[0] == 'on':
                        lights[(x, y, z)] = 1
                    else:
                        lights[(x, y, z)] = 0
        #print(sum(lights.values()), "after", step)

        # x = step[2] - step[1] + 1
        # y = step[4] - step[3] + 1
        # z = step[6] - step[5] + 1

    print("#1", sum(lights.values()))


part1_slow(puzzle)

# yeah, knew this wasn't gonna work for part2 :-)


def volume(box):
    return (box[1]+1-box[0])*(box[3]+1-box[2])*(box[5]+1-box[4])


def overlap(box1, box2):
    #print(box1, box2)
    x_range = max(box1[0], box2[0]), min(box1[1], box2[1])
    #print('x', x_range)
    if x_range[0] > x_range[1]:
        return None
    y_range = max(box1[2], box2[2]), min(box1[3], box2[3])
    #print('y', y_range)
    if y_range[0] > y_range[1]:
        return None
    z_range = max(box1[4], box2[4]), min(box1[5], box2[5])
    #print('z', z_range)
    if z_range[0] > z_range[1]:
        return None
    return x_range+y_range+z_range


# puzzle = """on x=10..12,y=10..12,z=10..12
# on x=11..13,y=11..13,z=11..13
# off x=9..11,y=9..11,z=9..11
# on x=10..10,y=10..10,z=10..10""".splitlines()

steps = parse_puzzle(puzzle)
# shared = overlap(steps[0][1:], steps[1][1:])
# print(shared, volume(shared))

# after each step, find overlap with remaining boxes.
# recursively!


def find_total_volume(boxes):
    """same as below, recursively this_volume - overlaps + remaining"""
    if len(boxes) == 0:
        return 0
    box, *remainder = boxes
    total_volume = volume(box)
    overlaps = []
    for next_box in remainder:
        box_overlap = overlap(box, next_box)
        if box_overlap is not None:
            overlaps.append(box_overlap)
    total_volume -= find_total_volume(overlaps)

    total_volume += find_total_volume(remainder)
    return total_volume


def what_is_on(steps):
    """recursively follow steps, 
    adding this box (if on) - overlaps with all remaining steps, 
    + what_is_on for remaining steps"""
    if len(steps) == 0:
        return 0
    step, *remaining_steps = steps
    if step[0] == 'off':
        # already considered with overlaps, so just continue
        return what_is_on(remaining_steps)
    # else we are on
    mine = volume(step[1:])

    overlaps = []
    for next_step in remaining_steps:
        box_overlap = overlap(step[1:], next_step[1:])
        if box_overlap is not None:
            overlaps.append(box_overlap)

    my_overlap = find_total_volume(overlaps)

    remainder = what_is_on(remaining_steps)

    return mine - my_overlap + remainder


steps = parse_puzzle(readinput(22))
print("#2", what_is_on(steps))
