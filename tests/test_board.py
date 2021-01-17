from Py2048.board import addRandomPiece, buildBoard, up
import unittest
import numpy as np

class TestBoard(unittest.TestCase):
    def test_buildBoard(self):
        # can build a standard 4x4 board
        board = buildBoard()
        self.assertEqual(np.count_nonzero(board), 1)
        self.assertTupleEqual(board.shape, (4, 4))

        # can build funny board sizes
        board = buildBoard((10, 3))
        self.assertEqual(np.count_nonzero(board), 1)
        self.assertTupleEqual(board.shape, (10, 3))

        # can control the rng
        board = buildBoard(rng=np.random.RandomState(0))
        self.assertTrue(np.all(
            board == np.array([
                [0, 0, 0, 0],
                [0, 1, 0, 0],
                [0, 0, 0, 0],
                [0, 0, 0, 0],
            ])
        ))

    def test_addRandomPiece(self):
        rng = np.random.RandomState(0)
        board = buildBoard(rng=rng)

        # can add a random piece to an empty square
        success = addRandomPiece(board, rng)
        self.assertTrue(success)

        self.assertTrue(np.all(
            board == np.array([
                [0, 0, 0, 0],
                [0, 1, 0, 0],
                [0, 0, 0, 0],
                [1, 0, 0, 0],
            ])
        ))

        # can fill board
        for _ in range(14):
            success = addRandomPiece(board, rng)
            self.assertTrue(success)

        self.assertTrue(np.all(
            board == np.array([
                [1, 1, 1, 1],
                [1, 1, 2, 1],
                [1, 1, 1, 1],
                [1, 1, 1, 1],
            ])
        ))

        # attempting to add another piece just returns False
        # and does not change board state
        self.assertFalse(addRandomPiece(board, rng))
        self.assertTrue(np.all(
            board == np.array([
                [1, 1, 1, 1],
                [1, 1, 2, 1],
                [1, 1, 1, 1],
                [1, 1, 1, 1],
            ])
        ))

    def test_up(self):
        # one per col
        board = np.array([
            [1, 0, 0, 0],
            [0, 1, 0, 0],
            [0, 0, 1, 0],
            [0, 0, 0, 1],
        ], dtype='int64')
        up(board)

        self.assertTrue(np.all(
            board == np.array([
                [1, 1, 1, 1],
                [0, 0, 0, 0],
                [0, 0, 0, 0],
                [0, 0, 0, 0],
            ])
        ))

        # simple merge
        board = np.array([
            [1, 0, 0, 0],
            [1, 1, 0, 0],
            [0, 0, 0, 0],
            [0, 0, 0, 0],
        ], dtype='int64')
        up(board)

        self.assertTrue(np.all(
            board == np.array([
                [2, 1, 0, 0],
                [0, 0, 0, 0],
                [0, 0, 0, 0],
                [0, 0, 0, 0],
            ])
        ))

        # triple
        board = np.array([
            [1, 0, 0, 0],
            [1, 0, 0, 0],
            [0, 0, 1, 0],
            [1, 0, 0, 1],
        ], dtype='int64')
        up(board)

        self.assertTrue(np.all(
            board == np.array([
                [2, 0, 1, 1],
                [1, 0, 0, 0],
                [0, 0, 0, 0],
                [0, 0, 0, 0],
            ])
        ))

        # quad
        board = np.array([
            [1, 0, 0, 0],
            [1, 1, 0, 0],
            [1, 0, 1, 0],
            [1, 0, 0, 1],
        ], dtype='int64')
        up(board)

        self.assertTrue(np.all(
            board == np.array([
                [2, 1, 1, 1],
                [2, 0, 0, 0],
                [0, 0, 0, 0],
                [0, 0, 0, 0],
            ])
        ))

        # complex
        board = np.array([
            [1, 0, 1, 1],
            [2, 1, 0, 0],
            [1, 1, 1, 0],
            [2, 0, 2, 1],
        ], dtype='int64')
        up(board)

        self.assertTrue(np.all(
            board == np.array([
                [1, 2, 2, 2],
                [2, 0, 2, 0],
                [1, 0, 0, 0],
                [2, 0, 0, 0],
            ])
        ))
