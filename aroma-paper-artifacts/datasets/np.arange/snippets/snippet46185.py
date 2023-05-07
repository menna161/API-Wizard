import numpy as np
import random
import copy


def _some_variables():
    parent = (np.array([0, 1, 2, 3, 4, 5, 1, 7, 8, 9, 10, 1, 12, 13, 14, 15, 13, 17, 18, 19, 20, 21, 20, 23, 13, 25, 26, 27, 28, 29, 28, 31]) - 1)
    offset = np.array([0.0, 0.0, 0.0, (- 132.948591), 0.0, 0.0, 0.0, (- 442.894612), 0.0, 0.0, (- 454.206447), 0.0, 0.0, 0.0, 162.767078, 0.0, 0.0, 74.999437, 132.948826, 0.0, 0.0, 0.0, (- 442.894413), 0.0, 0.0, (- 454.20659), 0.0, 0.0, 0.0, 162.767426, 0.0, 0.0, 74.999948, 0.0, 0.1, 0.0, 0.0, 233.383263, 0.0, 0.0, 257.077681, 0.0, 0.0, 121.134938, 0.0, 0.0, 115.002227, 0.0, 0.0, 257.077681, 0.0, 0.0, 151.034226, 0.0, 0.0, 278.882773, 0.0, 0.0, 251.733451, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 99.999627, 0.0, 100.000188, 0.0, 0.0, 0.0, 0.0, 0.0, 257.077681, 0.0, 0.0, 151.031437, 0.0, 0.0, 278.892924, 0.0, 0.0, 251.72868, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 99.999888, 0.0, 137.499922, 0.0, 0.0, 0.0, 0.0]).reshape((- 1), 3)
    rotInd = [[5, 6, 4], [8, 9, 7], [11, 12, 10], [14, 15, 13], [17, 18, 16], [], [20, 21, 19], [23, 24, 22], [26, 27, 25], [29, 30, 28], [], [32, 33, 31], [35, 36, 34], [38, 39, 37], [41, 42, 40], [], [44, 45, 43], [47, 48, 46], [50, 51, 49], [53, 54, 52], [56, 57, 55], [], [59, 60, 58], [], [62, 63, 61], [65, 66, 64], [68, 69, 67], [71, 72, 70], [74, 75, 73], [], [77, 78, 76], []]
    expmapInd = np.split((np.arange(4, 100) - 1), 32)
    return (parent, offset, rotInd, expmapInd)