#!/usr/bin/env python

import fileinput
from pprint import pprint


def most_equally_common(bins, pos, w) -> bool:
    shift = w-pos-1
    s = 0
    for b in bins:
        s += (b & (1 << shift)) >> shift
    return s >= len(bins) - s


def list_reduce(bins, width, match_ones):
    for i in range(0, width):
        shift = (width - i - 1)
        if most_equally_common(bins, i, width) == match_ones:
            # 1 most common in pos i
            bins = [n for n in bins if (n & 1 << shift)]
        else:
            # 0 most common in pos i
            bins = [n for n in bins if (~n & 1 << shift)]

        if len(bins) == 1:
            break
    return bins


all = list()
width = 0
for line in fileinput.input():
    all.append(int(line.strip(), 2))
    if not width:
        width = len(line.strip())

gamma = 0
epsilon = 0
for i in range(0, width):
    shift = (width - i - 1)
    if most_equally_common(all, i, width):
        gamma += 1 << shift
    else:
        epsilon += 1 << shift

print(f'gamma: {gamma} epsilon: {epsilon} mul: {gamma*epsilon}')

oxy = list_reduce(all.copy(), width, True)
co2 = list_reduce(all.copy(), width, False)

print(f"oxy: {oxy} co2: {co2} mul: {oxy[0]*co2[0]}")
