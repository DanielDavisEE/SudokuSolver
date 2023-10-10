import logging

import numpy as np

from sudoku_solver.sudoku_solvers import BacktrackSudokuSolver

logging.basicConfig(level=logging.DEBUG)


class Sudoku:
    WIDTH = 9
    HEIGHT = 9
    SHAPE = (WIDTH, HEIGHT)
    N_CELLS = WIDTH * HEIGHT

    BOX_WIDTH = 3
    BOX_HEIGHT = 3
    BOX_SHAPE = (BOX_WIDTH, BOX_HEIGHT)
    BOX_N_CELLS = BOX_WIDTH * BOX_HEIGHT

    def __init__(self, puzzle=None):
        self.log = logging.getLogger()

        self.puzzle: np.array | None = self._interpret_puzzle_repr(puzzle)
        self.solver = BacktrackSudokuSolver()

    @staticmethod
    def get_box_origin(row: int, col: int) -> tuple[int, int]:
        """Get the coordinates of the box which contains the input cell

        Args:
            row: The row coordinate of a cell
            col: The col coordinate of a cell

        Returns:
            The row, col coordinates of the top left corner of the box
        """
        if not (0 <= row < 9) or not (0 <= col < 9):
            raise ValueError(f"({row}, {col}) is not a valid coordinate.")
        return (row // 3) * 3, (col // 3) * 3

    @staticmethod
    def _interpret_puzzle_repr(puzzle: str | list | None):
        if isinstance(puzzle, list):
            puzzle_array = np.array(puzzle)
            puzzle_array[puzzle_array == " "] = 0
            return puzzle_array
        elif isinstance(puzzle, str):
            return np.array([int(x) for x in puzzle]).reshape((9, 9))
        else:
            return puzzle

    def __repr__(self):
        return "".join(self.puzzle.astype(str).reshape(-1))

    def __str__(self):
        h_line = f"+{'-' * 23}+"
        row_template = "| {} {} {} | {} {} {} | {} {} {} |"

        row_strings = []
        for i, line in enumerate(self.puzzle):
            if i % 3 == 0:
                row_strings.append(h_line)

            row_strings.append(row_template.format(*line))

        row_strings.append(h_line)

        return "\n".join(row_strings)

    def solve(self):
        return self.solver.solve(self.puzzle)

    def create_solved_puzzle(self):
        # Create blank board
        puzzle = np.zeros((9, 9), dtype=np.uint8)

        # Randomly fill in the first layer
        puzzle[0, :] = np.arange(1, 10)
        np.random.shuffle(puzzle[0, :])

        # Fill in the rest of the board
        return self.solver.solve(puzzle)

    # def _multiple_solutions(self):
    #     solving = True
    #     while solving:
    #         solving, move = self.solve_puzzle_fast_step()
    #         print(solving, move)
    #
    #     self.log.debug('Number of Solutions Found:', len(self.solutions))
    #     # [print(x.__repr__()) for x in self.solutions]
    #     self._action_list = []
    #     return len(self.solutions) == 1

    def generate_puzzle(self):
        puzzle_solution = self.create_solved_puzzle()

        # self.log.debug('Solved Puzzle:')
        # self.log.debug(puzzle_solution)
        #
        # # Remove random numbers from the board until a puzzle with multiple solutions
        # #    is generated.
        # i = 0
        # self.solve_puzzle_fast_init()
        # self.log.debug('entering loop')
        # while self._multiple_solutions() and i < 81:
        #     random_row, random_col = random.randint(0, 8), random.randint(0, 8)
        #     old_num = self._original_puzzle[random_row][random_col]
        #
        #     while old_num == ' ':
        #         random_row, random_col = random.randint(0, 8), random.randint(0, 8)
        #         old_num = self._original_puzzle[random_row][random_col]
        #
        #     # self.original_puzzle[random_row][random_col] = ' '
        #     key = (int(old_num), random_row, random_col)
        #     self.log.debug(key)
        #
        #     # for row in self.rows_info.keys():
        #     # self.rows_info[row] = self.rows_info[row][0], None
        #     # for i, row in enumerate(self.constraints_info):
        #     # if key in row[2] or key in row[3]:
        #     # print(i, row)
        #     self.log.debug(i)
        #     self.back_step(permanent=True, sub_key=(int(old_num), random_row, random_col))
        #     self.log.debug(self.original_puzzle)
        #     # if i == 0:
        #     # print(self.original_puzzle)
        #     # a1, b1, c1 = self.constraints_matrix, self.rows_info, self.constraints_info
        #
        #     # for i, row in enumerate(c1):
        #     # print(i, row)
        #
        #     # for k, v in b1.items():
        #     # print(k, v)
        #     i += 1
        #     yield random_row, random_col, ' '
        # self.log.debug('Left loop')
        #
        # # Replace the most recently removed number
        # self.original_puzzle[random_row][random_col] = old_num
        #
        # yield random_row, random_col, old_num
        #
        # self.log.debug('Finished Puzzle:')
        # self.log.debug(self.original_puzzle)
        # self.puzzle = self.original_puzzle.copy()


if __name__ == "__main__":
    sudoku_inst = Sudoku()
