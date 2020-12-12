import time


class SudokuGame:
    """
    The SudokuGame class keeps track of the stats of the current game and solves the sudoku puzzle

    Parameters
    ----------
    grid: list
        2-Dimensional list containing the unsolved sudoku puzzle
    Attributes
    ----------
    start: float
        Handles the time when the object is created, 
        i.e., when the game starts.

    recursions: int
        Records the amount of recursions needed to 
        solve the puzzle

    end: float
        Handles the time when the game is finally solved

    grid: list
        Stores the unsolved puzzle in a 2-D list

    solved_grid: list
        Stores the solved puzzle in a 2-D list
    """

    def __init__(self, grid):
        self.start = time.time()
        self.recursions = 0
        self.end = 0
        self.grid = grid
        self.solved_grid = None

    @classmethod
    def load_grid(cls, file: str, grid_number: int):
        """
        Returns a 2-D list containing the sudoku puzzle to solve.

        Parameters
        ----------
        file: str
            txt file existing in the current working directory
        grid_number: int
            puzzle number
        """
        fhand = list(open(file))
        board = None
        grid = []
        if len(str(grid_number)) == 1:
            grid_number = '0' + str(grid_number)  # add 0 to 1-digit numbers (e.g. 01,02,etc.)
        else:
            grid_number = str(grid_number)

        # Iterate over lines in file
        for i, line in enumerate(fhand):

            # Check if line starts with Grid
            if line.startswith('Grid') and grid_number in line:
                board = fhand[i + 1:i + 10]  # select board
                break

        if board is None:
            return False  # handle unbound boards for invalid files

        # Create grid
        for i, lines in enumerate(board):
            lines = lines.strip('\n')
            grid.append([])  # adds a new row for each iteration
            for number in lines:
                grid[i].append(int(number))  # adds numbers to row

        return grid

    @staticmethod
    def find_blank_cell(board: list):
        """
        Returns tuple of the position for the first blank cell found.

        Parameters
        ----------
        board: list
            sudoku puzzle
        """

        for i in range(9):  # Iterate over rows
            for j in range(9):  # Iterate over columns
                if board[i][j] == 0:
                    return j, i

    @staticmethod
    def find_group(n: int):
        """
        Returns list of numbers representing the belonging group of the board

        Parameters
        ----------
        n: int
            value of x or y
        """
        group1, group2, group3 = [0, 1, 2], [3, 4, 5], [6, 7, 8]
        if n in group1:
            return group1
        elif n in group2:
            return group2
        else:
            return group3

    def find_solutions(self, board: list, x: int, y: int):
        """
        Returns list of possible solutions for cell at given position,
        considering the current state of the puzzle.

        Parameters
        ----------
        board: list
            sudoku puzzle board
        x: int
            x coordinate
        y: int
            y coordinate
        """
        col_nums = []  # empty list for column numbers != 0
        for z in range(9):
            if not board[z][x] == 0:
                col_nums.append(board[z][x])  # appends numbers != 0
        # list containing numbers != 0 for the given row
        row_nums = [n for n in board[y] if not n == 0]

        # Finds group for x & y
        x_group = self.find_group(x)
        y_group = self.find_group(y)
        group_nums = []  # empty list containing the cell's group numbers
        for i in y_group:
            for j in x_group:
                if not board[i][j] == 0:
                    group_nums.append(board[i][j])  # appends numbers != 0

        # Set containing all unavailable numbers without duplicates
        numbers = set(col_nums + row_nums + group_nums)
        # Creates list with possible solutions
        possible_solutions = [n for n in range(1, 10) if n not in numbers]

        return possible_solutions

    def validate_cell(self, board: list, x: int, y: int):
        """
        Returns boolean. True if given cell is valid,
        False otherwise.

        Parameters
        ----------
        board: list
            sudoku puzzle
        x: int
            x coordinate
        y: int
            y coordinate
        """
        # Empty dictionaries, these will contain the counts of numbers
        row_counts = {}
        col_counts = {}
        group_counts = {}

        for i in range(9):
            # Registers if numbers for given row and column (if they are not 0)
            if not board[y][i] == 0:
                row_counts[str(board[y][i])] = row_counts.get(
                    str(board[y][i]), 0) + 1
            if not board[i][x] == 0:
                col_counts[str(board[i][x])] = col_counts.get(
                    str(board[i][x]), 0) + 1
        # Finds group for both positions
        col_group = self.find_group(y)
        row_group = self.find_group(x)

        # Registers number in the cell's group (if they are not 0)
        for y_pos in col_group:
            for x_pos in row_group:
                if not board[y_pos][x_pos] == 0:
                    group_counts[str(board[y_pos][x_pos])] = group_counts.get(
                        str(board[y_pos][x_pos]), 0) + 1

        # Checks whether there are duplicates
        if 2 in row_counts.values() or 2 in col_counts.values() or \
                2 in group_counts.values():
            return False

        return True

    def is_solved(self, grid: list):
        """
        Returns boolean. True if the grid is completely solved,
        False otherwise.

        Parameters
        ----------
        grid: list
            sudoku puzzle
        """
        # Iterates over rows
        for i in range(9):

            if 0 in grid[i]:  # Looks for 0s
                return False
            for j in range(9):
                if not self.validate_cell(grid, i, j):  # validates each cell
                    return False
        return True

    def solve_sudoku(self, board: list):
        """
        Recursive function, solves sudoku puzzle and returns boolean:
        True if the game was solved, False otherwise.
        Updates the SudokuGame.solved_grid attribute to the solved puzzle.

        Parameters
        ----------
        board: list
            sudoku puzzle
        """
        self.recursions += 1  # updates the recursion attr. on each call
        if self.is_solved(board):
            return True  # base-case, the board is solved
        else:
            x, y = self.find_blank_cell(board)  # gets coordinates for blank cell
            possible_solutions = self.find_solutions(board, x, y)
            # Checks whether there are possible solutions, if not, backtracks
            if not possible_solutions:
                return False
            # Tries each solution
            for solution in possible_solutions:
                board[y][x] = solution  # updates board position
                results = self.solve_sudoku(board)  # recursion
                if results:  # means grid is solved, exit function
                    self.solved_grid = board  # update the solved grid
                    return True
                if not results:
                    board[y][x] = 0
                    continue  # continues to the next possible solution

    def calc_time(self):
        """Returns time elapsed since the start of the program."""
        return round(self.end - self.start, 2)

    def print_grid(self):
        """Prints unsolved sudoku puzzle."""
        print(*self.grid, sep='\n')

    def print_solution(self):
        """
        Display method. Prints features of the solved game:
        - Time elapsed
        - Amount of recursions
        - Solved grid (readable format)
        """
        print('Time elapsed:', self.calc_time())
        print('Amount of recursions:', self.recursions, end='\n\n')
        print(*self.solved_grid, sep='\n')











