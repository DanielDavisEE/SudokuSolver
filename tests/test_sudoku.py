import unittest

import numpy as np

from sudoku_solver.sudoku import SudokuBoard


class TestSudokuBoard(unittest.TestCase):
    def setUp(self) -> None:
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

        # ex1 = [
        #     ["5", "3", " ", " ", "7", " ", " ", " ", " "],
        #     ["6", " ", " ", "1", "9", "5", " ", " ", " "],
        #     [" ", "9", "8", " ", " ", " ", " ", "6", " "],
        #     ["8", " ", " ", " ", "6", " ", " ", " ", "3"],
        #     ["4", " ", " ", "8", " ", "3", " ", " ", "1"],
        #     ["7", " ", " ", " ", "2", " ", " ", " ", "6"],
        #     [" ", "6", " ", " ", " ", " ", "2", "8", " "],
        #     [" ", " ", " ", "4", "1", "9", " ", " ", "5"],
        #     [" ", " ", " ", " ", "8", " ", " ", "7", "9"],
        # ]
        # ex2 = [
        #     [" ", " ", "6", "3", " ", " ", " ", "7", " "],
        #     [" ", " ", "1", "7", " ", " ", "3", " ", "9"],
        #     [" ", " ", " ", " ", "9", " ", "2", " ", " "],
        #     [" ", " ", " ", " ", " ", " ", " ", "1", " "],
        #     [" ", " ", " ", "9", " ", " ", " ", " ", "7"],
        #     [" ", "9", "7", " ", "5", " ", " ", " ", " "],
        #     [" ", "8", " ", " ", " ", " ", " ", " ", " "],
        #     [" ", "3", " ", " ", "6", "2", "5", " ", " "],
        #     [" ", "1", " ", " ", " ", "8", " ", "6", " "],
        # ]
        # ex3 = [
        #     [" ", "1", "3", " ", " ", "7", " ", " ", "6"],
        #     [" ", " ", " ", " ", " ", " ", " ", "2", "4"],
        #     [" ", "5", " ", "8", " ", " ", " ", "7", " "],
        #     [" ", " ", " ", "9", " ", "8", "7", " ", " "],
        #     ["4", "7", " ", " ", " ", " ", " ", "5", " "],
        #     ["5", " ", " ", "6", "7", " ", " ", " ", " "],
        #     [" ", " ", " ", " ", " ", " ", "9", " ", "2"],
        #     ["7", " ", "6", " ", "3", " ", "8", " ", " "],
        #     [" ", " ", "1", " ", "2", " ", " ", " ", " "],
        # ]
        # ex4 = [
        #     ["4", " ", " ", "8", " ", "5", " ", " ", "9"],
        #     [" ", " ", "5", " ", " ", " ", " ", "8", "6"],
        #     [" ", " ", " ", " ", " ", " ", " ", " ", " "],
        #     [" ", "7", " ", " ", " ", "9", "5", " ", " "],
        #     ["3", " ", " ", " ", "5", " ", " ", " ", " "],
        #     [" ", " ", "6", " ", "7", " ", "1", " ", " "],
        #     [" ", "3", " ", " ", " ", " ", " ", " ", "4"],
        #     ["5", " ", " ", " ", "3", "7", "2", " ", " "],
        #     [" ", "6", " ", "9", " ", " ", " ", " ", " "],
        # ]

    def test_interpret_array_repr(self):
        with self.subTest("None"):
            sudoku = SudokuBoard()
            self.assertListEqual(sudoku.tolist(), [[0] * 9] * 9)

        with self.subTest("str"):
            sudoku = SudokuBoard(repr(self.unsolved_puzzle))
            self.assertListEqual(sudoku.tolist(), self.unsolved_puzzle.tolist())

        with self.subTest("list"):
            sudoku = SudokuBoard(self.unsolved_puzzle.tolist())
            self.assertListEqual(
                sudoku.array.tolist(), self.unsolved_puzzle.tolist()
            )

    def test_str(self):
        self.assertEqual(
            str(self.unsolved_puzzle),
            """+-----------------------+
| 5 3 0 | 0 7 0 | 0 0 0 |
| 6 0 0 | 1 9 5 | 0 0 0 |
| 0 9 8 | 0 0 0 | 0 6 0 |
+-----------------------+
| 8 0 0 | 0 6 0 | 0 0 3 |
| 4 0 0 | 8 0 3 | 0 0 1 |
| 7 0 0 | 0 2 0 | 0 0 6 |
+-----------------------+
| 0 6 0 | 0 0 0 | 2 8 0 |
| 0 0 0 | 4 1 9 | 0 0 5 |
| 0 0 0 | 0 8 0 | 0 7 9 |
+-----------------------+""",
        )

    def test_repr(self):
        self.assertEqual(
            repr(self.unsolved_puzzle), "".join(self.unsolved_puzzle.array.astype(str).reshape(-1))
        )
        self.assertEqual(
            repr(self.solved_puzzle), "".join(self.solved_puzzle.array.astype(str).reshape(-1))
        )

    def test_get_box_origin(self):
        self.assertEqual(SudokuBoard.get_box_origin(0, 0), (0, 0))
        self.assertEqual(SudokuBoard.get_box_origin(3, 3), (3, 3))
        self.assertEqual(SudokuBoard.get_box_origin(8, 4), (6, 3))
        self.assertEqual(SudokuBoard.get_box_origin(5, 2), (3, 0))
        self.assertEqual(SudokuBoard.get_box_origin(7, 0), (6, 0))

        self.assertRaises(ValueError, SudokuBoard.get_box_origin, 9, 1)
        self.assertRaises(ValueError, SudokuBoard.get_box_origin, 1, 10)
        self.assertRaises(ValueError, SudokuBoard.get_box_origin, -1, 1)
        self.assertRaises(ValueError, SudokuBoard.get_box_origin, 1, -2)

    def test_check_validity(self):
        with self.subTest('correct_values'):
            puzzle_iterator = np.nditer(self.unsolved_puzzle.array, order="C", flags=["multi_index"])
            for cell in puzzle_iterator:
                cell_value = int(cell)
                if cell_value:
                    continue

                row, col = puzzle_iterator.multi_index
                true_value = self.solved_puzzle.array[row, col]

                self.assertTrue(self.unsolved_puzzle.check_validity(row, col, true_value), f"{(row, col, int(cell_value))}")

        options = set(range(1, 10))
        with self.subTest('incorrect_values'):
            empty_puzzle = SudokuBoard()
            empty_puzzle.array[0, 0] = 5

            self.assertFalse(empty_puzzle.check_validity(0, 8, 5), f"{(0, 8, 5)}")
            self.assertFalse(empty_puzzle.check_validity(8, 0, 5), f"{(8, 0, 5)}")
            self.assertFalse(empty_puzzle.check_validity(1, 1, 5), f"{(1, 1, 5)}")

    def test_tolist(self):
        pass

    def test_copy(self):
        pass

    def test_by_index(self):
        sudoku = SudokuBoard(np.arange(81).reshape((9, 9)))
        for i in range(81):
            self.assertEqual(sudoku.by_index(i), i)
