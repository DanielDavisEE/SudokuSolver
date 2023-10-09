from dataclasses import dataclass

import numpy as np
import random
import logging
from abc import ABC, abstractmethod

logging.basicConfig(level=logging.DEBUG)



class SudokuSolver(ABC):
    def __init__(self):
        self.log = logging.getLogger(self.__class__.__name__)

        self._puzzle = None

        self._solutions = set()
        self._action_list = []

    @abstractmethod
    def solve(self, puzzle: np.array) -> np.array:
        self._puzzle = puzzle

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
        for _row in range(Sudoku.HEIGHT):
            if _row != row:
                yield (_row, col), self._puzzle[_row][col]

        # Iterate across the row
        for _col in range(Sudoku.WIDTH):
            if _col != col:
                yield (row, _col), self._puzzle[row][_col]

        # Iterate through the 3x3 box
        box_row_origin, box_col_origin = Sudoku.get_box_origin(row, col)
        for row_diff in range(Sudoku.BOX_HEIGHT):
            for col_diff in range(Sudoku.BOX_WIDTH):
                _row, _col = box_row_origin + row_diff, box_col_origin + col_diff
                if (_row, _col) == (row, col):
                    continue

                yield (_row, _col), self._puzzle[_row][_col]


class BacktrackSudokuSolver(SudokuSolver):
    """
    A simple sudoku solver which uses trial and error with backtracking to find a solution
    to a given puzzle. Very lightweight, but not very fast.
    """
    def _check_validity(self, row: int, col: int, val: int):
        if (self._puzzle[row, :] == val).any():
            return False

        if (self._puzzle[:, col] == val).any():
            return False

        box_row_origin, box_col_origin = (row // 3) * 3, (col // 3) * 3
        if (self._puzzle[box_row_origin:box_row_origin + 3,
            box_col_origin:box_col_origin + 3] == val).any():
            return False

        return True

    def solve(self, puzzle: np.array):
        """A backtracking algorithm for solving a sudoku puzzle
        """
        super().solve(puzzle)
        
        idx = 0
        while (puzzle == 0).any():
            row, col = idx // 9, idx % 9

            # Find the next empty cell
            while puzzle[row, col]:
                idx += 1

            # Find the next valid value for this cell
            cell_value = puzzle[row, col] + 1
            while cell_value <= 10 and not self._check_validity(row, col, cell_value):
                cell_value += 1

            # Backtrack if we run out of valid options
            if cell_value > 9:
                puzzle[row, col] = 0
                idx -= 1
                continue

            puzzle[row, col] = cell_value

        return puzzle


class DancingChainsSudokuSolver(SudokuSolver):
    def __init__(self):
        super().__init__()

        # Create global data
        self.constraints_info, self.rows_info, self.constraints_matrix = self._create_constraints_matrix()
        self.best_constraints, self.best_actions = [], []  # Stores persistent info about future actions

        # log global data
        # self.log.debug('constraints_info:', self.constraints_info)
        # self.log.debug('rows_info:', self.rows_info)
        # self.log.debug('constraints_matrix:', self.constraints_matrix)

        # for row in self.constraints_matrix.keys():
        # self.log.debug(f"{row} ({self.rows_info[row]}): {self.constraints_matrix[row]}")

    def _create_constraints_matrix(self, cell_count=81, constraints_count=324):

        # constraints matrix which defines which constraints each row fulfills
        matrix = {}
        # Visibility, number of rows which satisfy constraint, rows which satisfy constraint
        constraints_info = [[True, 0, set(), set()] for _ in range(constraints_count)]
        # Visibility of rows
        rows_info = {}

        for cell_index in range(cell_count):
            for possibility in range(1, 10):
                # Each cell contains two bools, referring to the status re the
                #     constraint and its visibility
                k = (possibility, cell_index // 9, cell_index % 9)  # Define matrix keys

                # Define constraint details for each key
                constraints_satisfied = [
                    k[1] * 9 + k[2],
                    k[1] * 9 + (k[0] - 1) + cell_count * 1,
                    k[2] * 9 + (k[0] - 1) + cell_count * 2,
                    ((k[1] // 3) * 3 + k[2] // 3) * 9 + (k[0] - 1) + cell_count * 3
                ]

                matrix[k] = [False for _ in range(constraints_count)]
                for c in constraints_satisfied:
                    matrix[k][c] = True
                    constraints_info[c][1] += 1
                    constraints_info[c][2].add(k)
                matrix[k] = tuple(matrix[k])

                # Visibility of each constraint matrix row, defaults to True
                #    and which other key they were eliminated by
                rows_info[k] = True, None

        return constraints_info, rows_info, matrix

    def _init_solve(self):
        # Input preset values
        puzzle_iterator = np.nditer(self._puzzle, order='C', flags=['multi_index'])
        for cell_value in puzzle_iterator:
            if not cell_value:
                continue

            # self.log.debug(f"Coords: ({i}, {j}). Value: {int(value)}")
            self._remove_rows(cell_value, puzzle_iterator.multi_index, permanent=True)
    def solve(self, puzzle: np.array):
        super().solve(puzzle)
        
        self._init_solve()

    def _remove_rows(self, k, permanent=False):
        """ Remove all rows which satisfy a constraint also satisfied by k
        """
        self[k[1]][k[2]] = str(k[0])
        if not permanent:
            if self._action_list:
                self._action_list[-1][1].add(k)
            self._action_list.append((k, set()))

        row_k = self.constraints_matrix[k]
        # Iterate through the constraints that are satisfied by row_k
        for icol, isConstraint in enumerate(row_k):
            if isConstraint:

                self.constraints_info[icol][0] = False

                # Examine column for constraint 'icol'
                for secondary_k, secondary_row in self.constraints_matrix.items():
                    if secondary_row[icol]:
                        # Check if row is currently visible
                        if self.rows_info[secondary_k][0]:
                            self.rows_info[secondary_k] = False, k

                            # Decrement constraint satisfied count and move key
                            #     from available set to unavailable set
                            for jcol, secondaryConstraint in enumerate(secondary_row):
                                if secondaryConstraint:
                                    self.constraints_info[jcol][1] -= 1
                                    self.constraints_info[jcol][2].remove(secondary_k)
                                    self.constraints_info[jcol][3].add(secondary_k)

    def _back_step(self, permanent=False, sub_key=None):
        """ Add the rows removed by the most recent action in the action_list
        """

        def find_constraints(k):
            cell_count = 81
            constraints_satisfied = [
                k[1] * 9 + k[2],
                k[1] * 9 + (k[0] - 1) + cell_count * 1,
                k[2] * 9 + (k[0] - 1) + cell_count * 2,
                ((k[1] // 3) * 3 + k[2] // 3) * 9 + (k[0] - 1) + cell_count * 3
            ]
            return constraints_satisfied

        if not permanent:
            if not self._action_list:
                return False, None

            previous_action = self._action_list.pop()
            key, children = previous_action[0], previous_action[1]
            self[key[1]][key[2]] = ' '
        else:
            key, children = sub_key, []
            self.original_puzzle[key[1]][key[2]] = ' '

        row_k = self.constraints_matrix[key]
        # Iterate through the constraints that are satisfied by row_k
        for icol, isConstraint in enumerate(row_k):
            if isConstraint:

                self.constraints_info[icol][0] = True

                # Examine column for constraint 'icol'
                for secondary_k, secondary_row in self.constraints_matrix.items():
                    if secondary_row[icol]:
                        # Check that the key was hidden by the current key but isn't the current key
                        if not self.rows_info[secondary_k][0]:

                            primary_constraints = find_constraints(key)
                            secondary_constraints = find_constraints(secondary_k)
                            unique_constraints = [c for c in secondary_constraints if c not in primary_constraints]
                            valid = sum(self.constraints_info[c][0] for c in unique_constraints) == len(
                                unique_constraints)
                            if key == secondary_k and not permanent:
                                valid = False

                            if valid:
                                # if permanent or (self.rows_info[secondary_k][1] == key and secondary_k != key):
                                self.rows_info[secondary_k] = True, None

                                # Increment constraint satisfied count and move key
                                #     from unavailable set to available set
                                for jcol in find_constraints(
                                        secondary_k):  # , secondaryConstraint in enumerate(secondary_row):
                                    if secondary_row[jcol]:
                                        self.constraints_info[jcol][1] += 1
                                        self.constraints_info[jcol][2].add(secondary_k)
                                        self.constraints_info[jcol][3].remove(secondary_k)
        # Reset the status of the child actions
        for child in children:
            if permanent:
                self.log.debug("How'd I get here?", child)
            row_child = self.constraints_matrix[child]

            self.rows_info[child] = True, None
            for icol, isConstraint in enumerate(row_child):
                if isConstraint:
                    self.constraints_info[icol][1] += 1
                    self.constraints_info[icol][2].add(child)
                    self.constraints_info[icol][3].remove(child)

        self.best_constraints, self.best_actions = [], []

        _, row, col = key

        return True, (' ', row, col)

    def solve_puzzle_fast_step(self, generateRandom=False):
        """A dancing links algoritm for solving a sudoku puzzle
        """

        constraints_info = self.constraints_info
        constraints_matrix = self.constraints_matrix
        action_list = self._action_list
        rows_info = self.rows_info

        record = sum(c[0] for c in constraints_info)
        # self.log.debug(f"Available constraint options: {record}")

        best_constraints = self.best_constraints

        if not best_constraints:  # If no previous options are stored, find new best

            visible_constraints = [i for i, c in enumerate(constraints_info) if c[0]]

            # Choose the first visible constraint
            if visible_constraints:
                best_constraints = [visible_constraints[0]]
            else:
                # If no constraints are available then the puzzle is solved
                # self.log.debug('Solution found')
                self.solutions.add(self.puzzle.copy())

                if generateRandom:
                    return False, None
                else:
                    optionsAvailable, move = self.back_step()
                    return optionsAvailable, move

            for i in visible_constraints:
                if constraints_info[i][1] < constraints_info[best_constraints[0]][1]:
                    best_constraints = [i]
                elif constraints_info[i][1] == constraints_info[best_constraints[0]][1]:
                    best_constraints.append(i)

        # Select the next action from the chosen constraint. If no possible actions
        #     then back track the last action
        best_actions = self.best_actions

        if not best_actions:
            best_constraint = best_constraints.pop()

            if constraints_info[best_constraint][1] != 0:
                best_actions = list(constraints_info[best_constraint][2])
            else:
                # self.log.debug("Can't find viable option.")
                optionsAvailable, move = self.back_step()
                if not optionsAvailable:
                    # self.log.debug('No more solutions available.')
                    return optionsAvailable, move

        if best_actions:
            if generateRandom:
                best_action = random.choice(best_actions)
                best_actions.remove(best_action)
            else:
                best_action = best_actions.pop()

            value, row, col = best_action
            move = best_action

            self._remove_rows((int(value), row, col))

        return True, move


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
        return (row // 3) * 3, (col // 3) * 3

    @staticmethod
    def _interpret_puzzle_repr(puzzle: str | list | None):
        if isinstance(puzzle, list):
            puzzle_array = np.array(puzzle)
            puzzle_array[puzzle_array == ' '] = 0
            return puzzle_array
        elif isinstance(puzzle, str):
            return np.array(list(puzzle)).reshape((9, 9))
        else:
            return puzzle

    def __repr__(self):
        return ''.join([''.join(row) for row in self.puzzle])

    def __str__(self):
        h_line = f"+{'-' * 23}+\n"
        row_template = "| {} {} {} | {} {} {} | {} {} {} |\n"

        puzzle_str = ''
        for i, line in enumerate(self.puzzle):
            if i % 3 == 0:
                puzzle_str += h_line

            puzzle_str += row_template.format(*line)

        return puzzle_str + h_line

    def solve(self):
        return self.solver.solve(self.puzzle)

    def create_solved_puzzle(self):
        # Create blank board
        puzzle = np.zeros((9, 9), dtype=np.uint8)

        # Randomly fill in the first layer
        puzzle[0, :] = np.arange(1, 10)
        np.random.shuffle(self.puzzle[0, :])

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


if __name__ == '__main__':
    sudoku_inst = Sudoku()
