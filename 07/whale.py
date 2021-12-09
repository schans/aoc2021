#!/usr/bin/env python

import fileinput

from collections import Counter

for line in fileinput.input():
    P = Counter([int(i) for i in line.strip().split(",")])


def fuel(pos):
    f = 0
    for p, c in P.items():
        f += c * abs(p-pos)
    return f


def fuel2(pos):
    f = 0
    for p, c in P.items():
        d = abs(p-pos)
        f += c * d * (d + 1) // 2
    return f


def min(cost_func):
    prev = None
    for i in range(max(P.keys())):
        f = cost_func(i)
        if prev and f > prev:
            return prev
        prev = f
    return 0


print("Fuel part 1:", min(fuel))
print("Fuel part 2:", min(fuel2))
