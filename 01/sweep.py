#!/usr/bin/env python

import fileinput

# counters
incr = 0
incrsum = 0

# store prev values
prevsum = None
prev = None
prevprev = None
for line in fileinput.input():
    cur = int(line.strip())
    if prev:
        if cur > prev:
            incr += 1
    if prevprev:
        sum = cur + prev + prevprev
        if prevsum:
            if sum > prevsum:
                incrsum += 1
        prevsum = sum
    prevprev = prev
    prev = cur

print(f"Increases: {incr} Sum increases: {incrsum}")
