#!/usr/bin/env python

import fileinput

from collections import Counter, defaultdict
P = None
R = dict()
STEPS = 40

for line in fileinput.input():
    cur = line.strip()
    if cur == "":
        continue
    if not P:
        P = cur
        continue
    (a, b) = cur.split(' -> ')
    R[a] = b

# create pairs
PP = defaultdict(int)
for c in range(len(P)-1):
    PP[P[c] + P[c+1]] += 1

# permutate
for i in range(STEPS):
    K = defaultdict(int)
    for p in PP:
        if p in R:
            if PP[p] > 0:
                K[p[0] + R[p]] += PP[p]
                K[R[p] + p[1]] += PP[p]
        else:
            print(p)
            K[p] += PP[p]
    PP = K

# Count chas in pairs
C = defaultdict(int)
for p in PP:
    C[p[0]] += PP[p]
    C[p[1]] += PP[p]

# first and last chars are counted only once
C[P[0]] += 1
C[P[-1]] += 1
v = C.values()
print(f"Answer ({STEPS}):", (max(v) - min(v))//2)
