import unittest
from unittest import mock

from sudoku_solver.sudoku import SudokuBoard
from sudoku_solver.sudoku_solvers import (BacktrackSudokuSolver, DancingChainsSudokuSolver, SudokuSolver)


class TestSudokuSolver(unittest.TestCase):
    def setUp(self) -> None:
        class _SudokuSolver(SudokuSolver):
            def solve(self, puzzle: SudokuBoard) -> SudokuBoard:
                super().solve(puzzle)

                return puzzle

        self.solver = _SudokuSolver()

    def test_create_solved_puzzle(self):
        with mock.patch("numpy.random.shuffle", side_effect=lambda x: x):
            empty_puzzle = [list(range(1, 10))] + [[0] * 9] * 8
            self.assertListEqual(
                self.solver.create_solved_puzzle().tolist(), empty_puzzle
            )


class TestBacktrackSudokuSolver(unittest.TestCase):
    def setUp(self) -> None:
        self.empty_puzzle = SudokuBoard()
        self.unsolved_puzzle = SudokuBoard(
            [
                [5, 3, 0, 0, 7, 0, 0, 0, 0],
                [6, 0, 0, 1, 9, 5, 0, 0, 0],
                [0, 9, 8, 0, 0, 0, 0, 6, 0],
                [8, 0, 0, 0, 6, 0, 0, 0, 3],
                [4, 0, 0, 8, 0, 3, 0, 0, 1],
                [7, 0, 0, 0, 2, 0, 0, 0, 6],
                [0, 6, 0, 0, 0, 0, 2, 8, 0],
                [0, 0, 0, 4, 1, 9, 0, 0, 5],
                [0, 0, 0, 0, 8, 0, 0, 7, 9],
            ]
        )
        self.solved_puzzle = SudokuBoard(
            [
                [5, 3, 4, 6, 7, 8, 9, 1, 2],
                [6, 7, 2, 1, 9, 5, 3, 4, 8],
                [1, 9, 8, 3, 4, 2, 5, 6, 7],
                [8, 5, 9, 7, 6, 1, 4, 2, 3],
                [4, 2, 6, 8, 5, 3, 7, 9, 1],
                [7, 1, 3, 9, 2, 4, 8, 5, 6],
                [9, 6, 1, 5, 3, 7, 2, 8, 4],
                [2, 8, 7, 4, 1, 9, 6, 3, 5],
                [3, 4, 5, 2, 8, 6, 1, 7, 9],
            ]
        )

        self.solver = BacktrackSudokuSolver()

    def test_solve(self):
        with self.subTest('last step'):
            almost_solved_puzzle = self.solved_puzzle.copy()
            almost_solved_puzzle.array[4, 6] = 0
            solved_puzzle = self.solver.solve(almost_solved_puzzle)

            self.assertFalse(solved_puzzle is almost_solved_puzzle)
            self.assertTrue((solved_puzzle.array == self.solved_puzzle.array).all())

        with self.subTest('full solve'):
            self.assertTrue((self.solver.solve(self.unsolved_puzzle).array == self.solved_puzzle.array).all())


class TestDancingChainsSudokuSolver(unittest.TestCase):
    def setUp(self) -> None:
        self.sudoku = SudokuBoard()
        self.solver = DancingChainsSudokuSolver()
