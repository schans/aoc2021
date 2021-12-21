#!/usr/bin/env python

from collections import defaultdict
import fileinput

WIN = 1000
rolls = 0
pos = list()
score = defaultdict(int)


for line in fileinput.input():
    pos.append(int(line.strip()[-1])-1)


def deterministic_die():
    global rolls
    d = 1
    while True:
        yield d
        d %= 100
        d += 1
        rolls += 1


die = deterministic_die()
p = 0
while True:

    for _ in range(3):
        d = next(die)
        pos[p] += d

    pos[p] = pos[p] % 10
    score[p] += pos[p] + 1

    if score[p] >= WIN or score[1] >= WIN:
        break
    p = (p+1) % 2

rolls += 1
m = min(score.values())
print(f'{m} * {rolls} = {m*rolls}')
