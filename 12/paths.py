#!/usr/bin/env python

import fileinput

paths = 0
N = dict()
for line in fileinput.input():
    (p, c) = line.strip().split('-')
    if p not in N:
        N[p] = list()
    if c not in N:
        N[c] = list()
    N[p].append(c)
    N[c].append(p)


def traverse(n, part2=False, path=[], double=''):
    global paths
    path.append(n)

    if n == 'end':
        paths += 1
        return

    for c in sorted(N[n]):
        if c == 'start':
            continue
        if not c.lower() in path:
            traverse(c, part2, path.copy(), double)
        elif part2 and double == '':
            traverse(c, part2, path.copy(), c)


traverse('start')
print("Part 1:", paths)
paths = 0
traverse('start', part2=True)
print("Part 2:", paths)
