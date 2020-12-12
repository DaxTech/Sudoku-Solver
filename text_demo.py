#! python3
# Usage: python text_demo.py [filename] [grid number] [smart or raw]
import smart_solver
import raw_solver
import sys
import time


# ALGORITHM DEMO

if sys.argv[3].lower() == 'smart':
    game = smart_solver.SudokuGame.load_grid(sys.argv[1], int(sys.argv[2]))
    testRun = smart_solver.SudokuGame(game)
    testRun.print_grid()
    testRun.solve_sudoku(testRun.grid)
    testRun.end = time.time()
    testRun.print_solution()
    sys.exit()
elif sys.argv[3].lower() == 'raw':
    game = raw_solver.SudokuGame.load_grid(sys.argv[1], int(sys.argv[2]))
    testRun = raw_solver.SudokuGame(game)
    testRun.print_grid()
    testRun.solve_sudoku(testRun.grid)
    testRun.end = time.time()
    testRun.print_solution()
    sys.exit
else:
    print('Unknown command: '+sys.argv[3]+'\nPlease try again.')
    sys.exit(1)

