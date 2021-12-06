#!/usr/bin/env python

from pprint import pprint
import fileinput

# age buckets
P = [0] * 10

for line in fileinput.input():
    cur = line.strip()
    for i in cur.split(","):
        P[int(i)] += 1


def calculate(days):
    for d in range(1, days+1):
        p0 = P[0]
        for i in range(0, 9):
            P[i] = P[i+1]
        # multiply
        P[6] += p0
        P[8] = p0
    return sum(P)


days = 80
print(f"Days: {days} fish: {calculate(days)}")
print(f"Days: 256 fish: {calculate(256-days)}")
