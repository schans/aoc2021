#!/usr/bin/env python

from collections import defaultdict
import fileinput

WIN = 21
pos = list()
wins = [0, 0]

for line in fileinput.input():
    pos.append(int(line.strip()[-1])-1)
# print("init", pos)

# offset 3
DIE_WEIGHTS = [1, 3, 6, 7, 6, 3, 1]
DIE_LEN = len(DIE_WEIGHTS)


def play_round(offset0, offset1, weight_off=1, score_off0=0, score_off1=0):
    global DIE_WEIGHTS, DIE_LEN, WIN, wins

    for i in range(DIE_LEN):
        score0 = score_off0
        weight0 = weight_off

        pos0 = offset0 + i + 3  # dice offset
        pos0 %= 10
        score0 += pos0 + 1  # base0
        weight0 *= DIE_WEIGHTS[i]

        if score0 >= WIN:
            wins[0] += weight0
            continue

        for j in range(DIE_LEN):
            score1 = score_off1
            weight1 = weight0

            pos1 = offset1 + j + 3  # dice offset
            pos1 %= 10
            score1 += pos1 + 1  # base0
            weight1 *= DIE_WEIGHTS[j]

            if score1 >= WIN:
                wins[1] += weight1
                continue

            # no winner yet, play another round
            play_round(pos0, pos1, weight1, score0, score1)


play_round(pos[0], pos[1])


# print(wins)
print("Part 2:", max(wins))
