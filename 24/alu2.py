#!/usr/bin/env python

import fileinput
from os import devnull
from typing import Deque, Set, Tuple, List
from collections import deque
from sys import setrecursionlimit

setrecursionlimit(150000)

# The main insight is that 'z' register functions as a stack
# by multiplying and modding wiht 26
#
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

# b1  = [12, 11, 14, -6, 15, 12, -9, 14, 14, -5, -9, -5, -2, -7]
# b2  = [ 4, 10, 12, 14,  6, 16,  1,  7,  8, 11,  8,  3,  1,  8]
# div = [ 1,  1,  1, 26,  1,  1, 26,  1,  1, 26, 26, 26, 26, 26]

code = list()
reg = {'w': 0, 'x': 0, 'y': 0, 'z': 0}


B1 = list()
B2 = list()
DIV = list()

BLOCK_SIZE = 18
k = 0
for line in fileinput.input():
    ins = line.strip().split()
    if len(ins) == 2:
        ins.append(None)
    code.append(ins)

    if not k % BLOCK_SIZE:
        assert ins[0] == 'inp', "failed start block"

    if not (k-4) % BLOCK_SIZE:
        DIV.append(int(ins[2]))

    if not (k-5) % BLOCK_SIZE:
        B1.append(int(ins[2]))

    if not (k-15) % BLOCK_SIZE:
        B2.append(int(ins[2]))

    k += 1


def alu(op: str, a: str, b: str, digits: Deque[str]) -> int:
    global reg

    if b in ['w', 'x', 'y', 'z']:
        b = int(reg[b])
    elif b:
        b = int(b)

    if op == 'inp':
        reg[a] = int(digits.popleft())
    elif op == 'add':
        reg[a] += b
    elif op == 'mul':
        reg[a] *= b
    elif op == 'div':
        if b == 0:
            assert False, "div by zero"
        reg[a] //= b
    elif op == 'mod':
        if reg[a] < 0 or b <= 0:
            assert False, f"invalid mod {a} mod {b}"
        reg[a] %= b
    elif op == 'eql':
        if reg[a] == b:
            reg[a] = 1
        else:
            reg[a] = 0
    else:
        assert False, f"Unknown op:{op}"


def pstack(z: int):
    ''' helper to print values in "z-stack" '''
    s = ''
    while z > 0:
        s += str(z % 26)
        s += ','
        z //= 26
    return s


def python_code(inp: int, z: int, b1: int, b2: int, div: int) -> int:
    ''' decompiled in python code per box lenght 18'''
    # print(f'inp:{inp} b1:{b1} b2:{b2} div:{div}, z:{z}')

    # peek z
    x = z % 26

    # x = z + inp
    x += b1

    # pop
    z //= div

    if x == inp:
        # no push!
        # print(f'x:{x} z:{z} => {pstack(z)}')
        return z
    else:
        # push
        z *= 26
        z += (inp+b2)
        # print(f'x:{x} z:{z} => {pstack(z)}')
        return z


def run_alu(s: str) -> int:
    global reg
    reg = {'w': 0, 'x': 0, 'y': 0, 'z': 0}
    digits = deque(s)
    for j, ins in enumerate(code):
        alu(ins[0], ins[1], ins[2], digits)
    return reg['z']


def run_code(s: str) -> int:
    z = 0
    for i in range(0, 14):
        inp = int(s[i])
        z = python_code(inp, z, B1[i], B2[i], DIV[i])
    return z


def gen_rules_ranges(B1: List[int], B2: List[int], DIV: List[int]) -> Tuple[List, List]:
    ''' Generate rules and try ranges from the inputs of the "boxes"'''
    rules = list()
    ranges = list()
    s = deque()
    print("Rules:")
    for i in range(len(DIV)):
        if DIV[i] == 1:
            s.append(i+1)
        else:
            k = s.pop()
            v = B2[k-1] + B1[i]
            print(f'd{i+1}=d{k} + {v}')

            # d[idx1] = d[idx2] + a
            rules.append({'idx1': i, 'idx2': k-1, 'a': v})
            # d[idx] = [n..m]
            ranges.append({'idx': k-1, 'range': range(max(1, 1-v), min(10, 10-v))})

    assert len(rules) == len(ranges)
    print("--")
    return rules, ranges


def try_nums(n, ranges, rules, i, F):
    for k in ranges[i]['range']:
        n[ranges[i]['idx']] = k
        if i < len(ranges)-1:
            # first apply all ranges
            try_nums(n, ranges, rules, i+1, F)
        else:
            # apply rules for find remaining digits
            for rule in rules:
                assert n[rule['idx2']] != 0
                n[rule['idx1']] = n[rule['idx2']] + rule['a']
                assert n[rule['idx1']] > 0

            print(n)
            # Python (de)compiled code runs much faster
            # z = run_alu(n)
            z = run_code(n)
            if z == 0:
                num = int(''.join([str(l) for l in n]))
                F.add(num)
    return F


def find_valid_codes(rules: List, ranges: List) -> Set:
    n = [0] * 14
    F = set()
    return try_nums(n, ranges, rules, 0, F)


rules, ranges = gen_rules_ranges(B1, B2, DIV)
N = find_valid_codes(rules, ranges)

print("Part 1:", max(N))
print("Part 2:", min(N))
