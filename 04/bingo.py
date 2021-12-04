#!/usr/bin/env python

import fileinput

numbers = None
boards = list()
board = None

for line in fileinput.input():
    cur = line.strip()

    if not numbers:
        numbers = [int(i) for i in cur.split(",")]
    else:
        if cur == "":
            if board:
                boards.append(board)
            board = list()
        else:
            nums = [int(i) for i in cur.split()]
            board.extend(nums)
# append last board
boards.append(board)


def printb(board):
    for i, n in enumerate(board):
        print(f"{n:02d} ", end="")
        if not (i+1) % 5:
            print()


def printa(boards):
    for board in boards:
        printb(board)
        print()


def play(boards, num):
    for board in boards:
        for i, n in enumerate(board):
            if n == num:
                board[i] = -1


def check(board) -> bool:
    for i in range(0, 5):
        row_s = 0
        col_s = 0
        for j in range(0, 5):
            row_s += board[(i*5 + j)]
            col_s += board[(i + j*5)]
        if row_s == -5 or col_s == -5:
            return True
    return False


def check_any(boards) -> int:
    for cur, board in enumerate(boards):
        if check(board):
            return cur
    return None


def check_last(boards, left) -> int:
    b = set()
    for i in left:
        if check(boards[i]):
            b.add(i)
        if len(left-b) == 0:
            return left-b, i
    return left-b, i


def sumb(boards, num):
    s = 0
    for n in boards[num]:
        if n > 0:
            s += n
    return s


print(f"Numbers: {numbers}: num boards: {len(boards)}")
# printa(boards)


left = set(range(0, len(boards)))
win_b = None
win_l = None
first = True
for n in numbers:
    play(boards, n)
    if not win_b and first:
        win_b = check_any(boards)
    else:
        win = n
        if first:
            print(f"Bingo board: {win_b}!")
            first = False
            # printa(boards)
            sum = sumb(boards, win_b)
            print(f"sum: {sum} win:{win} => {sum*win}")
    (left, win_b) = check_last(boards, left)
    if len(left) == 0:
        win = n
        print(f"Bingo last board: {win_b}!")
        # printa(boards)
        sum = sumb(boards, win_b)
        print(f"sum: {sum} win:{win} => {sum*win}")
        break
