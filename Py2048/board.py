import numpy as np
from numba import njit
from typing import Tuple

def buildBoard(size: Tuple[int, int] = (4, 4), rng = np.random):
    board = np.zeros(size, dtype='int64')
    addRandomPiece(board, rng)

    return board

def getEmptyCoords(board: np.ndarray):
    return np.argwhere(board == 0)

def addRandomPiece(board: np.ndarray, rng = np.random):
    value = rng.choice([1, 2], p = [.9, .1])

    empty = getEmptyCoords(board)

    if len(empty) == 0:
        return False

    idx = rng.randint(len(empty))
    coord = tuple(empty[idx])

    board[coord] = value
    return True

@njit(cache=True)
def collapse(arr: np.ndarray, forward: bool):
    if np.all(arr == 0):
        return arr

    size = len(arr)

    last = -1
    last_idx = 0 if forward else size - 1
    last_zero = last_idx

    it = range(size) if forward else range(size - 1, -1, -1)

    for j in it:
        if arr[j] == 0:
            continue

        if arr[j] == last:
            v = arr[j]
            arr[j] = 0
            arr[last_idx] = v + 1
            last_idx = j
            last = -1

        else:
            v = arr[j]
            arr[j] = 0
            arr[last_zero] = v
            last = v
            last_idx = last_zero

            if forward:
                last_zero += 1
            else:
                last_zero -= 1

    return arr

@njit(cache=True)
def up(board: np.ndarray):
    for i in range(board.shape[1]):
        col = board[:, i]
        board[:, i] = collapse(col, forward=True)

    return board

@njit(cache=True)
def down(board: np.ndarray):
    for i in range(board.shape[1]):
        col = board[:, i]
        board[:, i] = collapse(col, forward=False)

    return board

@njit(cache=True)
def left(board: np.ndarray):
    for i in range(board.shape[0]):
        row = board[i]
        board[i] = collapse(row, forward=True)

    return board

@njit(cache=True)
def right(board: np.ndarray):
    for i in range(board.shape[0]):
        row = board[i]
        board[i] = collapse(row, forward=False)

    return board

@njit(cache=True)
def canCollapse(arr: np.ndarray):
    if np.any(arr == 0):
        return True

    last = -1
    for j in range(len(arr)):
        if last == arr[j]:
            return True

        last = arr[j]

    return False

def canUp(board: np.ndarray):
    return np.any([canCollapse(board[:, i]) for i in range(board.shape[1])])

def canDown(board: np.ndarray):
    return canUp(board)

def canLeft(board: np.ndarray):
    return np.any([canCollapse(board[i]) for i in range(board.shape[0])])

def canRight(board: np.ndarray):
    return canLeft(board)

def score(board: np.ndarray):
    return np.sum(board)

def highBlock(board: np.ndarray):
    return np.max(board)
