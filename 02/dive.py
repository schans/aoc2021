#!/usr/bin/env python

import fileinput

# counters
depth = 0
x = 0

for line in fileinput.input():
    (move, amount) = line.strip().split()
    amount = int(amount)
    if move == 'up':
        depth -= amount
    elif move == 'down':
        depth += amount
    elif move == 'forward':
        x += amount
    else:
        print(f"Unknown move {move}")


print(f"Depht: {depth} x: {x}: mul: {depth*x}")
