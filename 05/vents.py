#!/usr/bin/env python

import fileinput


P = {}

for line in fileinput.input():
    line = line.strip()
    (p1, p2) = line.split(" -> ")
    [x1, y1] = [int(i) for i in p1.split(",")]
    [x2, y2] = [int(i) for i in p2.split(",")]

    if x1 < x2:
        xr = range(x1, x2+1)
    else:
        xr = range(x1, x2-1, -1)
    if y1 < y2:
        yr = range(y1, y2+1)
    else:
        yr = range(y1, y2-1, -1)

    if x1 == x2:
        # vertical
        for y in yr:
            if (x1, y) in P:
                P[(x1, y)] += 1
            else:
                P[(x1, y)] = 1

    elif y1 == y2:
        # horizontal
        for x in xr:
            if (x, y1) in P:
                P[(x, y1)] += 1
            else:
                P[(x, y1)] = 1
    else:
        # diagonal
        # continue # uncomment for day1
        for x, y in zip(xr, yr):
            if (x, y) in P:
                P[(x, y)] += 1
            else:
                P[(x, y)] = 1

vents = sum([1 for p in P if P[p] > 1])
print(f"Vents: {vents}")
