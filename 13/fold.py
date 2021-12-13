#!/usr/bin/env python

import fileinput


P = set()
F = list()


for line in fileinput.input():
    cur = line.strip()
    if cur == "":
        continue
    if not line.startswith('fold'):
        p = [int(i) for i in line.split(',')]
        P.add((p[0], p[1]))
    else:
        (axis, n) = line.split()[-1].split('=')
        n = int(n)
        Q = set()
        for x, y in P:
            if axis == 'y':
                if y < n:
                    Q.add((x, y))
                else:
                    Q.add((x, n - (y-n)))
            elif axis == 'x':
                if x < n:
                    Q.add((x, y))
                else:
                    Q.add((n - (x-n), y))
        P = Q

print(f"Part 1:", len(P))

maxx = max([x for x, _ in P])
maxy = max([y for _, y in P])
print("Part 2:")
for y in range(maxy+1):
    for x in range(maxx+1):
        if (x, y) in P:
            print('#', end="")
        else:
            print(' ', end="")
    print()
