#!/usr/bin/env python

import fileinput

from collections import defaultdict

scans = dict()
matched = set()
locations = list()

scanner = 0
scans[scanner] = list()
for line in fileinput.input():
    line = line.strip()
    if not line:
        scanner += 1
        scans[scanner] = list()
        continue

    if line.startswith("--- scanner"):
        continue
    p = [int(i) for i in line.split(",")]
    scans[scanner].append((p[0], p[1], p[2]))


def rotate90(scanner):
    global scans
    # print("rotate")
    n = list()
    for (x, y, z) in scans[scanner]:
        n.append((x, z, -y))
    scans[scanner] = n


def flip(scanner):
    global scans
    # print("flip")
    n = list()
    for (x, y, z) in scans[scanner]:
        n.append((-x, -y, z))
    scans[scanner] = n


def translate(trans, scanner):
    global scans
    # print("trans", trans)
    n = list()
    for (x, y, z) in scans[scanner]:
        if trans == 'xy':
            n.append((y, -x, z))
        elif trans == 'yz':
            # plus rotate x->z
            n.append((z, x, y))
        elif trans == 'zx':
            # plus rotate
            n.append((-z, x, -y))
    scans[scanner] = n


def shift(diff, scanner):
    global scans
    # print("shift", diff)
    (dx, dy, dz) = diff
    n = list()
    for (x, y, z) in scans[scanner]:
        n.append((x + dx, y + dy, z+dz))
    scans[scanner] = n


def orientations(scanner):
    for trans in ['xy', 'yz', 'zx']:
        translate(trans, scanner)
        # flip
        for _ in range(2):
            flip(scanner)
            # up rotation
            for _ in range(4):
                rotate90(scanner)
                yield True


# zero is ref
matched.add(0)

done = False
while not done:

    found = set()
    for s in matched:
        for d in range(len(scans)):
            if s == d or d in matched:
                continue

            # for _ in orientations(d):
            #     if d in found:
            #         break

            for trans in ['xy', 'yz', 'zx']:
                if d in found:
                    break
                translate(trans, d)

                # flip
                for _ in range(2):
                    if d in found:
                        break
                    flip(d)

                    # up rotation
                    for _ in range(4):
                        rotate90(d)
                        mmap = defaultdict(int)
                        for i in scans[s]:
                            for j in scans[d]:
                                (xi, yi, zi) = i
                                (xj, yj, zj) = j
                                k = (xi-xj, yi-yj, zi - zj)
                                mmap[k] += 1
                        matches = [z for z in mmap if mmap[z] > 11]

                        if len(matches) > 0:
                            assert len(matches) == 1, "more than one match"
                            # print("Found match for:", d)
                            found.add(d)
                            locations.append(matches[0])
                            # shift grid to match
                            shift(matches[0], d)
                            break

    matched |= found
    if len(matched) == len(scans):
        # found all
        done = True


beacons = set()
for scanner in scans:
    for beacon in scans[scanner]:
        beacons.add(beacon)

max = 0
for i in locations:
    (xi, yi, zi) = i
    for j in locations:
        (xj, yj, zj) = j
        # Manhattan dist
        d = abs(xi-xj)+abs(yi-yj)+abs(zi-zj)
        if d > max:
            max = d

print("Part 1:", len(beacons))
print("Part 2:", max)
