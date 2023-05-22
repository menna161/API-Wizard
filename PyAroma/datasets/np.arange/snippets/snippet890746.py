import ctypes
import os
import numpy as np


@staticmethod
def np_2d_arr_to_c(np_2d_arr):
    return (np_2d_arr.__array_interface__['data'][0] + (np.arange(np_2d_arr.shape[0]) * np_2d_arr.strides[0])).astype(np.intp)
