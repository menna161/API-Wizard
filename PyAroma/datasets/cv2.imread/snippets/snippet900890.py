from __future__ import print_function
import numpy as np
import cv2


def solveSudoku(predictions, coords):
    board = np.array(predictions).reshape((9, 9))
    print(board)
    print('Solving...')
    solver = SudokuSolver(board)
    solver.solve()
    final = solver.board
    if (0 in final):
        print('Error occured while solving, try another image!')
    else:
        print(final)
    solutionBoard = cv2.imread('./blank.png')
    solutionImage = displaySolution(solutionBoard, final, predictions)
    return solutionImage
