#!/usr/bin/env python

import fileinput

from typing import Tuple
from collections import deque


def tokenize(s: str) -> deque:
    toks = deque()
    p = ''
    d = ''
    for i, c in enumerate(s):
        if p.isdigit() and not c.isdigit():
            toks.append(d)
            d = ''
        if c == '[':
            toks.append(c)
        elif c == ']':
            toks.append(c)
        elif c == ',':
            toks.append(c)
        elif c.isdigit():
            d += c
        p = c
    return toks


def tadd(l: deque, r: deque) -> deque:
    ntoks = deque()
    ntoks.append('[')
    ntoks.extend(l)
    ntoks.append(',')
    ntoks.extend(r)
    ntoks.append(']')
    return ntoks


def tmagnitude(toks: deque) -> int:
    while True:
        if len(toks) == 1:
            return int(toks.pop())

        ntoks = deque()
        for i in range(len(toks)):
            ntoks.append(toks[i])

            if toks[i] == '[' and toks[i+4] == ']':
                ntoks.pop()
                v = int(toks[i+1])*3 + int(toks[i+3])*2
                ntoks.append(str(v))
                for j in range(i+5, len(toks)):
                    ntoks.append(toks[j])

                toks = ntoks
                break


def texplode(toks: deque) -> Tuple[bool, deque]:
    d = 0
    ldi = -1  # last digit index
    edi = -1  # explode digit index
    for i in range(len(toks)):
        if toks[i].isdigit():
            ldi = i
        elif toks[i] == '[':
            d += 1
        elif toks[i] == ']':
            d -= 1
        if d == 5:
            edi = i
            break
    if edi == -1:
        return False, toks

    ntoks = deque()
    for i in range(edi):
        if i == ldi:
            v = int(toks[i]) + int(toks[edi+1])
            ntoks.append(str(v))
        else:
            ntoks.append(toks[i])
    ntoks.append('0')
    added = False
    for i in range(edi+5, len(toks)):
        if not added and toks[i].isdigit():
            added = True
            v = int(toks[i]) + int(toks[edi+3])
            ntoks.append(str(v))
        else:
            ntoks.append(toks[i])
    return True, ntoks


def tsplit(toks: deque) -> Tuple[bool, deque]:
    si = -1
    for i in range(len(toks)):
        if len(toks[i]) > 1:
            si = i
            break
    if si == -1:
        return False, toks

    ntoks = deque()
    for i in range(0, si):
        ntoks.append(toks[i])

    v = int(toks[si])
    l = v//2
    r = v - l
    ntoks.append('[')
    ntoks.append(str(l))
    ntoks.append(',')
    ntoks.append(str(r))
    ntoks.append(']')

    for i in range(si+1, len(toks)):
        ntoks.append(toks[i])

    return True, ntoks


def treduce(toks: deque) -> deque:
    while True:
        while True:
            changed, toks = texplode(toks)
            if not changed:
                break

        changed, toks = tsplit(toks)
        if not changed:
            return toks


L = list()
K = list()
for line in fileinput.input():
    L.append(tokenize(line.strip()))
    K.append(tokenize(line.strip()))


toks = L[0]

for l in L[1:]:
    toks = tadd(toks, l)
    toks = treduce(toks)

print("Part 1", tmagnitude(toks))

m = 0
for i in range(len(K)):
    for j in range(len(K)):
        if i == j:
            continue
        v = tmagnitude(treduce(tadd(K[i], K[j])))
        m = max(v, m)

print("Part 2", m)
