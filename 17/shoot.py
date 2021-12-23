#!/usr/bin/env python

import fileinput

xmin = xmax = ymin = ymax = 0

for line in fileinput.input():
    _, coords = line.strip().split(': ')

    xstr, ystr = coords.split(', ')
    xmin, xmax = [int(i) for i in xstr.split('=')[1].split('..')]
    ymin, ymax = [int(i) for i in ystr.split('=')[1].split('..')]


def shoot(vx, vy):
    global xmin, xmax, ymin, ymax
    x = y = maxh = 0

    while True:
        x += vx
        y += vy

        if vx > 0:
            vx -= 1
        elif vx < 0:
            vx += 1

        vy -= 1
        if y > maxh:
            maxh = y

        # stopped early
        if vx == 0 and x < xmin:
            return -1

        # overshoot
        if x > xmax:
            return -1

        # dropped below
        if y < ymin:
            return -1

        # hit
        if xmin <= x <= xmax and ymin <= y <= ymax:
            return maxh


maxh = -1
c = 0
for vx in range(0, xmax+1):
    for vy in range(ymin-1, 1000):
        h = shoot(vx, vy)
        if h > -1:
            c += 1
        if h > maxh:
            maxh = h

print("Part 1:", maxh)
print("Part 2:", c)
