#!/usr/bin/env python

import fileinput

from heapq import heappop, heappush
import heapq


expand = 1  # part 1
expand = 5  # part 2

O = list()
G = list()

for line in fileinput.input():
    O.append([int(i) for i in line.strip()])

# expand
for i in range(expand):
    for x in range(len(O)):
        r = list()
        for j in range(expand):
            for y in range(len(O[0])):
                v = O[x][y] + j + i
                if v > 9:
                    v -= 9
                r.append(v)
        G.append(r)


def solve(G):
    h = len(G)
    w = len(G[0])

    # initial costs
    W = [[1e6 for x in range(w)] for y in range(h)]
    W[0][0] = G[0][0]

    changed = True
    while changed:
        changed = False
        for x in range(w):
            for y in range(h):
                for (dx, dy) in [(-1, 0), (0, -1), (1, 0), (0, 1)]:
                    xx = x + dx
                    yy = y + dy
                    if 0 <= xx < w and 0 <= yy < h:
                        if W[xx][yy] + G[x][y] < W[x][y]:
                            W[x][y] = W[xx][yy] + G[x][y]
                            changed = True
    return W[-1][-1] - W[0][0]


def dijkstra(start, end, G):
    queue = [(0, start)]
    seen = set()

    h = len(G)
    w = len(G[0])

    while queue:
        c, state = heappop(queue)
        if state in seen:
            continue
        seen.add(state)

        if state == end:
            return c

        x, y = state
        for (dx, dy) in [(-1, 0), (0, -1), (1, 0), (0, 1)]:
            xx = x + dx
            yy = y + dy
            if 0 <= xx < w and 0 <= yy < h:
                heappush(queue, (c+G[xx][yy], (xx, yy)))

    raise ValueError("end not found")


start = (0, 0)
end = (len(G)-1, len(G[0])-1)
# print(f"Shortest path (expand:{expand}) ", solve(G))
print(f"Shortest path (expand:{expand}) ", dijkstra(start, end, G))
