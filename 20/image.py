#!/usr/bin/env python

import fileinput

ITERS = 50  # 2 for part 1
A = set()
M = set()

k = 0
minx = maxx = miny = maxy = 0
for line in fileinput.input():
    line = line.strip()
    if line == "":
        continue

    if not len(A):
        i = 0
        for c in line:
            if c == '#':
                A.add(i)
            i += 1
    else:
        i = 0
        for c in line:
            if c == '#':
                M.add((k, i))
                if i > maxy:
                    maxy = i
            i += 1

        k += 1

maxx = k-1


flipper = False
if 0 in A and not 511 in A:
    # image gets reversed each step
    flipper = True
    # print("Image flipper")

for iter in range(ITERS):
    N = set()
    flipped = iter % 2

    for x in range(minx-1, maxx+2):
        for y in range(miny-1, maxy+2):
            s = ""
            for dx in [-1, 0, 1]:
                for dy in [-1, 0, 1]:
                    if (x+dx, y+dy) in M:
                        if flipper:
                            s += str((iter+1) % 2)
                        else:
                            s += '1'
                    else:
                        if flipper:
                            s += str(iter % 2)
                        else:
                            s += '0'
            i = int(s, 2)
            added = False

            if iter % 2 or not flipper:
                if i in A:
                    N.add((x, y))
                    added = True
            else:
                if not i in A:
                    N.add((x, y))
                    added = True

            if added:
                if x > maxx:
                    maxx = x
                elif x < minx:
                    minx = x
                if y > maxy:
                    maxy = y
                elif y < miny:
                    miny = y
    M = N

print("Answer : ", len(M))
