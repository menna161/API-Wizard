from __future__ import absolute_import, division, print_function, unicode_literals
import tensorflow as tf
import tensorflow.contrib.slim as slim
from tensorflow.contrib import distributions as dist
from tensorflow.contrib.rnn import RNNCell
import numpy as np
from matplotlib.colors import hsv_to_rgb
import matplotlib.pyplot as plt
import os
import shutil
from dps import cfg
from dps.utils import Param
from dps.utils.tf import ScopedFunction


def get_gamma_colors(nr_colors):
    hsv_colors = np.ones((nr_colors, 3))
    hsv_colors[(:, 0)] = ((np.linspace(0, 1, nr_colors, endpoint=False) + (2 / 3)) % 1.0)
    color_conv = hsv_to_rgb(hsv_colors)
    return color_conv
