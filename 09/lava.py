#!/usr/bin/env python

import fileinput
from collections import Counter


M = 0
L = dict()
P = list()

for line in fileinput.input():
    P.append([int(j) for j in list(line.strip())])

rows = len(P)
cols = len(P[0])

for i in range(rows):
    for j in range(cols):

        u = 10
        d = 10
        l = 10
        r = 10
        if i > 0:
            u = P[i-1][j]
        if i < (rows-1):
            d = P[i+1][j]
        if j > 0:
            l = P[i][j-1]
        if j < (cols - 1):
            r = P[i][j+1]

        p = P[i][j]
        if p < u and p < d and p < l and p < r:
            M += p+1
            L[(i, j)] = 0


for i in range(rows):
    for j in range(cols):
        k = i
        l = j
        if P[k][l] == 9:
            continue
        # walk
        while True:
            # check if in min
            if (k, l) in L:
                L[(k, l)] += 1
                break
            # up
            if k > 0 and P[k-1][l] < P[k][l]:
                k -= 1
            # down
            if k < (rows-1) and P[k+1][l] < P[k][l]:
                k += 1
            # left
            if l > 0 and P[k][l-1] < P[k][l]:
                l -= 1
            # right
            if l < (cols-1) and P[k][l+1] < P[k][l]:
                l += 1

t = [v for k, v in Counter(L).most_common(3)]

print(f"Risk: {M}")
print(f"Basin:", t[0]*t[1]*t[2])
