import numpy as np
import math
import time
from pycuda import driver
import SimpleITK as sitk


def concatenate4x4(*matrix_Nx4x4):
    matrix = np.identity(4)
    for m in matrix_Nx4x4:
        matrix = np.matmul(matrix, m)
    return matrix
