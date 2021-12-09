#!/usr/bin/env python

import fileinput
from collections import Counter, defaultdict


M = 0
L = defaultdict(int)
P = list()

for line in fileinput.input():
    P.append([int(j) for j in list(line.strip())])

rows = len(P)
cols = len(P[0])
for i in range(rows):
    for j in range(cols):
        if P[i][j] == 9:
            continue
        # walk
        k = i
        l = j
        w = set()
        while True:
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

            # didn't move
            if (k, l) in w:
                L[(k, l)] += 1
                break
            else:
                # add to trail
                w.add((k, l))

t = [v for k, v in Counter(L).most_common(3)]

print(f"Risk: ", sum([P[i][j]+1 for (i, j) in L.keys()]))
print(f"Basin:", t[0]*t[1]*t[2])
