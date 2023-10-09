import unittest
from sudoku_solver.sudoku import Sudoku, Board


class TestBoard(unittest.TestCase):
    def setUp(self) -> None:
        self.board = Board()


class TestSudoku(unittest.TestCase):
    def setUp(self) -> None:
        self.sudoku = Sudoku()

        ex1 = [
            ['5', '3', ' ', ' ', '7', ' ', ' ', ' ', ' '],
            ['6', ' ', ' ', '1', '9', '5', ' ', ' ', ' '],
            [' ', '9', '8', ' ', ' ', ' ', ' ', '6', ' '],
            ['8', ' ', ' ', ' ', '6', ' ', ' ', ' ', '3'],
            ['4', ' ', ' ', '8', ' ', '3', ' ', ' ', '1'],
            ['7', ' ', ' ', ' ', '2', ' ', ' ', ' ', '6'],
            [' ', '6', ' ', ' ', ' ', ' ', '2', '8', ' '],
            [' ', ' ', ' ', '4', '1', '9', ' ', ' ', '5'],
            [' ', ' ', ' ', ' ', '8', ' ', ' ', '7', '9']
        ]
        ex2 = [
            [' ', ' ', '6', '3', ' ', ' ', ' ', '7', ' '],
            [' ', ' ', '1', '7', ' ', ' ', '3', ' ', '9'],
            [' ', ' ', ' ', ' ', '9', ' ', '2', ' ', ' '],
            [' ', ' ', ' ', ' ', ' ', ' ', ' ', '1', ' '],
            [' ', ' ', ' ', '9', ' ', ' ', ' ', ' ', '7'],
            [' ', '9', '7', ' ', '5', ' ', ' ', ' ', ' '],
            [' ', '8', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
            [' ', '3', ' ', ' ', '6', '2', '5', ' ', ' '],
            [' ', '1', ' ', ' ', ' ', '8', ' ', '6', ' ']
        ]
        ex3 = [
            [' ', '1', '3', ' ', ' ', '7', ' ', ' ', '6'],
            [' ', ' ', ' ', ' ', ' ', ' ', ' ', '2', '4'],
            [' ', '5', ' ', '8', ' ', ' ', ' ', '7', ' '],
            [' ', ' ', ' ', '9', ' ', '8', '7', ' ', ' '],
            ['4', '7', ' ', ' ', ' ', ' ', ' ', '5', ' '],
            ['5', ' ', ' ', '6', '7', ' ', ' ', ' ', ' '],
            [' ', ' ', ' ', ' ', ' ', ' ', '9', ' ', '2'],
            ['7', ' ', '6', ' ', '3', ' ', '8', ' ', ' '],
            [' ', ' ', '1', ' ', '2', ' ', ' ', ' ', ' ']
        ]
        ex4 = [
            ['4', ' ', ' ', '8', ' ', '5', ' ', ' ', '9'],
            [' ', ' ', '5', ' ', ' ', ' ', ' ', '8', '6'],
            [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
            [' ', '7', ' ', ' ', ' ', '9', '5', ' ', ' '],
            ['3', ' ', ' ', ' ', '5', ' ', ' ', ' ', ' '],
            [' ', ' ', '6', ' ', '7', ' ', '1', ' ', ' '],
            [' ', '3', ' ', ' ', ' ', ' ', ' ', ' ', '4'],
            ['5', ' ', ' ', ' ', '3', '7', '2', ' ', ' '],
            [' ', '6', ' ', '9', ' ', ' ', ' ', ' ', ' ']
        ]

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
        #         print(f"{'-' * 20} Solutions {'-' * 20}")
        #         for solution in game_inst.solutions:
        #             print(f"New Solution:")
        #             print(solution)
        #
        #     game_gui.draw_board()
        #
        # pygame.quit()

    def test_interpret_puzzle_repr(self):
        with self.subTest('None'):
            pass

        with self.subTest('str'):
            pass

        with self.subTest('list'):
            pass

    def test_str(self):
        pass

    def test_repr(self):
        pass

