#!/usr/bin/env python

import fileinput

from collections import deque

C = set()
CB = list()

total = 0

for line in fileinput.input():
    state, coords = line.strip().split()

    xstr, ystr, zstr = coords.split(',')
    xmin, xmax = [int(i) for i in xstr.split('=')[1].split('..')]
    ymin, ymax = [int(i) for i in ystr.split('=')[1].split('..')]
    zmin, zmax = [int(i) for i in zstr.split('=')[1].split('..')]

    CB.append((state, (xmin, ymin, zmin, xmax+1, ymax+1, zmax+1)))

    # part 1
    if -50 < xmin < 50 and -50 < xmax < 50:
        for x in range(xmin, xmax+1):
            for y in range(ymin, ymax+1):
                for z in range(zmin, zmax+1):
                    if state == 'on':
                        C.add((x, y, z))
                    elif state == 'off':
                        if (x, y, z) in C:
                            C.remove((x, y, z))


def calc_line(y, z, idx):
    global CB

    if not(len(idx)):
        return 0

    X = set()
    for i in idx:
        state, (x1, y1, z1, x2, y2, z2) = CB[i]
        X.add(x1)
        X.add(x2)
    X = sorted(X)

    p = X[0]
    line = 0
    for x in X[1:]:
        if p != None:
            cur = 'off'
            # find final state per line segment
            for i in idx:
                state, (x1, y1, z1, x2, y2, z2) = CB[i]
                if y1 <= y < y2 and z1 <= z < z2 and x1 <= p < x2:
                    cur = state
            # count segments that are "on"
            if cur == 'on':
                line += x-p
        p = x
    return line


def calc_area(z, idx):
    global CB

    if not(len(idx)):
        return 0

    Y = set()
    for i in idx:
        state, (x1, y1, z1, x2, y2, z2) = CB[i]
        Y.add(y1)
        Y.add(y2)
    Y = sorted(Y)

    p = Y[0]
    area = 0
    for y in Y[1:]:
        yidx = list()
        for i in idx:
            state, (x1, y1, z1, x2, y2, z2) = CB[i]
            if y1 <= p < y2:
                yidx.append(i)
        line = calc_line(p, z, yidx)
        area += line * (y-p)  # points "on" on line * width
        p = y
    return area


def calc_volume():
    global CB

    idx = list()
    Z = set()
    for i, (state, (x1, y1, z1, x2, y2, z2)) in enumerate(CB):
        state, (x1, y1, z1, x2, y2, z2) = CB[i]
        Z.add(z1)
        Z.add(z2)
        idx.append(i)
    Z = sorted(Z)

    p = Z[0]
    vol = 0
    for z in Z[1:]:
        yidx = list()
        for i in idx:
            state, (x1, y1, z1, x2, y2, z2) = CB[i]
            if z1 <= p < z2:
                yidx.append(i)
        area = calc_area(p, yidx)
        vol += area * (z-p)  # points "on" in area * height
        p = z
    return vol


print(f"Part 1: {len(C)}")
print(f"Part 2: {calc_volume()}")
