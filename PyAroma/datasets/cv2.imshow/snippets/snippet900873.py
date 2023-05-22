from __future__ import print_function
import numpy as np
import cv2

if (__name__ == '__main__'):
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
        solutionBoard = cv2.imread('./boards/blank.png')
        solutionImage = displaySolution(solutionBoard, final, predictions)
        print("Press 'q' to quit...")
        while True:
            cv2.imshow('Actual Image', image)
            cv2.imshow('Warped Image', warpedImage)
            cv2.imshow('Coords Image', coordsImage)
            cv2.imshow('Solution', solutionImage)
            if ((cv2.waitKey(1) & 255) == ord('q')):
                cv2.destroyAllWindows()
                break
