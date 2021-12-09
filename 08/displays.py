#!/usr/bin/env python

import fileinput

from collections import Counter
from collections import defaultdict


# Counter({6: 3, 5: 3, 2: 1, 4: 1, 3: 1, 7: 1})
# uniq len: 1:2, 4:4, 7:3, 8:7
N = ['abcefg', 'cf', 'acdeg', 'acdfg', 'bcdf', 'abdfg', 'abdefg', 'acf', 'abcdefg', 'abcdfg']
C = {'a', 'b', 'c', 'd', 'e', 'f', 'g'}

# socres
W = list()
T = 0


def check_freq(input, wires):
    # use letter frequence to find wires
    freqs = defaultdict(int)
    for i in input:
        for k, v in Counter(i).items():
            freqs[k] += v

    # letter frequencies
    # {'a': 8, 'b': 6, 'c': 8, 'd': 7, 'e': 4, 'f': 9, 'g': 7}
    for k, v in freqs.items():
        if v == 4:
            wires[k] = {'e'}
        elif v == 6:
            wires[k] = {'b'}
        elif v == 7:
            wires[k] = {'d', 'g'}
        elif v == 8:
            wires[k] = {'a', 'c'}
        elif v == 9:
            wires[k] = {'f'}
    # print("freq", wires)


def check_len(input, wires):
    # use lengths to find fires
    for i in input:
        l = len(i)
        # uniq lens 2=>1, 4=>4, 4=>7, 8=>8
        # 2 and 4 is enough
        if l == 2:
            # 1
            for c in i:
                wires[c] &= set(N[1])
        elif l == 4:
            # 4
            for c in i:
                wires[c] &= set(N[4])
    # print("len", wires)


def reduce_single(wires):
    # use already found wires to find wires
    for i, c in wires.items():
        if len(c) == 1:
            for j, d in wires.items():
                if i != j:
                    d -= c
    # print("single", wires)


def get_value(str, wires):
    trans = set()
    for c in str:
        trans.add(next(iter(wires[c])))
    return N.index("".join(sorted(trans)))


def calc_score(output, wires):
    s = 0
    m = 1000
    for o in output:
        s += m * get_value(o, wires)
        m /= 10
    return int(s)


def decode(input, output):
    mapping = {}
    wires = {}

    check_freq(input, wires)
    check_len(input, wires)
    reduce_single(wires)

    W.append(calc_score(output, wires))


for line in fileinput.input():
    (input, output) = line.strip().split(" | ")
    # print(input, "|", output)

    for o in output.split():
        l = len(o)
        if l == 2 or l == 4 or l == 3 or l == 7:
            T += 1

    decode(input.split(), output.split())


print("Part 1:", T)
print("Part 2:", sum(W))
