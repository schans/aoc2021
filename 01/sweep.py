#!/usr/bin/env python

import fileinput

# counters
c_incr = 0
c_isum = 0

# store prev values
psum = None
prev = None
pprev = None
for line in fileinput.input():
    cur = int(line.strip())
    if prev and cur > prev:
        c_incr += 1
    if pprev:
        csum = cur + prev + pprev
        if psum and csum > psum:
            c_isum += 1
        psum = csum
    pprev = prev
    prev = cur

print(f"Increases: {c_incr} Sum increases: {c_isum}")
