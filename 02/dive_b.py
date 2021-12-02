#!/usr/bin/env python

import fileinput

# counters
depth = 0
x = 0
aim = 0

for line in fileinput.input():
    (move, amount) = line.strip().split()
    amount = int(amount)
    if move == 'up':
        aim -= amount
    elif move == 'down':
        aim += amount
    elif move == 'forward':
        x += amount
        depth += (aim * amount)
    else:
        print(f"Unknown move {move}")


print(f"Depht: {depth} x: {x}: mul: {depth*x}")
