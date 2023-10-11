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

    VALUE_OPTIONS = tuple(range(1, 10))

    array: np.ndarray | None

    def __init__(self, puzzle=None, *, validate=False):
        self.log = logging.getLogger()

        self.array = self._interpret_array_repr(puzzle)

        if validate:
            self.validate_board()

    @staticmethod
    def _interpret_array_repr(puzzle: str | list | None) -> np.ndarray:
        if isinstance(puzzle, SudokuBoard):
            return puzzle.array.copy()
        elif isinstance(puzzle, np.ndarray):
            return puzzle.copy()
        elif isinstance(puzzle, list):
            return np.array(puzzle, dtype=np.uint8)
        elif isinstance(puzzle, str):
            return np.array([int(n) for n in puzzle], dtype=np.uint8).reshape((9, 9))
        elif puzzle is None:
            return np.zeros((9, 9), dtype=np.uint8)
        else:
            raise ValueError(f"Invalid sudoku input type '<{type(puzzle)}>'")

    def validate_board(self):
        puzzle_iterator = np.nditer(self.array, order="C", flags=["multi_index"])
        for cell in puzzle_iterator:
            cell_value = int(cell)
            row, col = puzzle_iterator.multi_index

            self.array[row, col] = 0
            if not self.is_valid_cell_value(row, col, cell_value):
                raise ValueError(f"value '{cell_value}' in position {(row, col)} is invalid.")
            self.array[row, col] = cell_value

    def is_valid_cell_value(self, row: int, col: int, val: int):
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

    def _neighbours(self, row: int, col: int):
        """
        Find the neighbouring cells for a chosen cell on a Sudoku board.
            Yield a generator of each value in the neighbours.

        Args:
            row: The row coordinate
            col: The column coordinate

        Yields:
            tuple[int, int], int: A row, col coordinate tuple and the value at those coordinates
        """
        # Iterate down the column
        for _row in range(SudokuBoard.HEIGHT):
            if _row != row:
                yield (_row, col), self.array[_row, col]

        # Iterate across the row
        for _col in range(SudokuBoard.WIDTH):
            if _col != col:
                yield (row, _col), self.array[row, _col]

        # Iterate through the 3x3 box
        box_row_origin, box_col_origin = SudokuBoard.get_box_origin(row, col)
        for row_diff in range(SudokuBoard.BOX_HEIGHT):
            for col_diff in range(SudokuBoard.BOX_WIDTH):
                _row, _col = box_row_origin + row_diff, box_col_origin + col_diff
                if (_row, _col) == (row, col):
                    continue

                yield (_row, _col), self.array[_row, _col]

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
        return SudokuBoard(self)

    def by_index(self, idx):
        return self.array[idx // 9, idx % 9]
