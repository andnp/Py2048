import numpy as np
from Py2048.board import addRandomPiece, buildBoard, canLeft, canUp, down, left, right, up, score

class Actions:
    UP = 0
    RIGHT = 1
    DOWN = 2
    LEFT = 3

class Game:
    def __init__(self, size=(4, 4), additive=False, rng=np.random):
        self.size = size
        self.rng = rng
        self.additive = additive

        self.done = False
        self.board = buildBoard(self.size, self.rng)

    def takeAction(self, act: int):
        if self.done:
            raise Exception('The game has already ended')

        if act == Actions.UP:
            up(self.board)
        elif act == Actions.RIGHT:
            right(self.board)
        elif act == Actions.DOWN:
            down(self.board)
        elif act == Actions.LEFT:
            left(self.board)

        else:
            raise Exception(f"Unexpected action taken: {act}")

        self.done = False

        # if I couldn't add a piece
        # then check if I can take anymore moves
        success = addRandomPiece(self.board, self.rng)
        if not success:
            # this is expensive to check, so only check when needed
            if len(self.availableActions()) == 0:
                self.done = True

        return self.done

    def getBoard(self) -> np.ndarray:
        if self.additive:
            return self.board.copy()

        p = np.power(2, self.board)
        return np.where(p > 1, p, np.zeros_like(p))

    def availableActions(self):
        acts = []
        if canUp(self.board):
            acts += [Actions.UP, Actions.DOWN]

        if canLeft(self.board):
            acts += [Actions.LEFT, Actions.RIGHT]

        return acts

    def getScore(self):
        return score(self.getBoard())

    def copy(self):
        new_game = Game(self.size, self.rng)
        new_game.board = self.board.copy()

        return new_game

    def __str__(self):
        return str(self.getBoard())
