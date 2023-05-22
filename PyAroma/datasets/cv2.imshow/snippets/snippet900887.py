import cv2
from basic import *
from sud import *
from solver import *

if (__name__ == '__main__'):
    detected = False
    solved = False
    tiles = []
    print('Get board closer to webcam until stated otherwise...')
    while True:
        (retr, frame) = cap.read()
        preprocess = preprocessImage(frame)
        preprocess = cv2.bitwise_not(preprocess.copy(), preprocess.copy())
        contourImage = preprocess.copy()
        contourImage = cv2.cvtColor(contourImage, cv2.COLOR_GRAY2BGR)
        coordsImage = contourImage.copy()
        (contours, polygon) = getContours(preprocess)
        coords = getCoords(contourImage, polygon)
        if (detected and solved):
            unwarpedImage = unwarp(solutionImage, coords)
        else:
            unwarpedImage = np.zeros((frame.shape[0], frame.shape[1]))
        if ((cv2.contourArea(polygon) > 80000) and (not detected)):
            for coord in coords:
                cv2.circle(coordsImage, (coord[0], coord[1]), 5, (255, 0, 0), (- 1))
            cv2.drawContours(contourImage, polygon, (- 1), (0, 255, 0), 3)
            cv2.drawContours(frame, polygon, (- 1), (0, 255, 0), 3)
            warpedImage = warp(coordsImage.copy(), coords)
            warpedImage = cv2.resize(warpedImage, (540, 540))
            rects = displayGrid(warpedImage)
            tiles = extractGrid(warpedImage, rects)
            if (cv2.contourArea(polygon) >= 90000):
                print('Detected')
                detected = True
            else:
                print('Bring closer...')
        else:
            warpedImage = np.zeros((540, 540))
        if (detected and (not solved)):
            predictions = getPredictions(tiles)
            solutionImage = solveSudoku(predictions, coords)
            solved = True
        if (retr == True):
            cv2.imshow('Frame', frame)
            if solved:
                cv2.imshow('Solution', solutionImage)
            if ((cv2.waitKey(1) & 255) == ord('q')):
                cap.release()
                cv2.destroyAllWindows()
                break
        else:
            cap.release()
            cv2.destroyAllWindows()
            break
