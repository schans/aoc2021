#!/usr/bin/env python

import fileinput


# Manual rules decode (7 in total):
# divs: 4, 7, 10, 11, 12, 13, 14
#
# ....d4 = (d3+12) -6
# >>> d4 = d3 + 6
#
# ....d7 = (d6+16) -9
# >>> d7 = d6 + 7
#
# ....d10 = (d9 +8) -5
# >>> d10 = d9 +3
#
# ....d11 = (d8+7) -9
# >>> d11 = d8 - 2
#
# ....d12 = (d5+6) -5
# >>> d12 = d5 + 1
#
# ....d13 = (d2+10) -2
# >>> d13 = d2 + 8
#
# ....d14 = (d1+4) -7
# >>> d14 = d1 - 3
#
#         1234   567   890     1234
# ans1 = '9139'+'829'+'969' + '7996'
# ans2 = '4117'+'118'+'314' + '1291'


boxn1 = [
    12,
    11,
    14,
    -6,
    15,
    12,
    -9,
    14,
    14,
    -5,
    -9,
    -5,
    -2,
    -7]

boxn2 = [
    4,
    10,
    12,
    14,
    6,
    16,
    1,
    7,
    8,
    11,
    8,
    3,
    1,
    8]

boxdiv = [
    1,
    1,
    1,
    26,
    1,
    1,
    26,
    1,
    1,
    26,
    26,
    26,
    26,
    26]

reg = {
    'w': 0,
    'x': 0,
    'y': 0,
    'z': 0,
    'i': 0
}


code = list()
for line in fileinput.input():
    ins = line.strip().split()
    if len(ins) == 2:
        ins.append(None)
    if not ins[2] in ['w', 'x', 'y', 'z', None]:
        ins[2] = int(ins[2])
    code.append(ins)


def alu(op, a, b=None):
    global reg, inputs

    if b in ['w', 'x', 'y', 'z']:
        b = int(reg[b])

    if op == 'inp':
        reg[a] = inputs // 10**reg['i'] % 10
        reg['i'] -= 1
    elif op == 'add':
        reg[a] += b
    elif op == 'mul':
        reg[a] *= b
    elif op == 'div':
        if b == 0:
            return None
        reg[a] //= b
    elif op == 'mod':
        if reg[a] < 0 or b <= 0:
            return None
        reg[a] %= b
        pass
    elif op == 'eql':
        if reg[a] == b:
            reg[a] = 1
        else:
            reg[a] = 0
    else:
        assert False, f"Unknown op:{op}"


def reset():
    global reg
    reg = {
        'w': 0,
        'x': 0,
        'y': 0,
        'z': 0,
        'i': 13
    }


def pstack(z):
    ''' helper to print values in "z-stack" '''
    s = ''
    while z > 0:
        s += str(z % 26)
        s += ','
        z //= 26
    return s


def boxer(inp, z, boxn1, boxn2, div):
    ''' decompiled in python code per box lenght 18'''
    # print(f'inp:{inp} b1:{boxn1} b2:{boxn2} div:{div}, z:{z}')

    # peek z
    x = z % 26

    # x = z + inp
    x += boxn1

    # pop
    z //= div

    if x == inp:
        # print(f'x:{x} z:{z} => {pstack(z)}')
        return z
    else:
        # push
        z *= 26
        z += (inp+boxn2)
        # print(f'x:{x} z:{z} => {pstack(z)}')
        return z


def run_alu(s):
    global inputs
    reset()
    inputs = int(s)
    for j, ins in enumerate(code):
        alu(ins[0], ins[1], ins[2])
    return reg['z']


def run_code(s):
    z = 0
    for i in range(0, 14):
        inp = int(s[i])
        z = boxer(inp, z, boxn1[i], boxn2[i], boxdiv[i])
    return z


F = set()
for d1 in [4, 5, 6, 7, 8, 9]:
    for d2 in [1]:
        for d3 in [1, 2, 3]:
            for d5 in [1, 2, 3, 4, 5, 6, 7, 8]:
                for d6 in [1, 2]:
                    for d8 in [3, 4, 5, 6, 7, 8, 9]:
                        for d9 in [1, 2, 3, 4, 5, 6]:
                            # rules
                            d4 = d3 + 6
                            d7 = d6 + 7
                            d10 = d9 + 3
                            d11 = d8 - 2
                            d12 = d5 + 1
                            d13 = d2 + 8
                            d14 = d1 - 3

                            s = str(d1) + str(d2) + str(d3) + str(d4) + str(d5) + str(d6) + str(d7) + \
                                str(d8) + str(d9) + str(d10) + str(d11) + str(d12) + str(d13) + str(d14)

                            # z = run_alu(s)
                            z = run_code(s)

                            if z == 0:
                                # print(s)
                                F.add(int(s))

print("Part 1", max(F))
print("Part 2", min(F))
