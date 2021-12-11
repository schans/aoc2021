#!/usr/bin/env python

import fileinput
from collections import defaultdict

C = list()

# clockwise
dx = [-1, -1, 0, 1, 1, 1, 0, -1]
dy = [0, -1, -1, -1, 0, 1, 1, 1]

for line in fileinput.input():
    C.append([int(j) for j in list(line.strip())])

rows = len(C)
cols = len(C[0])

flashes = 0
F = set()


def flash(i, j):
    if (i, j) in F:
        return
    F.add((i, j))
    for d in range(8):
        ii = i + dx[d]
        jj = j + dy[d]
        if 0 <= ii < rows and 0 <= jj < cols:
            C[ii][jj] += 1
            if C[ii][jj] > 9 and (ii, jj) not in F:
                flash(ii, jj)


for day in range(1000):
    for i in range(rows):
        for j in range(cols):
            C[i][j] += 1
    F = set()
    for i in range(rows):
        for j in range(cols):
            if C[i][j] > 9 and not (i, j) in F:
                flash(i, j)
    s = 0
    for i in range(rows):
        for j in range(cols):
            if C[i][j] > 9:
                flashes += 1
                C[i][j] = 0
            s += C[i][j]
    if not s:
        break


print("Part 1:", flashes)
print("Part 2:", day+1)
