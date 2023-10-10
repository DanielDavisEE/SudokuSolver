import logging

import numpy as np

logging.basicConfig(level=logging.DEBUG)


class SudokuBoard:
    WIDTH = 9
    HEIGHT = 9
    SHAPE = (WIDTH, HEIGHT)
    N_CELLS = WIDTH * HEIGHT

    BOX_WIDTH = 3
    BOX_HEIGHT = 3
    BOX_SHAPE = (BOX_WIDTH, BOX_HEIGHT)
    BOX_N_CELLS = BOX_WIDTH * BOX_HEIGHT

    array: np.ndarray | None

    def __init__(self, puzzle=None, *, validate=False):
        self.log = logging.getLogger()

        self.array = self._interpret_puzzle_repr(puzzle)

        if validate:
            self.validate_board()

    @staticmethod
    def _interpret_puzzle_repr(puzzle: str | list | None) -> np.ndarray:
        if isinstance(puzzle, SudokuBoard):
            return puzzle.array.copy()
        elif isinstance(puzzle, list):
            return np.array(puzzle)
        elif isinstance(puzzle, str):
            return np.array([int(n) for n in puzzle]).reshape((9, 9))
        elif puzzle is None:
            return np.zeros((9, 9))
        else:
            raise ValueError(f"Invalid sudoku input type '<{type(puzzle)}>'")

    def validate_board(self):
        puzzle_iterator = np.nditer(self.array, order="C", flags=["multi_index"])
        for cell in puzzle_iterator:
            cell_value = int(cell)
            row, col = puzzle_iterator.multi_index

            self.array[row, col] = 0
            if not self.check_validity(row, col, cell_value):
                raise ValueError(f"value '{cell_value}' in position {(row, col)} is invalid.")
            self.array[row, col] = cell_value

    def check_validity(self, row: int, col: int, val: int):
        if (self.array[row, :] == val).any():
            return False

        if (self.array[:, col] == val).any():
            return False

        box_row_origin, box_col_origin = (row // 3) * 3, (col // 3) * 3
        box = self.array[
              box_row_origin:box_row_origin + 3,
              box_col_origin:box_col_origin + 3]
        if (box == val).any():
            return False

        return True

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

    def __repr__(self):
        if self.array is None:
            return "No array"
        return "".join(self.array.astype(str).reshape(-1))

    def __str__(self):
        h_line = f"+{'-' * 23}+"
        row_template = "| {} {} {} | {} {} {} | {} {} {} |"

        row_strings = []
        for i, line in enumerate(self.array):
            if i % 3 == 0:
                row_strings.append(h_line)

            row_strings.append(row_template.format(*line))

        row_strings.append(h_line)

        return "\n".join(row_strings)

    def tolist(self):
        return self.array.tolist()

    def copy(self):
        return self.array.copy()
