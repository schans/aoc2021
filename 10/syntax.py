#!/usr/bin/env python

import fileinput
from collections import defaultdict


points = {
    ')': 3,
    ']': 57,
    '}': 1197,
    '>': 25137,
}

points2 = {
    '(': 1,
    '[': 2,
    '{': 3,
    '<': 4,
}


starts = ['<', '{', '(', '[']
ends = ['>', '}', ')', ']']
score = 0

S = list()
ins = list()
for line in fileinput.input():
    l = line.strip()

    # part 1
    corrupt = False
    for c in l:
        if c in starts:
            ins.append(c)
        elif c in ends:
            b = starts[ends.index(c)]
            if ins[-1] != b:
                # print(f"expected {ins[-1]}, got {c}")
                score += points[c]
                corrupt = True
                break
            ins.pop()

    # part 2
    if not corrupt:
        pairs = ('{}', '[]', '<>', '()')
        prev = ""
        s = 0
        while True:
            for p in pairs:
                l = l.replace(p, '')
            if prev == l:
                # all pairs removed, calc score by reversing
                for c in l[::-1]:
                    s *= 5
                    s += points2[c]
                S.append(s)
                break
            prev = l

print("Part 1:", score)
print("Part 2:", sorted(S)[len(S)//2])
