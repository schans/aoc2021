#!/usr/bin/env python

import fileinput
# import sys
# sys.setrecursionlimit(10_000)

cost_min = 1e6

B = list()
COLS = 4
ROWS = 0
L = 0

C = [[] for i in range(COLS)]

for line in fileinput.input():
    line = line.strip().replace('#', '')
    if not line:
        continue
    if line.startswith('.'):
        B = ['.'] * len(line)
        L = len(line)
    else:
        for i, c in enumerate(line):
            C[i].append(c)
        ROWS += 1

# append rows to B
for i in range(COLS):
    for c in C[i]:
        B.append(c)

S = ROWS*COLS


def dump(B):
    print(f'#############')
    print(f'#{"".join(B[0:L])}#')
    for k in range(0, ROWS):
        print(f"###{B[L+k+0]}#{B[L+k+ROWS]}#{B[L+k+2*ROWS]}#{B[L+k+3*ROWS]}###")
    print(f'  #########')


def solved(B):
    for k in range(0, COLS):
        for i in range(L+k*ROWS, L+(k+1)*ROWS):
            if B[i] != ['A', 'B', 'C', 'D'][k]:
                return False
    return True


def get_z(i):
    zi = i
    if i >= L:
        if 0 <= i-L < ROWS:
            zi = 2
        elif ROWS <= i-L < (2*ROWS):
            zi = 4
        elif (2*ROWS) <= i-L < (3*ROWS):
            zi = 6
        elif (3*ROWS) <= i-L < (4*ROWS):
            zi = 8
    return zi


def path_free(B, i, d):
    # "vertical" component
    zi = get_z(i)
    zd = get_z(d)

    # check obstructions
    for n in range(min(zi, zd)+1, max(zi, zd)):
        if B[n] != '.':
            # print(f"blocked by {B[n]} {n}")
            return False
    return True


def can_move_to_line(B, i, d):
    assert i >= L, "not a move col to line"
    assert d < L, "not a move col to line"

    # not above holes
    if d in [2, 4, 6, 8]:
        return False

    # not to wrong hole
    if (0 <= d-L < ROWS) and B[i] != 'A':
        return False
    if (ROWS <= d-L < 2*ROWS) and B[i] != 'B':
        return False
    if (2*ROWS <= d-L < 3*ROWS) and B[i] != 'C':
        return False
    if (3*ROWS <= d-L < 4*ROWS) and B[i] != 'D':
        return False

    return path_free(B, i, d)


def move(B, i, d) -> int:
    assert B[d] == '.', "tried to move to occupied slot"
    # cost factor
    c = 1
    if B[i] == 'B':
        c = 10
    elif B[i] == 'C':
        c = 100
    elif B[i] == 'D':
        c = 1000

    # calc cost
    zi = get_z(i)
    zd = get_z(d)
    dist = abs(zi - zd)

    # up
    if i >= L:
        k = (zi // 2) - 1
        top = L+k*ROWS
        dist += (i-top+1)

    # down
    if d >= L:
        k = (zd // 2) - 1
        top = L+k*ROWS
        dist += (d-top+1)

    # move
    B[d] = B[i]
    B[i] = '.'
    return c * dist


def get_top_col(B, k):
    m = list()
    c = ['A', 'B', 'C', 'D'][k]

    correct = True

    # bottom up
    top = L+k*ROWS
    bottom = L+(k+1)*ROWS
    for i in range(bottom-1, top-1, -1):
        if B[i] != '.':
            m.append(i)
            if B[i] != c:
                correct = False

    if correct:
        # empty or all correct
        return None

    # top one
    return m[-1]


def can_move_to_col(B, i, k):
    m = list()
    c = ['A', 'B', 'C', 'D'][k]

    if B[i] != c:
        return - 1

    correct = True

    # bottom up
    top = L+k*ROWS
    bottom = L+(k+1)*ROWS
    for j in range(bottom-1, top-1, -1):
        if B[j] != '.':
            m.append(j)
            if B[j] != c:
                correct = False

    # not empty or contains wrong one
    if not correct:
        return -1

    # one above top one
    d = bottom - len(m) - 1
    if not path_free(B, i, d):
        return -1

    return bottom - len(m) - 1


def get_movers(B, last):
    m = set()

    # line
    for i in range(L):
        if B[i] != '.':
            m.add(i)

    # top of cols
    for k in range(0, COLS):
        r = get_top_col(B, k)
        if r:
            m.add(r)

    # remove last
    if not last is None:
        m.discard(last)

    # order cheapest first
    n = list()
    for c in ['A', 'B', 'C', 'D']:
        for k in m:
            if B[k] == c:
                n.append(k)
    return n


def get_moves(B, i):
    m = set()

    # correct column for B[i]
    k = ['A', 'B', 'C', 'D'].index(B[i])

    # move from line to correct hole
    r = can_move_to_col(B, i, k)
    if r > 0:
        return [r]

    # moves from hole to line
    l = len(B) - S
    if i >= l:
        for d in range(l):
            if B[d] == '.' and can_move_to_line(B, i, d):
                m.add(d)
        return m

    return []


def solve(B, cost, last):
    global cost_min

    if cost >= cost_min:
        return False

    if solved(B):
        print(f'Found solution with cost:', cost)
        cost_min = min(cost_min, cost)
        return True

    movers = get_movers(B, last)
    for n in movers:

        moves = get_moves(B, n)
        for m in moves:
            BC = B.copy()
            c = move(BC, n, m)
            solve(BC, cost + c, m)  # the one in the dest is the one last moved
    return True


solve(B, 0, None)

print(f"Answer: {cost_min}")
