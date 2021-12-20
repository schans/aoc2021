#!/usr/bin/env python

import fileinput

VERSION_TOTAL = 0

for line in fileinput.input():
    code = int(line.strip(), 16)
    code_bin = bin(code)[2:]

    # fix leading zeros
    if int(line[0], 16) < 8:
        code_bin = '0' + code_bin
    if int(line[0], 16) < 4:
        code_bin = '0' + code_bin


def decode_literal(code_bin):
    last = False
    bstr = ''
    offset = 0
    while not last:
        part = code_bin[offset: offset+5]
        bstr += part[1:]
        if part[0] == '0':
            # stop bit
            last = True
        # next segment
        offset += 5

    val = int(bstr, 2)
    return offset, val


def calculate(type, values):
    # print("calc", type, values)
    if type == 0:
        return sum(values)
    elif type == 1:
        p = 1
        for v in values:
            p *= v
        return p
    elif type == 2:
        return min(values)
    elif type == 3:
        return max(values)
    elif type == 5:
        if values[0] > values[1]:
            return 1
        else:
            return 0
    elif type == 6:
        if values[0] < values[1]:
            return 1
        else:
            return 0
    elif type == 7:
        if values[0] == values[1]:
            return 1
        else:
            return 0
    else:
        print("UNKNOWN TYPE:", type)
        return -1


def parse_packet(code_bin):
    global VERSION_TOTAL
    pos = 0

    if code_bin == '':
        # string consumed
        return None, None

    version = int(code_bin[pos:pos+3], 2)
    pos += 3

    type = int(code_bin[pos:pos+3], 2)
    pos += 3

    VERSION_TOTAL += version

    if type == 4:
        length, val = decode_literal(code_bin[pos:])
        return pos+length, val
    else:
        # operator
        lid = code_bin[pos:pos+1]
        pos += 1

        if lid == '0':
            sub_length = int(code_bin[pos:pos+15], 2)
            pos += 15
            end = pos+sub_length

            values = list()
            while True:
                l, val = parse_packet(code_bin[pos:end])
                if not l:
                    break
                values.append(val)
                pos += l
            return end, calculate(type, values)
        else:
            sub_packets = int(code_bin[pos:pos+11], 2)
            pos += 11

            values = list()
            for p in range(sub_packets):
                l, val = parse_packet(code_bin[pos:])
                values.append(val)
                pos += l
            return pos, calculate(type, values)


p, v = parse_packet(code_bin)
print("Part 1:", VERSION_TOTAL)
print("Part 2:", v)
