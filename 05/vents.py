#!/usr/bin/env python

import fileinput
from collections import defaultdict

P1 = defaultdict(int)
P2 = defaultdict(int)

for line in fileinput.input():
    line = line.strip()
    (p1, p2) = line.split(" -> ")
    [x1, y1] = [int(i) for i in p1.split(",")]
    [x2, y2] = [int(i) for i in p2.split(",")]

    diag = False
    if x1 != x2 and y1 != y2:
        diag = True

    l = max(abs(x1-x2), abs(y1-y2))
    dx = (x2 - x1) / l
    dy = (y2 - y1) / l

    x, y = x1, y1
    for i in range(0, l+1):
        P2[(x, y)] += 1
        if not diag:
            P1[(x, y)] += 1
        x += dx
        y += dy

vents1 = sum([1 for p in P1 if P1[p] > 1])
vents2 = sum([1 for p in P2 if P2[p] > 1])
print(f"Vents1: {vents1} Vents2: {vents2}")
