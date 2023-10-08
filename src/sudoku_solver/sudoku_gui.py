import pygame
from pygame.locals import *
import utils

BASE_UNIT = 20
TILE_DIM = 2
BOARD_DIM = TILE_DIM * 9 + 0.1 * 10 + 0.1 * 2
pygame.init()


class Board():

    def __init__(self, isMain=False, backend=None, puzzle=None):
        if not pygame.font:
            raise ImportError("Fonts not imported")

        if isMain and backend is None:
            self.backend = GS(puzzle=puzzle)
        elif isMain:
            self.backend = backend

        self.isMain = isMain

        pygame.display.set_caption("Sudoku Solver")
        window_size = win_width, win_height = (int(BASE_UNIT * (BOARD_DIM + 2)),
                                               int(BASE_UNIT * (BOARD_DIM + 10)))
        self.window = pygame.display.set_mode(window_size)

        self.GUI_state = {
            'generating': False,
            'solving': False,
            'display_solutions': False
        }

        self.colours = {
            'bg_color': (230, 220, 205),
            'title_colour': (238, 201, 0),
            'board_colour': (105, 95, 80),
            'tile_colour': (134, 122, 102),
            'black': (0, 0, 0),
            'white': (255, 255, 255)
        }

        self.init_puzzle_page()

    def run_GUI(self):
        assert self.isMain

        running = True

        self.draw_board()

        pygame.key.set_repeat(1000, 100)
        while running:
            pygame.time.delay(100)
            for event in pygame.event.get():
                if event.type == KEYDOWN and event.key == K_ESCAPE:
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

            if self.GUI_state['solving']:
                self.GUI_state['solving'], move = self.backend.solve_puzzle_fast_step()
                if move is not None:
                    value, row, col = move
                    self.set_value(row, col, value)

                # Print solutions if puzzle has just been solved
                if not self.GUI_state['solving']:
                    print(f"{'-' * 20} Solutions {'-' * 20}")
                    print(type(self.backend.solutions), len(self.backend.solutions))
                    for solution in self.backend.solutions:
                        print(f"New Solution: {type(solution)}")
                        print(solution)
                    self.GUI_state['display_solutions'] = True

            if self.GUI_state['display_solutions']:
                pass
            self.draw_board()

        pygame.quit()

    def init_puzzle_page(self):
        self.block_list = myStorage.MyList('window', self.window)
        self.text_list = {}
        self.button_list = []

        # Children of Window
        header_block_info = {
            'name': 'header_block',
            'parent': 'window',
            'dimensions': (BOARD_DIM + 2, 4),
            'coordinates': (0, 0),
            'colour': 'bg_color'
        }
        board_block_info = {
            'name': 'board_block',
            'parent': 'window',
            'dimensions': (BOARD_DIM + 2, BOARD_DIM + 2),
            'coordinates': (0, 4),
            'colour': 'bg_color'
        }
        nav_block_info = {
            'name': 'nav_block',
            'parent': 'window',
            'dimensions': (BOARD_DIM + 2, 4),
            'coordinates': (0, BOARD_DIM + 6),
            'colour': 'bg_color'
        }

        # Children of Header Block
        title_block_info = {
            'name': 'title_block',
            'parent': 'header_block',
            'dimensions': (BOARD_DIM, 2),
            'coordinates': (1, 1),
            'colour': 'title_colour'
        }

        # Children of Board Block
        tile_board_info = {
            'name': 'tile_board',
            'parent': 'board_block',
            'dimensions': (BOARD_DIM, BOARD_DIM),
            'coordinates': (1, 1),
            'colour': 'board_colour'
        }

        # Children of Nav Block
        test_button_info = {
            'name': 'test_button',
            'parent': 'nav_block',
            'dimensions': (4, 2),
            'coordinates': ((BOARD_DIM + 2 - 4) / 2, 1),
            'colour': 'tile_colour'
        }

        self.create_block(**header_block_info)
        self.create_block(**title_block_info)
        self.create_block(**board_block_info)
        self.create_block(**tile_board_info)
        self.create_block(**nav_block_info)

        self.create_button(pygame.quit, **test_button_info)

        self.create_cells()

        self.create_text('title_text', 'Sudoku', 'title_block', 'white', 50)

    # -------------------------- Object Creation ----------------------------

    def create_button(self, function, name, parent, dimensions, coordinates, colour):
        # Coordinates need to be referenced from window, not parent surface
        parent_tmp = parent
        overall_coords = list(coordinates)
        while parent_tmp != 'window':
            overall_coords[0] += self.block_list[parent_tmp].coordinates[0]
            overall_coords[1] += self.block_list[parent_tmp].coordinates[1]
            parent_tmp = self.block_list[parent_tmp].parent

        # Create rect object for simplicity of collision detection
        button_rect = Rect([int(coord * BASE_UNIT) for coord in overall_coords],
                           [int(dim * BASE_UNIT) for dim in dimensions])
        self.button_list.append((name, button_rect, function))

        # Create surface as usual
        self.block_list.append(name, parent, dimensions, coordinates, colour)
        return self.block_list[name]

    def create_block(self, name, parent, dimensions, coordinates, colour):
        self.block_list.append(name, parent, dimensions, coordinates, colour)
        return self.block_list[name]

    def create_text(self, name, value, parent, colour, size):
        coords = [int(n * BASE_UNIT // 2) for n in self.block_list[parent].dimensions]
        font = pygame.font.Font(None, size)
        text = font.render(str(value), 1, self.colours[colour])
        pos = (text.get_rect(centerx=coords[0],
                             centery=coords[1]))
        self.text_list[name] = [text, pos, parent]

    def create_surface(self, block_info):
        block_size = [int(dim * BASE_UNIT) for dim in block_info.dimensions]

        block = pygame.Surface(block_size)
        block = block.convert()
        block.fill(self.colours[block_info.colour])
        block_info.surface = block

    def create_cells(self):

        tile_info_dict = {
            'parent': 'tile_board',
            'dimensions': (TILE_DIM, TILE_DIM),
            'colour': 'tile_colour'
        }

        for row in range(9):
            for col in range(9):
                # Create tile
                name = f'tile {row}{col}'
                coordinates = [n * (TILE_DIM + 0.1) + (n // 3) * 0.1 + 0.1 for n in (col, row)]
                tile_info_dict['name'] = name
                tile_info_dict['coordinates'] = coordinates
                tile_info = self.create_block(**tile_info_dict)

                # Create text
                number_font = pygame.font.Font(None, 50)
                number_text = number_font.render(' ', 1, (0, 0, 0))
                coords = [int(n * BASE_UNIT // 2) for n in tile_info_dict['dimensions']]
                number_pos = (number_text.get_rect(centerx=coords[0],
                                                   centery=coords[1]))

                self.text_list[f'{row}{col}'] = [number_text, number_pos, name]

                # -------------------------- Manipulate Cells ----------------------------

    def set_board(self, puzzle=None, blank=False):
        for row in range(9):
            for col in range(9):
                if blank:
                    self.set_value(row, col, ' ')
                else:
                    self.set_value(row, col, puzzle[row][col])

    def set_value(self, row, col, value=None):
        if value is None:
            value = ' '

        tile_dimensions = self.block_list[f'tile {row}{col}'].dimensions

        font = pygame.font.Font(None, 50)
        text = font.render(str(value), 1, (0, 0, 0))
        self.text_list[f'{row}{col}'][0] = text

    # -------------------------- Button Funcitons ----------------------------

    def generate_new_puzzle(self):
        self.set_board(blank=True)
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

    # -------------------------- GUI Drawing ----------------------------

    def blit_text(self):
        for name, text_object in self.text_list.items():
            text, position, parent = text_object
            self.block_list[parent].surface.blit(text, position)

    def draw_board(self):

        def draw_recurse(block_iter):
            try:
                block_name, block_info = next(block_iter)
            except StopIteration:
                self.blit_text()
                return True

            self.create_surface(block_info)

            draw_recurse(block_iter)

            parent_surface = self.block_list[block_info.parent].surface
            block_pos = [int(coord * BASE_UNIT) for coord in block_info.coordinates]
            parent_surface.blit(block_info.surface, block_pos)

        block_iter = iter(self.block_list)
        draw_recurse(block_iter)
        pygame.display.flip()


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

    game_inst = GS()

    game_inst.run_GUI()


if __name__ == '__main__':
    from sudoku import Sudoku as GS

    main()
