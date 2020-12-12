#! python3
# Usage: python sloppy_visualization.py [filename] [grid number]

import sys
import pygame
import time
from raw_solver import SudokuGame

pygame.init()


class Game:
    """
    The Game class stores of the board stats, as well as solving
    and visualization methods.

    Parameters
    ----------
    grid: list
        2-D list containing the sudoku puzzle
    screen: pygame.Surface()
        pygame.Surface object

    Attributes
    ----------
    grid: list
        2-D list containing the sudoku puzzle
    solved: list
        2-D list containing the solved sudoku puzzle
    screen: pygame.Surface()
        pygame.Surface object (the game window)
    recursions: int
        amount of recursions needed to solve the puzzle
    start: float
        starting time of the program
    current_time: float
        actual time of the program while it is running
    """

    # Constants for the coordinates of red & green cells
    x_pos = 25
    y_pos = 110
    # Constant for the font of numbers
    font = pygame.font.SysFont('comicsans', 60, True)

    def __init__(self, grid, screen):
        self.grid = grid
        self.solved = None
        self.screen = screen
        self.recursions = 0
        self.start = 0
        self.current_time = 0

    def draw_board(self):
        """Draws board to the game window."""
        for i in range(0, 800, 80):
            if i == 80:
                pygame.draw.line(self.screen, 'black', (i, 80), (i, 800), width=3)
                pygame.draw.line(self.screen, (0, 0, 128), (0, i), (720, i), width=5)
                continue
            pygame.draw.line(self.screen, 'black', (i, 80), (i, 800), width=3)
            pygame.draw.line(self.screen, 'black', (0, i), (720, i), width=3)
        for j in range(240, 800, 240):
            pygame.draw.line(self.screen, (0, 0, 128), (j, 80), (j, 800), width=5)
            pygame.draw.line(self.screen, (0, 0, 128), (0, j + 80), (720, j + 80), width=5)
        pygame.draw.line(self.screen, (0, 0, 128), (0, 80), (0, 800), width=5)

    def steady_numbers(self):
        """Draws 'helping' numbers given by the initial grid."""
        for y in range(9):
            for x in range(9):
                if not self.grid[y][x] == 0:
                    n = self.font.render(str(self.grid[y][x]), 1, 'black')
                    self.screen.blit(n, ((self.x_pos + x * 80), (self.y_pos + y * 80)))

    def set_screen(self):
        """Initializes game window."""
        self.screen.fill((255, 255, 255))
        self.draw_board()
        self.steady_numbers()
        pygame.display.update()

    @staticmethod
    def rect_area(x, y):
        """
        Parameters
        ----------
        x: int
            x coordinate
        y: int
            y coordinate

        Returns
        -------
        4 integer tuple to draw a rect, containing (x pos, y pos, length, width)
        """
        # 80 (size of cell), + 5 and 70 so as to not block the original cell
        return x * 80 + 5, 80 + y * 80 + 5, 80 - 10, 80 - 10

    def draw_cell(self, board, x, y, color):
        """
        Draws red rectangle around cell at given location.

        Parameters
        ----------
        board: list
            2-d list, containing the current state of the board
        x: int
            x coordinate
        y:
            y coordinate
        color: tuple
            3-integer tuple containing RGB values
        """
        r = self.rect_area(x, y) # gets rect area for given cell
        pygame.draw.rect(self.screen, color, r, 3)
        e = self.font.render(str(board[y][x]), 1, (0, 0, 0))  # creates number
        self.screen.blit(e, (self.x_pos + x * 80, self.y_pos + y * 80))  # draws number
        pygame.display.update(r)  # updates screen to showcase rect

    def green_cell(self, x, y):
        """
        Draws green cell around cell at given location.
        Parameters
        ----------
        x: int
            x coordinate
        y: int
            y coordinate
        """
        r = self.rect_area(x, y)  # gets rect area for cell
        pygame.draw.rect(self.screen, (0, 255, 0), r, 3)
        pygame.display.update(r)  # updates screen to showcase green rect

    def clear_cell(self, x, y):
        """
        Clears cell in case of backtrack.
        Parameters
        ----------
        x: int
            x coordinate
        y: int
            y coordinate
        """
        r = self.rect_area(x, y)
        background = pygame.Surface((75, 75))  # creates a white surface
        background.fill((255, 255, 255))
        self.screen.blit(background, (x * 80 + 3, 80 + y * 80 + 3))  # draw
        pygame.display.update(r)  # update screen to showcase changes

    def print_stats(self):
        """Prints stats onto the screen (recursions & time elapsed)."""
        self.clear_top()
        font2 = pygame.font.SysFont('comicsans', 40, True) # creates new font object
        minutes, seconds = divmod(self.current_time - self.start, 60)  # calculation
        minutes, seconds = round(minutes), round(seconds)  # rounds numbers
        if seconds == 60:
            seconds = 0
        # Draw text onto the screen
        text = font2.render('Attempts: ' + str(self.recursions), 1, (0, 0, 0))
        if len(str(seconds)) == 1:
            seconds = '0' + str(seconds)
        text2 = font2.render(' Time: 0{}:{}'.format(minutes, seconds),
                             1, (0, 0, 0))
        self.screen.blit(text, (20, 20))
        self.screen.blit(text2, (480, 20))
        pygame.display.update((0, 0, 720, 800))

    def clear_top(self):
        """Clears the top of the screen to update recursions and time."""
        background = pygame.Surface((720, 77))
        background.fill((255, 255, 255))
        self.screen.blit(background, (0, 0))
        pygame.display.update((0, 0, 720, 77))

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
            y coordinate
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
        self.current_time = time.time()
        pygame.time.delay(100)
        self.recursions += 1  # updates the recursion attr. on each call
        self.print_stats()
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
                self.draw_cell(board, x, y, (255, 0, 0))

                results = self.solve_sudoku(board)  # recursion
                if results:  # means grid is solved, exit function
                    self.green_cell(x, y)
                    self.solved = board  # update the solved grid
                    return True
                if not results:
                    self.clear_cell(x, y) # clear cell in case of backtrack
                    board[y][x] = 0
                    continue  # continues to the next possible solution


# VISUALIZATION DEMO

sudoku = Game(SudokuGame.load_grid(sys.argv[1], int(sys.argv[2])), pygame.display.set_mode((720, 800)))
pygame.display.set_caption('Sudoku')

# Handles missing icon file
try:
    pygame.display.set_icon(pygame.image.load('puzzle-piece.png'))
except FileNotFoundError:
    pass

sudoku.set_screen()

running = True
done = False
while running:
    for events in pygame.event.get():
        if events.type == pygame.QUIT:
            running = False
        if done:
            continue
        if events.type == pygame.KEYDOWN:
            if events.key == pygame.K_SPACE:
                sudoku.start = time.time()
                sudoku.solve_sudoku(sudoku.grid)
                done = True
