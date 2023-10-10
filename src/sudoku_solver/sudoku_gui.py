import pygame
import pygame.locals as py_locals

from sudoku_solver.sudoku import SudokuBoard
from sudoku_solver.sudoku_solvers import SudokuSolver
from sudoku_solver.utils import MyGUI

pygame.init()


class SudokuGUI(MyGUI):
    """

    """
    TILE_DIM = 2
    BOARD_DIM = TILE_DIM * 9 + 0.1 * 10 + 0.1 * 2

    def __init__(self, puzzle: SudokuBoard = None, solver: SudokuSolver = None):
        if not pygame.font:
            raise ImportError("Fonts not imported")

        window_size = win_width, win_height = (int(self.BASE_UNIT * (self.BOARD_DIM + 2)),
                                               int(self.BASE_UNIT * (self.BOARD_DIM + 10)))
        super().__init__("Sudoku Solver", window_size)

        self.sudoku_state = puzzle
        if self.sudoku_state is None:
            self.sudoku_state = SudokuBoard()

        self.solver = solver

        self.GUI_state = {
            'generating': False,
            'solving': False,
            'display_solutions': False
        }

        self.init_puzzle_page()

    def init_puzzle_page(self):

        # Children of Window
        header_block_info = {
            'name': 'header_block',
            'parent': 'window',
            'dimensions': (self.BOARD_DIM + 2, 4),
            'coordinates': (0, 0),
            'colour': 'bg_color'
        }
        board_block_info = {
            'name': 'board_block',
            'parent': 'window',
            'dimensions': (self.BOARD_DIM + 2, self.BOARD_DIM + 2),
            'coordinates': (0, 4),
            'colour': 'bg_color'
        }
        nav_block_info = {
            'name': 'nav_block',
            'parent': 'window',
            'dimensions': (self.BOARD_DIM + 2, 4),
            'coordinates': (0, self.BOARD_DIM + 6),
            'colour': 'bg_color'
        }

        # Children of Header Block
        title_block_info = {
            'name': 'title_block',
            'parent': 'header_block',
            'dimensions': (self.BOARD_DIM, 2),
            'coordinates': (1, 1),
            'colour': 'title_colour'
        }

        # Children of Board Block
        tile_board_info = {
            'name': 'tile_board',
            'parent': 'board_block',
            'dimensions': (self.BOARD_DIM, self.BOARD_DIM),
            'coordinates': (1, 1),
            'colour': 'board_colour'
        }

        # Children of Nav Block
        test_button_info = {
            'name': 'test_button',
            'parent': 'nav_block',
            'dimensions': (4, 2),
            'coordinates': ((self.BOARD_DIM + 2 - 4) / 2, 1),
            'colour': 'tile_colour'
        }

        self.create_block(**header_block_info)
        self.create_block(**title_block_info)
        self.create_block(**board_block_info)
        self.create_block(**tile_board_info)
        self.create_block(**nav_block_info)

        self.create_button(pygame.quit, **test_button_info)

        self.create_cells()
        self.set_board()

        self.create_text('title_text', 'Sudoku', 'title_block', 'white', 50)

    def run(self):
        running = True

        self.draw_board()

        pygame.key.set_repeat(1000, 100)
        while running:
            pygame.time.delay(100)
            for event in pygame.event.get():
                if event.type == py_locals.KEYDOWN and event.key == py_locals.K_ESCAPE:
                    running = False
                if event.type == pygame.QUIT:
                    running = False
                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_pos = event.pos  # gets mouse position

                    # checks if mouse position is over the button
                    for button_name, button_rect, button_func in self.button_list:

                        if button_rect.collidepoint(mouse_pos):
                            # Calls relevant function
                            button_func()

            # if self.GUI_state['solving']:
            #     self.GUI_state['solving'], move = self.backend.solve_puzzle_fast_step()
            #     if move is not None:
            #         value, row, col = move
            #         self.set_value(row, col, value)
            #
            #     # Print solutions if puzzle has just been solved
            #     if not self.GUI_state['solving']:
            #         print(f"{'-' * 20} Solutions {'-' * 20}")
            #         print(type(self.backend.solutions), len(self.backend.solutions))
            #         for solution in self.backend.solutions:
            #             print(f"New Solution: {type(solution)}")
            #             print(solution)
            #         self.GUI_state['display_solutions'] = True
            #
            # if self.GUI_state['display_solutions']:
            #     pass
            self.draw_board()

        pygame.quit()

    # -------------------------- Manipulate Cells ----------------------------

    def create_cells(self):

        tile_info_dict = {
            'parent': 'tile_board',
            'dimensions': (self.TILE_DIM, self.TILE_DIM),
            'colour': 'tile_colour'
        }

        for row in range(9):
            for col in range(9):
                # Create tile
                name = f'tile {row}{col}'
                coordinates = [n * (self.TILE_DIM + 0.1) + (n // 3) * 0.1 + 0.1 for n in (col, row)]
                tile_info_dict['name'] = name
                tile_info_dict['coordinates'] = coordinates
                tile_info = self.create_block(**tile_info_dict)

                # Create text
                number_font = pygame.font.Font(None, 50)
                number_text = number_font.render(' ', 1, (0, 0, 0))
                coords = [int(n * self.BASE_UNIT // 2) for n in tile_info_dict['dimensions']]
                number_pos = (number_text.get_rect(centerx=coords[0],
                    centery=coords[1]))

                self.text_list[f'{row}{col}'] = [number_text, number_pos, name]

    def set_board(self):
        for row in range(SudokuBoard.HEIGHT):
            for col in range(SudokuBoard.WIDTH):

                text_value = str(self.sudoku_state.array[row, col])
                if text_value == '0':
                    text_value = ' '

                self.set_value(row, col, text_value)

    def set_value(self, row, col, value=None):
        if value is None:
            value = ' '

        tile_dimensions = self.block_list[f'tile {row}{col}'].dimensions

        font = pygame.font.Font(None, 50)
        text = font.render(str(value), 1, (0, 0, 0))
        self.text_list[f'{row}{col}'][0] = text

    # -------------------------- Button Functions ----------------------------

    def generate_new_puzzle(self):
        self.sudoku_state = SudokuBoard()
        self.set_board()
        for key in self.GUI_state.keys():
            self.GUI_state[key] = False
        self.GUI_state['generating'] = True

    def solve_puzzle(self):
        self.GUI_state['solving'] = True

    def next_solution(self):
        pass

    def prev_solution(self):
        pass

    def enter_number(self, position):
        """lambda: self.enter_number((row, col))"""
        pass


def main():
    ex = [
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

    gui_inst = SudokuGUI()
    gui_inst.run()


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

if __name__ == '__main__':
    main()
