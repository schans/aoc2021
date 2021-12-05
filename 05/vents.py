#!/usr/bin/env python

import fileinput


P = {}

for line in fileinput.input():
    line = line.strip()
    (p1, p2) = line.split(" -> ")
    [x1, y1] = [int(i) for i in p1.split(",")]
    [x2, y2] = [int(i) for i in p2.split(",")]

    # uncomment for day1
    # if x1 != x2 and y1 != y2:
    #     # diag
    #     continue

    l = max(abs(x1-x2), abs(y1-y2))
    dx = (x2 - x1) / l
    dy = (y2 - y1) / l

    x, y = x1, y1
    for i in range(0, l+1):
        if (x, y) in P:
            P[(x, y)] += 1
        else:
            P[(x, y)] = 1
        x += dx
        y += dy

vents = sum([1 for p in P if P[p] > 1])
print(f"Vents: {vents}")
