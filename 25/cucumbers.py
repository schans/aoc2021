#!/usr/bin/env python

import fileinput

E = set()
D = set()

R = C = 0

r = 0
for line in fileinput.input():

    for c, ch in enumerate(line.strip()):
        if ch == '>':
            E.add((r, c))
        elif ch == 'v':
            D.add((r, c))
    r += 1

R = r
C = len(line.strip())


def dump():
    global E, D, R, C
    for r in range(R):
        s = ""
        for c in range(C):
            if (r, c) in E:
                s += ">"
            elif (r, c) in D:
                s += "v"
            else:
                s += '.'
        print(s)


step = 0
while True:

    identical = True

    # move east
    NE = set()
    for (r, c) in E:
        cc = (c+1) % C
        if not (r, cc) in D and not (r, cc) in E:
            NE.add((r, cc))
        else:
            NE.add((r, c))
    if len(E-NE):
        identical = False
    E = NE

    # move down
    ND = set()
    for (r, c) in D:
        rr = (r+1) % R
        if not (rr, c) in E and not (rr, c) in D:
            ND.add((rr, c))
        else:
            ND.add((r, c))
    if len(D-ND):
        identical = False
    D = ND

    step += 1

    if identical:
        break

print("Part 1:", step)
