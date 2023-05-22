import cv2
import numpy as np
import tensorflow as tf
from logging import exception
import math
import scipy.stats as st
import os
import urllib
import scipy
from scipy import io
from enum import Enum
from easydict import EasyDict as edict


def gauss_kernel(size=21, sigma=3):
    interval = (((2 * sigma) + 1.0) / size)
    x = np.linspace(((- sigma) - (interval / 2)), (sigma + (interval / 2)), (size + 1))
    ker1d = np.diff(st.norm.cdf(x))
    kernel_raw = np.sqrt(np.outer(ker1d, ker1d))
    kernel = (kernel_raw / kernel_raw.sum())
    out_filter = np.array(kernel, dtype=np.float32)
    out_filter = out_filter.reshape((size, size, 1, 1))
    return out_filter
