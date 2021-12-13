#!/usr/bin/env python

import fileinput


P = set()
F = list()


for line in fileinput.input():
    cur = line.strip()
    if cur == "":
        continue

    if line.startswith('fold'):
        (line, nr) = line.split()[-1].split('=')
        F.append((line, int(nr)))
    else:
        p = [int(i) for i in line.split(',')]
        P.add((p[0], p[1]))

for (a, n) in F:
    Q = set()

    for x, y in P:
        if a == 'y':
            if y < n:
                Q.add((x, y))
            else:
                Q.add((x, n - (y-n)))
        elif a == 'x':
            if x < n:
                Q.add((x, y))
            else:
                Q.add((n - (x-n), y))
    P = Q

maxx = maxy = 0
for x, y in P:
    if x > maxx:
        maxx = x
    if y > maxy:
        maxy = y

print(f"Part 1:", len(P))
print("Part 2:")
for y in range(maxy+1):
    for x in range(maxx+1):
        if (x, y) in P:
            print('#', end="")
        else:
            print('.', end="")
    print()
