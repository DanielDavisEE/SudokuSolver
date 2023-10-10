import unittest
from unittest import mock

import numpy as np

from sudoku_solver.sudoku import Sudoku


class TestSudoku(unittest.TestCase):
    def setUp(self) -> None:
        self.sudoku = Sudoku()

        self.unsolved_puzzle_1 = np.array(
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
        self.solved_puzzle_1 = np.array(
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
        self.sudoku = Sudoku(self.unsolved_puzzle_1)
        mock_sudoku_solver = mock.MagicMock()
        mock_sudoku_solver.solve.side_effect = lambda x: x
        self.sudoku.solver = mock_sudoku_solver

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

        # # pygame.key.set_repeat(1000, 100)
        #
        # game_gui = BoardGUI()
        # game_inst = Sudoku(game_gui=game_gui, puzzle=ex4, isMain=True)
        #
        # game_inst.solve_puzzle_fast_init()
        #
        # running, solving, solved = True, True, False
        #
        # game_gui.draw_board()
        #
        # while running:
        #     pygame.time.delay(10)
        #     for event in pygame.event.get():
        #         if event.type == KEYDOWN and event.key == K_ESCAPE:
        #             running = False
        #         if event.type == pygame.QUIT:
        #             running = False
        #
        #     if solving:
        #         solving, move = game_inst.solve_puzzle_fast_step()
        #         if move is not None:
        #             value, row, col = move
        #             game_inst.game_gui.set_value(row, col, value)
        #             print(move)
        #             # print(game_inst.puzzle)
        #         if not solving:
        #             solved = True
        #
        #     if solved:
        #         solved = False
        #         print(f"{'-' * 20} Solutions {'-' * 20`}")
        #         for solution in game_inst.solutions:
        #             print(f"New Solution:")
        #             print(solution)
        #
        #     game_gui.draw_board()
        #
        # pygame.quit()

    def test_interpret_puzzle_repr(self):
        with self.subTest("None"):
            sudoku = Sudoku()
            self.assertEqual(sudoku.puzzle, None)

        with self.subTest("str"):
            sudoku = Sudoku("".join(self.unsolved_puzzle_1.astype(str).reshape(-1)))
            self.assertEqual(sudoku.puzzle.tolist(), self.unsolved_puzzle_1.tolist())

        with self.subTest("list"):
            sudoku = Sudoku(self.unsolved_puzzle_1)
            self.assertListEqual(
                sudoku.puzzle.tolist(), self.unsolved_puzzle_1.tolist()
            )

    def test_str(self):
        self.assertEqual(
            str(self.sudoku),
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
            repr(self.sudoku), "".join(self.sudoku.puzzle.astype(str).reshape(-1))
        )

    def test_get_box_origin(self):
        self.assertEqual(Sudoku.get_box_origin(0, 0), (0, 0))
        self.assertEqual(Sudoku.get_box_origin(3, 3), (3, 3))
        self.assertEqual(Sudoku.get_box_origin(8, 4), (6, 3))
        self.assertEqual(Sudoku.get_box_origin(5, 2), (3, 0))
        self.assertEqual(Sudoku.get_box_origin(7, 0), (6, 0))

        self.assertRaises(ValueError, Sudoku.get_box_origin, 9, 1)
        self.assertRaises(ValueError, Sudoku.get_box_origin, 1, 10)
        self.assertRaises(ValueError, Sudoku.get_box_origin, -1, 1)
        self.assertRaises(ValueError, Sudoku.get_box_origin, 1, -2)

    def test_create_solved_puzzle(self):
        with mock.patch("numpy.random.shuffle", side_effect=lambda x: x):
            empty_puzzle = [list(range(1, 10))] + [[0] * 9] * 8
            self.assertListEqual(
                self.sudoku.create_solved_puzzle().tolist(), empty_puzzle
            )
